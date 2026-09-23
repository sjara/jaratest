#!/usr/bin/env python3
"""
Generate a 500-ms 1/f AM/FM dynamic tone complex and scrambled versions with:
  * nominal chunk scales: 125, 62.5, 31.25, 15.625 ms
  * 2-ms silence at every internal join
  * exact 500-ms onset-to-offset duration
  * RMS matched to the intact 500-ms reference over the full waveform,
    including the silent gaps.

To keep total duration at exactly 500 ms WITHOUT time-stretching:
each 2-ms join replaces 2 ms of waveform with silence by trimming 1 ms from
the end of the left chunk and 1 ms from the beginning of the right chunk.
"""

from pathlib import Path
import argparse
import numpy as np
from scipy.io import wavfile

F0S = np.array([4000,5040,6350,8000,10080,12700,16000,20160,25400,32000], float)
CHUNK_MS = [125.0,62.5,31.25,15.625]

def one_over_f_process(n, fs, fmin, fmax, gamma, rng):
    f = np.fft.rfftfreq(n, 1/fs)
    z = np.zeros(f.size, complex)
    keep = (f >= fmin) & (f <= fmax)
    phase = rng.uniform(0, 2*np.pi, keep.sum())
    z[keep] = f[keep]**(-gamma/2) * np.exp(1j*phase)
    x = np.fft.irfft(z, n=n)
    return 2*(x-x.min())/(x.max()-x.min()) - 1

def rms(x):
    return np.sqrt(np.mean(np.asarray(x,float)**2))

def save(path, fs, x):
    wavfile.write(path, fs, np.int16(np.clip(x,-1,1)*32767))

def nonidentity_perm(n, rng):
    ident = np.arange(n)
    while True:
        p = rng.permutation(ident)
        if not np.array_equal(p, ident):
            return p

def gap_exact_500(chunks, fs, gap_ms=2.0):
    half = int(round((gap_ms/2)*fs/1000))
    gap = np.zeros(int(round(gap_ms*fs/1000)))
    parts = []
    for i, ch in enumerate(chunks):
        lo = half if i > 0 else 0
        hi = len(ch)-half if i < len(chunks)-1 else len(ch)
        if i > 0:
            parts.append(gap)
        parts.append(ch[lo:hi])
    return np.concatenate(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", default="one_over_f_gap2ms_500ms")
    ap.add_argument("--seed", type=int, default=20260923)
    args = ap.parse_args()

    fs = 192000
    n = int(0.5*fs)
    rng = np.random.default_rng(args.seed)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    a = one_over_f_process(n,fs,2,80,1,rng)
    q = one_over_f_process(n,fs,2,80,1,rng)

    A = 10**((10*a)/20)
    shift = 0.30*q
    p0 = rng.uniform(0,2*np.pi,len(F0S))

    comps = []
    for f0, ph0 in zip(F0S,p0):
        f = f0*2**shift
        phase = ph0 + 2*np.pi*np.cumsum(f)/fs
        comps.append(np.sin(phase))

    s = A*np.sum(comps,axis=0)/np.sqrt(len(comps))

    nr = int(round(0.005*fs))
    r = np.sin(np.linspace(0,np.pi/2,nr))**2
    s[:nr] *= r
    s[-nr:] *= r[::-1]

    s /= np.max(np.abs(s))
    s *= 10**(-6/20)
    target_rms = rms(s)
    save(out/"base_1overf_naturalistic_500ms_RMS_reference.wav",fs,s)

    for ms in CHUNK_MS:
        cn = int(round(ms*fs/1000))
        chunks = s.reshape(-1,cn)
        order = nonidentity_perm(len(chunks),rng)
        y = gap_exact_500(chunks[order],fs,2.0)

        assert len(y) == len(s)
        y *= target_rms/rms(y)

        tag = str(ms).replace(".","p")
        save(out/f"scrambled_{tag}ms_gap2ms_total500ms_RMSmatched.wav",fs,y)
        print(ms,"ms order=",order.tolist(),
              "duration_ms=",len(y)/fs*1000,
              "RMS=",rms(y))

if __name__ == "__main__":
    main()
