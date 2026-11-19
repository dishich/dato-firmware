#!/usr/bin/env python3
"""Render original Dato DRUM one-shots from oscillators and filtered noise."""
import argparse
from itertools import product
from pathlib import Path
import wave

import numpy as np
from scipy import signal

RATE = 44100

def noise_band(rng, t, low, high):
    raw = rng.standard_normal(len(t))
    filtered = signal.sosfilt(signal.butter(2, (low, high), 'bandpass', fs=RATE, output='sos'), raw)
    return filtered / max(np.std(filtered), 1e-9)

def one_shot(track, index, organic, rng):
    t = np.arange(round(RATE * (.26 + .061 * index if track == 0 else .29 + .045 * index))) / RATE
    tail = (.049 + .010 * index)
    if track == 0:
        f = [38.89,38.89,46.25,46.25,51.91,51.91,58.27,58.27][index]
        drop = .007 + .002 * (index % 4)
        phase = 2*np.pi*(f*t + (117 if organic else 156)*drop*(-np.expm1(-t/drop)))
        audio = .91 * np.sin(phase) * np.exp(-t / (tail * 2.6))
        audio += .07*np.sin(phase*2.01)*np.exp(-t/.026)
        audio += (.032 if organic else .062)*noise_band(rng,t,1100,5900)*np.exp(-t/.008)
    elif track == 1:
        hits = (.0, .010, .022) if index < 5 else (.0, .004)
        shape = sum(np.where(t >= hit, np.exp(-np.maximum(t-hit,0)/(.004+index*.0015)),0) for hit in hits)
        edge = np.exp(-t/(tail*(1.05 if organic else .72)))
        audio = noise_band(rng,t,500+130*index,4800+400*index) * (.56*shape+.32*edge)
        audio += (.27 if index>=5 else .09)*np.sin(2*np.pi*(167+17*index)*t)*np.exp(-t/.046)
    elif track == 2:
        f = [77.78,92.50,103.83,155.56,207.65,233.08,311.13,466.16][index]
        intervals = (1,1.59,2.14,3.02) if organic else (1,2.03,2.59,4.41)
        audio = sum(np.sin(2*np.pi*f*ratio*t)*np.exp(-t/(tail/(1+j*.68)))/(1+j*.9)
                    for j,ratio in enumerate(intervals))
        audio += .11 * noise_band(rng,t,700,4200)*np.exp(-t/.012)
    else:
        tail *= (.50 if index < 4 else 1.40)
        audio = noise_band(rng,t,3900+index*270,11700+index*370)*np.exp(-t/tail)
        if organic:
            audio *= .71 + .29*np.sin(2*np.pi*(43+index*7)*t+.3)
            audio += .18*noise_band(rng,t,1300,4500)*np.exp(-t/(tail*.54))
        else:
            audio += .10*np.sign(np.sin(2*np.pi*(6180+index*155)*t))*np.exp(-t/(tail*.50))
    audio[:22] *= np.linspace(0,1,22)
    audio[-441:] *= (.5+.5*np.cos(np.linspace(0,np.pi,441)))
    audio /= np.abs(audio).max()
    return audio * (.55,.33,.30,.22)[track]

def build(out, bank, start, organic):
    rng = np.random.default_rng(662 + start)
    sounds = [[one_shot(track,i,organic,rng) for i in range(8)] for track in range(4)]
    max_len = max(len(x) for track in sounds for x in track)
    padded = [[np.pad(x,(0,max_len-len(x))) for x in track] for track in sounds]
    worst = max(np.abs(sum(combo)).max() for combo in product(*padded))
    gain = min(1, .88 / worst)
    directory = out / bank
    directory.mkdir(parents=True, exist_ok=False)
    names = ('kick','clap-snare','tom-perc','hat-shaker')
    for track, family in enumerate(sounds):
        for i, audio in enumerate(family):
            slot = start+8*track+i
            with wave.open(str(directory / f'{slot}_{names[track]}-{i+1:02}.wav'),'wb') as w:
                w.setparams((1,2,RATE,0,'NONE',''))
                w.writeframes(np.round(audio*gain*32767).astype('<i2').tobytes())
    print(f'{bank} slots {start}–{start+31}, verified worst normalized four-hit peak {worst*gain:.3f}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    out = parser.parse_args().output
    if out.exists():
        parser.error('Use a new output directory')
    build(out,'Techno',30,False)
    build(out,'Organic',62,True)
