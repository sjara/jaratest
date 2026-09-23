#!/usr/bin/env python3
"""
make_1overf_scrambled_examples.py

Generate the agreed 500-ms 1/f AM/FM dynamic tone complex, then make scrambled
versions at 125, 62.5, 31.25, and 15.625 ms.

Two boundary treatments:
  1) true 4-ms equal-power overlap crossfade (conceptually +/-2 ms at each join)
  2) literal 4-ms silent gaps between chunks

Important:
  - A true overlap crossfade SHORTENS total duration by 4 ms per boundary.
  - Literal gaps LENGTHEN total duration by 4 ms per boundary.
  - Both versions use the exact same permutation at each chunk size.
"""

from pathlib import Path
import argparse
import numpy as np
from scipy.io import wavfile

F0S = np.array([4000, 5040, 6350, 8000, 10080, 12700, 16000, 20160, 25400, 32000], float)
CHUNK_MS = [125.0, 62.5, 31.25, 15.625]

def one_over_f_process(n, fs, fmin, fmax, gamma, rng):
    freqs = np.fft.rfftfreq(n, 1/fs)
    spec = np.zeros(freqs.size, complex)
    keep = (freqs >= fmin) & (freqs <= fmax)
    phases = rng.uniform(0, 2*np.pi, keep.sum())
    spec[keep] = freqs[keep]**(-gamma/2) * np.exp(1j*phases)
    x = np.fft.irfft(spec, n=n)
    return 2*(x-x.min())/(x.max()-x.min()) - 1

def save(path, fs, y):
    wavfile.write(path, fs, np.int16(np.clip(y, -1, 1)*32767))

def permute_nonidentity(n, rng):
    identity = np.arange(n)
    while True:
        p = rng.permutation(identity)
        if not np.array_equal(p, identity):
            return p

def crossfade(chunks, fs, overlap_ms=4.0):
    L = int(round(overlap_ms*fs/1000))
    theta = np.linspace(0, np.pi/2, L)
    fo, fi = np.cos(theta), np.sin(theta)
    out = chunks[0].copy()
    for nxt in chunks[1:]:
        ov = out[-L:]*fo + nxt[:L]*fi
        out = np.concatenate([out[:-L], ov, nxt[L:]])
    return out

def add_gaps(chunks, fs, gap_ms=4.0):
    z = np.zeros(int(round(gap_ms*fs/1000)))
    pieces = []
    for i, ch in enumerate(chunks):
        if i:
            pieces.append(z)
        pieces.append(ch)
    return np.concatenate(pieces)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", default="one_over_f_scrambles")
    ap.add_argument("--seed", type=int, default=20260923)
    args = ap.parse_args()

    fs = 192000
    dur = 0.5
    n = int(fs*dur)
    rng = np.random.default_rng(args.seed)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    a = one_over_f_process(n, fs, 2, 80, 1.0, rng)
    q = one_over_f_process(n, fs, 2, 80, 1.0, rng)

    level_db = 60 + 10*a
    A = 10**((level_db-60)/20)
    oct_shift = 0.30*q

    phases0 = rng.uniform(0, 2*np.pi, len(F0S))
    comps = []
    for f0, p0 in zip(F0S, phases0):
        f = f0 * 2**oct_shift
        phase = p0 + 2*np.pi*np.cumsum(f)/fs
        comps.append(np.sin(phase))

    s = A * np.sum(comps, axis=0)/np.sqrt(len(comps))

    nr = int(round(0.005*fs))
    r = np.sin(np.linspace(0, np.pi/2, nr))**2
    s[:nr] *= r
    s[-nr:] *= r[::-1]
    s /= np.max(np.abs(s))
    s *= 10**(-3/20)

    save(outdir/"base_1overf_naturalistic_500ms.wav", fs, s)

    for ms in CHUNK_MS:
        cn = int(round(ms*fs/1000))
        chunks = s.reshape(-1, cn)
        order = permute_nonidentity(len(chunks), rng)
        chunks = chunks[order]

        tag = str(ms).replace(".", "p")
        xc = crossfade(chunks, fs, 4.0)
        xg = add_gaps(chunks, fs, 4.0)

        save(outdir/f"scrambled_{tag}ms_crossfade_pm2ms.wav", fs, xc)
        save(outdir/f"scrambled_{tag}ms_gap_4ms.wav", fs, xg)
        print(ms, "ms order:", order.tolist(),
              "crossfade duration ms=", len(xc)/fs*1000,
              "gap duration ms=", len(xg)/fs*1000)

if __name__ == "__main__":
    main()
