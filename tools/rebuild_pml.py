#!/usr/bin/env python3
"""Build the two original video banks locally from legally acquired PML WAVs."""
import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

SR = 44_100
CAP = int(0.9 * SR)
CEILINGS = (0.80, 0.56, 0.42, 0.30)
NOTE = {n: i for i, n in enumerate(('C','C#','D','D#','E','F','F#','G','G#','A','A#','B'))}
SLOTS = Path(__file__).resolve().parents[1] / "samples/pml-slots.json"

def hz(name):
    return 440.0 * 2 ** ((NOTE[name[:-1]] + 12 * (int(name[-1]) + 1) - 69) / 12)

def k_weight(x, sr):
    # ITU-R BS.1770: высокочастотная полка +4 дБ и срез низа 38 Гц (коэффициенты под нужную частоту)
    def shelf(f0=1681.97, G=3.99984, Q=0.7071752):
        K = np.tan(np.pi * f0 / sr); Vh = 10 ** (G / 20); Vb = Vh ** 0.4996667741545416
        a0 = 1 + K / Q + K * K
        return [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0], [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    def hp(f0=38.13547, Q=0.5003270):
        K = np.tan(np.pi * f0 / sr); a0 = 1 + K / Q + K * K
        return [1, -2, 1], [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    b, a = shelf(); x = signal.lfilter(b, a, x)
    b, a = hp(); return signal.lfilter(b, a, x)

def load(path):
    d, sr = sf.read(path, always_2d=True)
    if sr != SR:
        d = signal.resample_poly(d, SR, sr, axis=0)
    return d

def to_mono(d):
    if d.shape[1] == 1: return d[:, 0], 1.0
    L, R = d[:, 0], d[:, 1]
    mid = (L + R) / 2; e_mid = np.sum(mid ** 2); e_lr = (np.sum(L ** 2) + np.sum(R ** 2)) / 2
    return mid, float(e_mid / (e_lr + 1e-20))       # 1.0 = сумма в моно ничего не теряет

def trim(m):
    pk = np.abs(m).max()
    idx = np.where(np.abs(m) > pk * 10 ** (-50 / 20))[0]
    a = max(0, idx[0] - 22)                         # полмиллисекунды до первого звука
    idx60 = np.where(np.abs(m) > pk * 10 ** (-60 / 20))[0]
    return m[a:idx60[-1] + 1]

def loud(m):
    k = k_weight(m, SR); win = int(SR * 0.1)
    if len(k) < win: k = np.pad(k, (0, win - len(k)))
    ms = signal.convolve(k ** 2, np.ones(win) / win, mode='valid')
    return float(-0.691 + 10 * np.log10(ms.max() + 1e-20)), float(-0.691 + 10 * np.log10(np.sum(k ** 2) / SR + 1e-20))

def pitch_peak(m, lo=28, hi=140):
    """Тон низкого удара — частота самого сильного пика спектра всего звука. Сверено с тональностями,
    которые производитель указал в именах 20 бочек и томов: в пределах полутона 17 из 20
    (способ по переходам через ноль — 12 из 20)."""
    n = 1 << 18; seg = m * np.hanning(len(m))
    sp = np.abs(np.fft.rfft(seg, n)); fr = np.fft.rfftfreq(n, 1 / SR); band = (fr >= lo) & (fr <= hi)
    i = int(np.argmax(sp * band))
    if i <= 0 or i >= len(sp) - 1: return None
    a, b, c = np.log(sp[i - 1] + 1e-12), np.log(sp[i] + 1e-12), np.log(sp[i + 1] + 1e-12)
    return float(fr[i] + (fr[1] - fr[0]) * 0.5 * (a - c) / (a - 2 * b + c))

def pitch_tonal(m, lo=70, hi=2500):
    """Тон перкуссии: главный пик спектра и то, насколько он выделяется над шумом."""
    n = 1 << 16; seg = m[:min(len(m), int(SR * 0.5))]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n)); fr = np.fft.rfftfreq(n, 1 / SR)
    band = (fr >= lo) & (fr <= hi); i = np.argmax(sp * band)
    if i <= 0 or i >= len(sp) - 1: return None, 0.0
    a, b, c = np.log(sp[i - 1] + 1e-12), np.log(sp[i] + 1e-12), np.log(sp[i + 1] + 1e-12)
    f = fr[i] + (fr[1] - fr[0]) * 0.5 * (a - c) / (a - 2 * b + c)
    near = (fr > f * 0.94) & (fr < f * 1.06)
    prominence = float(np.sum(sp[near] ** 2) / (np.sum(sp[band] ** 2) + 1e-20))   # доля энергии в ±1 полутоне от пика
    return float(f), prominence


def pitch_near(x, target):
    if target < 160:
        result = pitch_peak(x, lo=target * .62, hi=target * 1.6)
        if result:
            return result
    return pitch_tonal(x, lo=target * .75, hi=target * 1.33)[0]

def prepare(path, row, ceiling, max_soften):
    audio = load(path)
    mono, retained = to_mono(audio)
    if retained < .75 and audio.shape[1] > 1:
        mono = audio[:, np.argmax(np.sum(audio ** 2, axis=0))]
    mono = mono - np.mean(mono)
    mono = signal.sosfilt(signal.butter(2, row["highpass"], fs=SR, btype="highpass", output="sos"), mono)
    if row["note"]:
        target = hz(row["note"])
        measured = pitch_near(trim(mono), target)
        if measured:
            shift = 12 * np.log2(target / measured)
            if abs(shift) > 2.6:
                raise ValueError(f"{path.name} needs {shift:+.2f} semitones. Check the input file.")
            ratio = Fraction(measured / target).limit_denominator(2000)
            mono = signal.resample_poly(mono, ratio.numerator, ratio.denominator)
    mono = trim(mono)
    truncated = len(mono) > CAP
    mono = mono[:CAP].copy()
    attack = min(len(mono), 13)
    mono[:attack] *= np.linspace(0, 1, attack)
    tail = min(len(mono), int(SR * (.15 if truncated else .006)))
    mono[-tail:] *= .5 * (1 + np.cos(np.linspace(0, np.pi, tail)))
    mono = mono / np.abs(mono).max()
    gain = 10 ** ((row["level"] - loud(mono)[0]) / 20)
    if gain <= ceiling:
        return mono * gain

    def shaped(drive):
        return ceiling * np.tanh(mono * drive / ceiling)

    lo, hi = gain, gain * 10 ** (max_soften / 20)
    for _ in range(30):
        mid = (lo * hi) ** .5
        if loud(shaped(mid))[0] < row["level"]:
            lo = mid
        else:
            hi = mid
    return shaped(hi)

def build(rows, roots, out, max_soften):
    waves = []
    for i, row in enumerate(rows):
        waves.append(prepare(roots[row["pack"]] / row["source"], row, CEILINGS[i // 8], max_soften))
    worst = 0.0
    for hits in itertools.product(waves[:8], waves[8:16], waves[16:24], waves[24:]):
        combined = np.zeros(max(map(len, hits)))
        for hit in hits:
            combined[:len(hit)] += hit
        worst = max(worst, np.abs(combined).max() * (100 / 127))
    gain = min(1.0, .88 / worst)
    out.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(7)
    for row, mono in zip(rows, waves, strict=True):
        mono = mono * gain
        pcm = np.round(mono * 32767 + (rng.random(len(mono)) - rng.random(len(mono)))).clip(-32768, 32767).astype(np.int16)
        sf.write(out / f"{row['slot']}_{row['name']}.wav", pcm, SR, subtype="PCM_16")
    print(f"{out}: 32 WAVs. Whole-bank gain {20*np.log10(gain):+.2f} dB.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("melodic", "organic", "percussive", "out"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    roots = vars(args)
    manifest = json.loads(SLOTS.read_text())
    missing = [roots[r["pack"]] / r["source"] for r in manifest if not (roots[r["pack"]] / r["source"]).is_file()]
    if missing:
        parser.error("Check the three pack roots. Missing WAVs:\n" + "\n".join(map(str, missing)))
    if args.out.exists():
        parser.error("--out must be a new directory")
    build(manifest[:32], roots, args.out / "Techno", 4)
    build(manifest[32:], roots, args.out / "Organic", 3)

if __name__ == "__main__":
    main()
