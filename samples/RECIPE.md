# Rebuild the two sample banks heard in the walkthrough

These are source credits. This demo is not sponsored and the links are not affiliate links.

| Pack | Producer | Used for |
| --- | --- | --- |
| [Melodic Techno Vol.1 Drum Sample Pack](https://www.productionmusiclive.com/products/melodic-techno-vol-1-drum-sample-pack) | François Rengère | Slots 30–61 |
| [Organic House Essentials](https://www.productionmusiclive.com/products/organic-house-essentials) | Felix Raphael | Organic kicks, claps, wood, bongos, glass hats and shakers |
| [Percussive House](https://www.productionmusiclive.com/products/percussive-house-samples-loops-by-florian-busse) | Florian Busse | Additional kicks, clap, snare, bell, percussion and hats |

[All 64 source filenames, roles, target notes, high-pass frequencies and level targets](PML-SLOTS.md). The sample audio belongs to its licensors. Build the demo banks from your own copies under the [PML license](https://www.productionmusiclive.com/pages/pml-licensing-agreement).

### Run the processing locally

Use Python 3.10 or later with NumPy, SciPy and SoundFile in a virtual environment. Give the three pack roots and a **new** output folder. Use the directory that contains the paths shown in the slot table.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install numpy scipy soundfile
python tools/rebuild_pml.py --melodic "/path/to/Melodic Techno Vol.1" --organic "/path/to/Organic House Essentials" --percussive "/path/to/Percussive House" --out "./demo-banks"
```

1. Resample to 44.1 kHz. For stereo, check the energy of the mono average. If it retains less than 75% of the mean channel energy, keep the stronger channel to preserve out-of-phase transients.
2. Remove DC and apply the slot's second-order high-pass. Measure pitched hits and resample to their target note. Stop for review if a shift exceeds 2.6 semitones. Unpitched hats and claps keep their pitch.
3. Trim silence, preserve a short lead-in and limit each hit to 39,690 frames (0.9 s). Fade in over 13 samples. Fade uncut tails over 6 ms and capped tails over 150 ms.
4. Set each hit's level by role using its strongest 100 ms K-weighted window. If a peak exceeds its track ceiling, apply bounded soft shaping. Techno permits up to 4 dB additional drive, Organic up to 3 dB. This happens offline in sample preparation.
5. Sum all 4,096 combinations of one hit per track at velocity 100. Reduce each bank as a whole to keep its worst summed peak at or below 0.88 full scale. Reference gain was −4.57 dB for Techno and −5.15 dB for Organic. Export dithered PCM16 WAV. Other velocities, pitch settings and patterns can change playback peaks.

[Install the finished banks](../docs/INSTALL.md). The separate original kit asset was generated entirely from oscillators and noise. It can be used directly without buying any packs.
