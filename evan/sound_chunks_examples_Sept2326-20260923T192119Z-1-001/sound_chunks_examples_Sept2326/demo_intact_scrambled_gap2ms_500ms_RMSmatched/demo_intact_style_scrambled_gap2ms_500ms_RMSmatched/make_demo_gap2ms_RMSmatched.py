#!/usr/bin/env python3
"""
Recreate the original demo_intact_500ms.wav sound and make RMS-matched
500-ms scrambled versions with 2-ms silent gaps.

Chunk sizes:
    125, 62.5, 31.25, 15.625 ms

Duration preservation:
    at each join, remove 1 ms from the end of the left chunk and 1 ms
    from the beginning of the right chunk, then insert 2 ms of silence.

RMS matching:
    the final 500-ms waveform, INCLUDING gaps, is matched to the intact
    reference RMS.
"""
from pathlib import Path
import argparse
import numpy as np
from scipy.io import wavfile
from scipy.signal import chirp

FS = 48000
CHUNK_MS = [125.0, 62.5, 31.25, 15.625]

def rms(x):
    return np.sqrt(np.mean(np.asarray(x,float)**2))

def save(path, x):
    wavfile.write(path, FS, np.int16(np.clip(x,-1,1)*32767))

def make_base():
    n = int(0.5*FS)
    t = np.arange(n)/FS
    x = (
        0.45*chirp(t,f0=1200,f1=9000,t1=0.5,method="logarithmic")
        + 0.25*chirp(t,f0=8500,f1=1800,t1=0.5,method="linear")
        + 0.18*np.sin(2*np.pi*(3500*t + 700*np.sin(2*np.pi*3*t)/(2*np.pi)))
    )
    env = 0.35 + 0.65*(0.5
        + 0.28*np.sin(2*np.pi*2.1*t+0.3)
        + 0.17*np.sin(2*np.pi*5.3*t+1.2))
    x *= np.clip(env,0.05,1.0)
    r = int(0.005*FS)
    fade = np.sin(np.linspace(0,np.pi/2,r))**2
    x[:r] *= fade
    x[-r:] *= fade[::-1]
    x /= np.max(np.abs(x))
    x *= 10**(-3/20)
    return x

def nonidentity_perm(n, rng):
    ident = np.arange(n)
    while True:
        p = rng.permutation(ident)
        if not np.array_equal(p, ident):
            return p

def add_gap_exact_total(chunks, gap_ms=2.0):
    half = int(round((gap_ms/2)*FS/1000))
    gap = np.zeros(int(round(gap_ms*FS/1000)))
    parts = []
    for i,ch in enumerate(chunks):
        lo = half if i > 0 else 0
        hi = len(ch)-half if i < len(chunks)-1 else len(ch)
        if i > 0:
            parts.append(gap)
        parts.append(ch[lo:hi])
    return np.concatenate(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", default="demo_gap2ms_RMSmatched")
    ap.add_argument("--seed", type=int, default=20260923)
    args = ap.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    base = make_base()
    target = rms(base)
    save(out/"demo_intact_500ms_RMS_reference.wav", base)

    rng = np.random.default_rng(args.seed)

    for ms in CHUNK_MS:
        cn = int(round(ms*FS/1000))
        chunks = base.reshape(-1,cn)
        order = nonidentity_perm(len(chunks),rng)
        y = add_gap_exact_total(chunks[order],2.0)
        assert len(y) == len(base)
        y *= target/rms(y)

        tag = str(ms).replace(".","p")
        save(out/f"demo_scrambled_{tag}ms_gap2ms_total500ms_RMSmatched.wav",y)
        print(ms,"ms:",order.tolist(),"RMS=",rms(y))

if __name__ == "__main__":
    main()
