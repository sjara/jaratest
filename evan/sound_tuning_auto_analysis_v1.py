#!/usr/bin/env python3
"""
Automatic sound_tuning analysis planner/runner (v1).

Reads info2p and every session's behavior file for the requested dates, works out which
sounds were presented in each FOV, and runs the matching analyses:

    * Pure-tone level series -- any FOV with pure-tone sessions at >= 2 different levels:
        sound_tuning_pure_tone_levels_fov_analysis_v2.py (those sessions only), then
        posthoc_figures/bf_level_figures.py and posthoc_figures/bf_level_tonotopy.py with
        --fov-order AREA=<FOV# ascending> (FOV# is assumed to follow the physical order
        along the tonotopic axis; use --no-fov-order to sort by median BF/CF instead).
    * Multistim ("regular") analysis -- any FOV with a chord, FM, FM fixed-range, band-noise,
        or noise-pair session: sound_tuning_multistim_fov_analysis_v6.py on those sessions
        plus the FOV's pure-tone sessions (v6 uses one pure-tone level per FOV). An FOV with
        two chord F0s is sent to the dual-F0 branch (sound_tuning_multistim_dualF0_fov_analysis_v1.py)
        instead, which only knows pure tones / chords / fixed-duration FM.
    * Stages 2/3 (GREEN vs YELLOW by layer; cross-area) run only when a red channel was
        recorded (stage 3 also needs >= 2 areas). Stage 2/3 v6 cover pure tones, chords and
        fixed-duration FM only.

The sound type comes from the behavior file (current_stim_type), so sessionLabels do not
need to follow a pattern; the level from current_intensity. Sessions without a behavior file,
without a Suite2p folder, with several sound types, or with AM / fading noise (those belong
to sound_tuning_area_analysis_v13.py) are listed and left out.

Detection is imported from sound_tuning_multistim_fov_analysis_v6.py on purpose, so the planner
and the analysis always agree on what a block is.

Example
-------
python sound_tuning_auto_analysis_v1.py imag041 --dates 20261015 --dry-run   # print the plan
python sound_tuning_auto_analysis_v1.py imag041 --dates 20261015             # run it
python sound_tuning_auto_analysis_v1.py imag041 --dates 20261015 --only levels

Output: the plan (plan.json, plan.txt) and one log per step under
<TEMP_OUTPUT_PATH>/evan/sound_tuning_auto_analysis/<subject>/<date_tag>/; each analysis writes
to its usual output folder.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np

from jaratoolbox import settings

HERE = Path(__file__).resolve().parent
MULTISTIM = "sound_tuning_multistim_fov_analysis_v6.py"
LEVELS = "sound_tuning_pure_tone_levels_fov_analysis_v2.py"
DUALF0 = "sound_tuning_multistim_dualF0_fov_analysis_v1.py"
STAGE2 = "sound_tuning_multistim_area_layer_green_yellow_analysis_v6.py"
STAGE3 = "sound_tuning_multistim_cross_area_cellclass_analysis_v6.py"
DUALF0_STAGE2 = "sound_tuning_multistim_dualF0_area_layer_green_yellow_analysis_v1.py"
DUALF0_STAGE3 = "sound_tuning_multistim_dualF0_cross_area_cellclass_analysis_v1.py"
BF_FIGURES = "posthoc_figures/bf_level_figures.py"
BF_TONOTOPY = "posthoc_figures/bf_level_tonotopy.py"
LEVELS_FAMILY = "sound_tuning_pure_tone_levels_fov_analysis"


def _load_v6():
    spec = importlib.util.spec_from_file_location("_multistim_v6", HERE / MULTISTIM)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ms = _load_v6()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject")
    p.add_argument("--dates", nargs="+", required=True)
    p.add_argument("--areas", nargs="+", default=None, choices=["A1", "AAF", "A2"], help="default: every area found")
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--only", choices=["levels", "multistim"], default=None, help="run only one analysis family")
    p.add_argument("--exclude-sessions", nargs="+", default=None, metavar="SESSION",
                   help="leave out these sessions (001, 20261015_001, or 001-004)")
    p.add_argument("--pure-tone-level", type=float, default=None, help="passed to multistim v6")
    p.add_argument("--n-permutations", type=int, default=None, help="passed to the stage-1 scripts")
    p.add_argument("--skip-cell-reports", action="store_true", help="passed to the stage-1 scripts")
    p.add_argument("--no-fov-order", action="store_true", help="do not pass --fov-order to the posthoc BF figures")
    p.add_argument("--dry-run", action="store_true", help="print and save the plan; run nothing")
    return p.parse_args()


def suite2p_status(subject: str, date: str, session: str, plane: int) -> dict[str, Any]:
    d = Path(settings.TWOPHOTON_PATH) / f"{subject}_processed" / date / session / "suite2p" / f"plane{plane}"
    if not (d / "iscell.npy").exists():
        return {"suite2p_dir": str(d), "suite2p_ok": False, "red_channel": None, "n_rois": 0}
    ops = np.load(d / "ops.npy", allow_pickle=True).item() if (d / "ops.npy").exists() else {}
    red = ops.get("meanImg_chan2") is not None or int(ops.get("nchannels", 1)) > 1
    return {"suite2p_dir": str(d), "suite2p_ok": True, "red_channel": bool(red),
            "n_rois": int(len(np.load(d / "iscell.npy")))}


def _range_tokens(date_sessions: list[str]) -> list[str]:
    """['20261015_001','20261015_002','20261015_003','20261015_005'] -> ['20261015_001-003','20261015_005']."""
    by_date: dict[str, list[int]] = {}
    for tok in date_sessions:
        d, _, sess = tok.rpartition("_"); by_date.setdefault(d, []).append(int(sess))
    out = []
    for d, nums in sorted(by_date.items()):
        nums = sorted(set(nums)); i = 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            out.append(f"{d}_{nums[i]:03d}" if i == j else f"{d}_{nums[i]:03d}-{nums[j]:03d}")
            i = j + 1
    return out


def inventory(subject: str, dates: list[str], areas: list[str] | None, plane: int,
              exclude: set | None) -> list[dict[str, Any]]:
    _, sessions = ms.load_info2p(subject)
    rows = []
    for s in sessions:
        date = str(s.get("date", "")); sess = str(s.get("session", "")).zfill(3)
        area = ms.canonical_area(s.get("brainArea", ""))
        if date not in dates or str(s.get("paradigm", "")) != ms.PARADIGM or area is None:
            continue
        if areas and area not in areas:
            continue
        rec = {"date": date, "session": sess, "area": area, "brainArea": s.get("brainArea"),
               "FOV#": s.get("FOV#"), "depth": s.get("depth"), "sessionLabel": s.get("sessionLabel")}
        if exclude and ms._in_filter(exclude, date, sess):
            rows.append({**rec, "use": False, "reason": "excluded on the command line"}); continue
        info = ms.inspect_behavior_session(subject, date, sess)
        rec.update({"status": info["status"], "stim_types": info["stim_types"], "block": info["detected_block"],
                    "level_db": info["level_db"], "n_trials": info["n_trials"],
                    "center_frequency_hz": info.get("center_frequency_hz"), "chord_F0_hz": info.get("chord_F0_hz")})
        if info["status"] == "no_stim_type":
            rec["block"] = ms.canonical_block(s.get("sessionLabel", ""))
        rec.update(suite2p_status(subject, date, sess, plane))
        if info["status"] == "no_behavior":
            rec.update(use=False, reason="no behavior file")
        elif info["status"] == "mixed":
            rec.update(use=False, reason=f"several sound types in one session: {info['stim_types']}")
        elif rec["block"] is None:
            rec.update(use=False, reason=f"sound type {info['stim_types']} not handled here "
                                         "(AM / fading noise: sound_tuning_area_analysis_v13.py)")
        elif not rec["suite2p_ok"]:
            rec.update(use=False, reason=f"no Suite2p output at {rec['suite2p_dir']}")
        elif rec["FOV#"] is None:
            rec.update(use=False, reason="no FOV# in info2p (run multistim v6 with --fov-groups by hand)")
        else:
            rec.update(use=True, reason="")
        rows.append(rec)
    rows.sort(key=lambda r: (r["date"], r["session"]))
    return rows


def make_plan(rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    use = [r for r in rows if r.get("use")]
    plan: dict[str, Any] = {"levels": {}, "multistim": {}, "dualF0": {}, "stage2": False, "stage3": False,
                            "dualF0_stage2": False, "dualF0_stage3": False, "notes": []}
    fovs: dict[tuple, list[dict[str, Any]]] = {}
    for r in use:
        fovs.setdefault((r["area"], r["date"], int(r["FOV#"])), []).append(r)
    red_any = False
    for (area, date, fov), seq in sorted(fovs.items()):
        pure = [r for r in seq if r["block"] == "pure_tones"]
        other = [r for r in seq if r["block"] != "pure_tones"]
        red_any |= any(r.get("red_channel") for r in seq)
        # Level series: >= 2 distinct pure-tone levels. A repeated level keeps the later session (a redo).
        by_level: dict[float, dict[str, Any]] = {}
        for r in pure:
            if np.isfinite(r["level_db"]):
                if r["level_db"] in by_level:
                    plan["notes"].append(f"{date} FOV{fov}: two pure-tone sessions at {r['level_db']:g} dB "
                                         f"({by_level[r['level_db']]['session']}, {r['session']}); level series uses {r['session']}")
                by_level[r["level_db"]] = r
        if len(by_level) >= 2:
            plan["levels"].setdefault(area, {"dates": set(), "sessions": [], "fovs": []})
            plan["levels"][area]["dates"].add(date)
            plan["levels"][area]["sessions"] += [f"{date}_{r['session']}" for r in sorted(by_level.values(), key=lambda x: x["session"])]
            plan["levels"][area]["fovs"].append(fov)
        if other:
            chords = [r for r in other if r["block"] == "chord_tones"]
            target = "dualF0" if len({r.get("chord_F0_hz") for r in chords}) >= 2 else "multistim"
            if target == "dualF0":
                new = [r["block"] for r in other if r["block"] not in ("chord_tones", "fm_tones")]
                if new:
                    plan["notes"].append(f"{date} FOV{fov}: two chord F0s -> dual-F0 branch; its {sorted(set(new))} "
                                         "blocks are not analyzed by that branch")
            dup = {b for b in (r["block"] for r in other) if sum(x["block"] == b for x in other) > 1}
            if target == "multistim" and dup:
                plan["notes"].append(f"{date} FOV{fov}: several {sorted(dup)} sessions; multistim v6 will stop. "
                                     "Use --exclude-sessions to keep one.")
            plan[target].setdefault(area, {"dates": set(), "sessions": [], "fovs": []})
            plan[target][area]["dates"].add(date)
            plan[target][area]["sessions"] += [f"{date}_{r['session']}" for r in sorted(seq, key=lambda x: x["session"])]
            plan[target][area]["fovs"].append(fov)
    ms_areas = sorted(set(plan["multistim"]) | set(plan["dualF0"]))
    for key, s2, s3 in (("multistim", "stage2", "stage3"), ("dualF0", "dualF0_stage2", "dualF0_stage3")):
        if not plan[key]:
            continue
        if not red_any:
            plan["notes"].append(f"{key}: no red channel recorded, so GREEN/YELLOW stage 2 and cross-area stage 3 are skipped.")
            continue
        plan[s2] = True
        plan[s3] = len(plan[key]) >= 2
        if not plan[s3]:
            plan["notes"].append(f"{key}: only one area, so cross-area stage 3 is skipped.")
    for key in ("levels", "multistim", "dualF0"):
        for a in plan[key].values():
            a["dates"] = sorted(a["dates"])
    plan["areas_with_multistim"] = ms_areas
    return plan


def commands(plan: dict[str, Any], args: argparse.Namespace) -> list[tuple[str, list[str]]]:
    py = sys.executable; out = []
    common = ["--plane", str(args.plane)]
    s1 = list(common)
    if args.n_permutations is not None: s1 += ["--n-permutations", str(args.n_permutations)]
    if args.skip_cell_reports: s1 += ["--skip-cell-reports"]
    if args.only in (None, "levels"):
        for area, a in sorted(plan["levels"].items()):
            out.append((f"levels_{area}", [py, str(HERE / LEVELS), args.subject, "--area", area, "--dates", *a["dates"],
                                           "--sessions", *_range_tokens(a["sessions"]), *s1]))
            root = str(Path(settings.TEMP_OUTPUT_PATH) / "evan" / LEVELS_FAMILY / args.subject)
            date_tag = "_".join(a["dates"])
            order = [] if args.no_fov_order else ["--fov-order", f"{area}=" + ",".join(str(f) for f in sorted(set(a["fovs"])))]
            for name, script in (("bf_figures", BF_FIGURES), ("bf_tonotopy", BF_TONOTOPY)):
                out.append((f"{name}_{area}", [py, str(HERE / script), root, "--date", date_tag, "--areas", area, *order]))
    if args.only in (None, "multistim"):
        for area, a in sorted(plan["multistim"].items()):
            cmd = [py, str(HERE / MULTISTIM), args.subject, "--area", area, "--dates", *a["dates"],
                   "--sessions", *_range_tokens(a["sessions"]), *s1]
            if args.pure_tone_level is not None: cmd += ["--pure-tone-level", str(args.pure_tone_level)]
            out.append((f"multistim_{area}", cmd))
        for area, a in sorted(plan["dualF0"].items()):
            cmd = [py, str(HERE / DUALF0), args.subject, "--area", area, "--dates", *a["dates"], *common]
            if args.n_permutations is not None: cmd += ["--n-permutations", str(args.n_permutations)]
            out.append((f"dualF0_{area}", cmd))
        dates = sorted({d for a in plan["multistim"].values() for d in a["dates"]})
        areas = sorted(plan["multistim"])
        if plan["stage2"]:
            out.append(("stage2", [py, str(HERE / STAGE2), args.subject, "--dates", *dates, "--areas", *areas]))
        if plan["stage3"]:
            out.append(("stage3", [py, str(HERE / STAGE3), args.subject, "--dates", *dates, "--areas", *areas]))
        ddates = sorted({d for a in plan["dualF0"].values() for d in a["dates"]})
        dareas = sorted(plan["dualF0"])
        if plan["dualF0_stage2"]:
            out.append(("dualF0_stage2", [py, str(HERE / DUALF0_STAGE2), args.subject, "--dates", *ddates, "--areas", *dareas]))
        if plan["dualF0_stage3"]:
            out.append(("dualF0_stage3", [py, str(HERE / DUALF0_STAGE3), args.subject, "--dates", *ddates, "--areas", *dareas]))
    return out


def format_plan(rows: list[dict[str, Any]], plan: dict[str, Any], cmds: list[tuple[str, list[str]]]) -> str:
    lines = ["SESSIONS", "-" * 100]
    for r in rows:
        lvl = f"{r['level_db']:g} dB" if r.get("level_db") is not None and np.isfinite(r.get("level_db", np.nan)) else ""
        cf = f" center {r['center_frequency_hz']/1000:g} kHz" if r.get("center_frequency_hz") else ""
        f0 = f" F0 {r['chord_F0_hz']/1000:g} kHz" if r.get("chord_F0_hz") else ""
        red = "" if r.get("red_channel") is None else (" red" if r["red_channel"] else " no-red")
        tag = "use " if r.get("use") else "SKIP"
        lines.append(f"{tag} {r['date']}_{r['session']} {r['area']:4s} FOV{r.get('FOV#')!s:4s} {str(r.get('block')):11s} "
                     f"{lvl:7s}{cf}{f0}{red} | {r.get('sessionLabel')} {('-- ' + r['reason']) if r.get('reason') else ''}")
    lines += ["", "ANALYSES"]
    for key, title in (("levels", "Pure-tone level series"), ("multistim", "Multistim v6"), ("dualF0", "Dual-F0 chords")):
        for area, a in sorted(plan[key].items()):
            lines.append(f"  {title} {area}: FOVs {sorted(set(a['fovs']))}; sessions {' '.join(_range_tokens(a['sessions']))}")
    yn = lambda k: "yes" if plan[k] else "no"
    lines.append(f"  Stage 2 (GREEN vs YELLOW): {yn('stage2')} | Stage 3 (cross-area): {yn('stage3')}"
                 + (f" | dual-F0 stage 2: {yn('dualF0_stage2')}, stage 3: {yn('dualF0_stage3')}" if plan["dualF0"] else ""))
    for n in plan["notes"]:
        lines.append(f"  NOTE: {n}")
    lines += ["", "COMMANDS"] + [f"  [{name}] " + " ".join(c) for name, c in cmds]
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    dates = [str(d) for d in args.dates]
    rows = inventory(args.subject, dates, args.areas, args.plane, ms.parse_session_filter(args.exclude_sessions))
    if not rows:
        raise RuntimeError(f"No {ms.PARADIGM} sessions in info2p for {args.subject} on {dates}")
    plan = make_plan(rows, args)
    cmds = commands(plan, args)
    text = format_plan(rows, plan, cmds)
    print(text)
    out = Path(settings.TEMP_OUTPUT_PATH) / "evan" / "sound_tuning_auto_analysis" / args.subject / "_".join(dates)
    out.mkdir(parents=True, exist_ok=True)
    (out / "plan.txt").write_text(text + "\n", encoding="utf-8")
    (out / "plan.json").write_text(json.dumps(ms.jsonable({"sessions": rows, "plan": plan,
                                                           "commands": [{"step": n, "cmd": c} for n, c in cmds]}), indent=2))
    if args.dry_run or not cmds:
        print("\nDry run: nothing executed." if args.dry_run else "\nNothing to run.")
        return
    failed = []; skip = set()
    for name, cmd in cmds:
        if name in skip:
            print(f"\n=== {name}: skipped (its stage-1 run failed)"); continue
        log = out / f"{name}.log"
        print(f"\n=== {name} (log: {log})")
        with open(log, "w") as fh:
            rc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, cwd=str(HERE)).returncode
        print(f"    exit code {rc}")
        if rc:
            failed.append(name)
            if name.startswith("levels_"):
                area = name.split("_", 1)[1]
                skip |= {f"bf_figures_{area}", f"bf_tonotopy_{area}"}
            if name.startswith("multistim_"):
                skip |= {"stage2", "stage3"}
            if name.startswith("dualF0_") and "stage" not in name:
                skip |= {"dualF0_stage2", "dualF0_stage3"}
    print("\nDONE" + (f"; failed steps: {failed}" if failed else ""))


if __name__ == "__main__":
    main()
