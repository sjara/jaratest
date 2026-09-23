#!/usr/bin/env python3
from pathlib import Path
import argparse
import numpy as np
from scipy.io import wavfile

CHUNK_MS = [500.0, 125.0, 62.5, 31.25, 15.625]

def to_float(a):
    if np.issubdtype(a.dtype, np.floating):
        return a.astype(float)
    if a.dtype == np.int16:
        return a.astype(float)/32768.0
    if a.dtype == np.int32:
        return a.astype(float)/2147483648.0
    if a.dtype == np.uint8:
        return (a.astype(float)-128.0)/128.0
    raise TypeError(a.dtype)

def save(path, fs, a):
    peak = np.max(np.abs(a))
    if peak > 1:
        a = a/peak
    wavfile.write(path, fs, np.int16(np.clip(a,-1,1)*32767))

def scramble(a, fs, chunk_ms, rng):
    n = int(round(fs*chunk_ms/1000.0))
    if len(a) % n:
        raise ValueError(f"{chunk_ms} ms does not divide 500 ms exactly at fs={fs}.")
    chunks = a.reshape(len(a)//n, n, *a.shape[1:]).copy()
    base = np.arange(len(chunks))
    if len(base) == 1:
        return a.copy(), base
    while True:
        perm = rng.permutation(base)
        if not np.array_equal(perm, base):
            break
    return chunks[perm].reshape(a.shape), perm

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--n-scrambles", type=int, default=8)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--start-ms", type=float, default=0.0)
    ap.add_argument("--output-dir", default=None)
    args = ap.parse_args()

    path = Path(args.wav)
    fs, a = wavfile.read(path)
    a = to_float(a)

    start = int(round(args.start_ms*fs/1000.0))
    n500 = int(round(0.5*fs))
    source = a[start:start+n500]
    if len(source) != n500:
        raise ValueError("Not enough audio for a full 500-ms segment.")

    outdir = Path(args.output_dir) if args.output_dir else path.parent/(path.stem+"_scrambles")
    outdir.mkdir(parents=True, exist_ok=True)
    save(outdir/"chunk_500ms_intact.wav", fs, source)

    rng = np.random.default_rng(args.seed)
    for ms in CHUNK_MS[1:]:
        for i in range(args.n_scrambles):
            y, order = scramble(source, fs, ms, rng)
            label = str(ms).replace(".","p")
            out = outdir/f"chunk_{label}ms_scramble_{i+1:02d}.wav"
            save(out, fs, y)
            print(out.name, "order=", order.tolist())

if __name__ == "__main__":
    main()
