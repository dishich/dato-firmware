# Dato DUO + DRUM · dishich music

Two small instruments, one MIDI cable. My custom DUO adds voices for melodic techno and organic house. My DRUM leads the pair, switches kits and lets one track run sixteenths against the others. These are independent community builds tested on my own instruments.

**[Download the firmware and original sample kits](https://github.com/dishich/dato-firmware/releases/latest)** · [Installation and rollback](docs/INSTALL.md) · [Rebuild the exact demo banks](samples/RECIPE.md) · [Instructions for an installation agent](AGENTS.md)

| Instrument | Supported hardware | Download |
| --- | --- | --- |
| Dato DUO | **Brains 1**, NXP Kinetis K20, normal USB ID 1fc9:818a. Brains 2 / i.MX RT uses different firmware. | DUO-Brains-1-1.2.66.bin |
| Dato DRUM | Dato's four-voice RP2350 drum machine, with MIDI firmware update support | DRUM-1.0.1-dishich.uf2 |
| DRUM one-shots | Two optional original synthesized kits, 32 sounds each, mono 44.1 kHz / PCM16 | dishich-original-kits.zip |

**Illustrated field guide** · [English PDF](https://github.com/dishich/dato-firmware/releases/download/v1.2.66/Dato-Field-Guide-EN.pdf) · [Русский PDF](https://github.com/dishich/dato-firmware/releases/download/v1.2.66/Dato-Field-Guide-RU.pdf)

Five pocket pages cover the mode colours, button combinations, per-track sixteenths, live effects and the MIDI connection.

### Play the pair

Connect **DRUM MIDI OUT → DUO MIDI IN** using a 5-pin DIN cable. Set the DUO speed knob near the middle and press Play on DRUM. This gives a 1:1 pulse. Each instrument has its own audio output.

- **DUO voices.** Press both transpose arrows together to cycle Factory (white), Techno (blue, natural minor), Organic (amber, minor pentatonic) and Organic East (pink, harmonic minor). The three custom voices are centred on D♯. Their filter response, delay and space are voiced for live playing.
- **DUO gestures.** With the sequencer stopped, hold Accent and tap a step to accent it. Accent + transpose up switches kick ducking. When playing to the DRUM, holding ×2 adds temporary steps. Release it and the melody comes back to its original place in the bar.
- **DRUM kits.** Press the next-sample buttons on tracks 1 and 2 together to cycle Factory → Techno → Organic. Factory's 32 sounds are embedded. Techno and Organic read editable slots 30–61 and 62–93. Install either the original downloadable samples or the banks rebuilt from the demo recipe.
- **DRUM rhythm.** Press both sample arrows of a single track together to toggle eighths and sixteenths. The filter sends fewer redundant MIDI messages. Sample switching, swing and retrigger handling have also been revised.

### What was checked

We recorded outgoing MIDI from both instruments during live panel gestures. On DUO 1.2.66, the final 186 steps after ×2 and other variations matched the original melody, including its rests. In a dedicated Organic delay pass, all 174 full steps matched and each of 2,094 interior DRUM clock pulses had one DUO response. These measurements describe MIDI timing on one hardware pair. Analog attack timing depends on the sound.

The original downloadable kits are new synthetic alternatives. The demo uses privately prepared PML material. Owners of the three packs can regenerate all 64 demo WAVs locally with the included recipe. On the reference machine their PCM matched all 64 slots read back from the DRUM.

[Source changes and notices](source/README.md) · [dishich music on YouTube](https://www.youtube.com/@dishich) · [Dato support](https://dato.mu/support)
