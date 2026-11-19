# Dato DUO + DRUM · dishich music

> [!CAUTION]
> **BEFORE YOU FLASH: ASK YOUR AI AGENT TO VERIFY THIS FILE FITS YOUR EXACT DEVICE.**
> A wrong firmware image can leave your instrument unable to start. Ask for a **read-only compatibility check first**. Have the agent show you the detected model and board or USB identity, the exact release filename, and its SHA-256 match. Confirm those findings against the [installation guide](https://github.com/dishich/dato-firmware/blob/main/docs/INSTALL.md) and [Dato support](https://dato.mu/support/).
>
> **DUO** — Brains 1 / Kinetis K20 only. Confirm normal USB ID `1fc9:818a` before entering the bootloader. A Brains 2 / i.MX RT needs different firmware. **DRUM** — Dato DRUM RP2350 with USB-MIDI firmware update support. Identify it with drumtool first. If the hardware, checksum or recovery steps are unclear, stop and contact Dato. Back up your sounds and record your pattern before authorizing any write.

Two small instruments, one MIDI cable. My custom DUO adds voices for melodic techno and organic house. My DRUM leads the pair, switches kits and lets one track run sixteenths against the others. These are independent community builds tested on my own instruments.

**[Download the firmware and original sample kits](https://github.com/dishich/dato-firmware/releases/latest)** · [Installation and rollback](docs/INSTALL.md) · [Rebuild the exact demo banks](samples/RECIPE.md) · [Instructions for an installation agent](AGENTS.md)

| Instrument | Supported hardware | Download |
| --- | --- | --- |
| Dato DUO | **Brains 1**, NXP Kinetis K20, normal USB ID 1fc9:818a. Brains 2 / i.MX RT uses different firmware. | DUO-Brains-1-1.2.66.bin |
| Dato DRUM | Dato's four-voice RP2350 drum machine, with MIDI firmware update support | DRUM-1.0.1-dishich.uf2 |
| DRUM one-shots | Two optional original synthesized kits, 32 sounds each, mono 44.1 kHz / PCM16 | dishich-original-kits.zip |

**Illustrated field guide** · [English PDF](https://github.com/dishich/dato-firmware/releases/download/v1.2.66/Dato-Field-Guide-EN.pdf) · [Русский PDF](https://github.com/dishich/dato-firmware/releases/download/v1.2.66/Dato-Field-Guide-RU.pdf)

Six pocket pages start with a hardware check and cover the mode colours, button combinations, per-track sixteenths, live effects and the MIDI connection.

### What the firmware changes

- **Stay together over MIDI.** DRUM leads. Sweeping its filter sends fewer duplicate control messages. Hold ×2 on DUO for a fill, release it and the melody returns to the master's current step.
- **Play 96 drum sounds.** Three banks of 32. Each bank has four tracks with eight sounds per track. Factory's 32 are built into the firmware. The two additional kits supply 64. Set one track to sixteenths while the others hold eighths.

### Play the pair

Connect **DRUM MIDI OUT → DUO MIDI IN** using a 5-pin DIN cable. Set the DUO speed knob near the middle and press Play on DRUM. This gives a 1:1 pulse. Each instrument has its own audio output.

I developed the DUO modes with Claude Fable. I wanted a bass voice for melodic techno and a softer one for organic house, with Armen Miran as a reference. Press both transpose arrows together to move through these four modes.

| DUO mode | What to play and listen for |
| --- | --- |
| Factory · white | Start with the familiar factory pentatonic layout. |
| Techno · blue | Play a held bass note in D♯ natural minor. The filter opens quickly, then falls back while the note is held. The saw is at full level and the dotted-eighth echo has more feedback. |
| Organic · amber | Play a short call and response in D♯ minor pentatonic. The softer attack, quieter saw and fewer repeats leave room for percussion and the reverb tail. |
| Organic East · pink | Play D then D♯ near the top of the keyboard. That half step resolves to the root of D♯ harmonic minor. The oscillators, filter and effects use the same settings as Organic. |

On startup, each custom mode draws from four eight-step patterns. Techno includes a low pulse and a descending line. Organic has a phrase written to answer the bongos. Organic East has its own bass and Hijaz-style phrases. Pressing both transpose arrows during a jam changes the mode and preserves your running sequence.

- **DUO gestures.** With the sequencer stopped, hold Accent and tap a step to accent it. When playing to the DRUM, holding ×2 adds temporary steps. Release it and the melody comes back to its original place in the bar.
- **DRUM kits.** Press the next-sample buttons on tracks 1 and 2 together to cycle Factory → Techno → Organic. Factory's 32 sounds are embedded. Techno and Organic read editable slots 30–61 and 62–93. Install either the original downloadable samples or the banks rebuilt from the demo recipe.
- **DRUM rhythm.** Press both sample arrows of a single track together to toggle eighths and sixteenths. The filter sends fewer redundant MIDI messages. Sample switching, swing and retrigger handling have also been revised.

### Hear the kick sidechain

Connect **DRUM MIDI OUT → DUO MIDI IN**. Play a steady kick and hold a long note on the DUO. Hold **Accent**, tap and release **Transpose ↑**, then release Accent. The keys flash green for on and red for off. The default is off. DUO remembers the setting after power-off.

Kick notes on MIDI channel 10 (notes 30–37) briefly lower the entire dry synth voice. A full-strength hit dips up to **3 dB in Factory and Techno** or **1.5 dB in Organic and Organic East**. Softer hits produce a smaller dip. The delay and reverb keep ringing. Audio from the two instruments can go to separate speakers.

[Play the 16-second sidechain comparison](https://github.com/dishich/dato-firmware/releases/download/v1.2.66/DUO-sidechain-AB.mp4). Listen to the isolated DUO recording at one volume. At 0:00 Organic plays without a trigger, then with the kick trigger at 0:04. Techno repeats the comparison at 0:08 and 0:12. The audio comes from the DUO 1.2.63 bench test. The panel toggle described above is in the released 1.2.66 build.

### What was checked

We recorded outgoing MIDI from both instruments during live panel gestures. On DUO 1.2.66, the final 186 steps after ×2 and other variations matched the original melody, including its rests. In a dedicated Organic delay pass, all 174 full steps matched and each of 2,094 interior DRUM clock pulses had one DUO response. These measurements describe MIDI timing on one hardware pair. Analog attack timing depends on the sound.

The original downloadable kits are new synthetic alternatives. The demo uses privately prepared PML material. Owners of the three packs can regenerate all 64 demo WAVs locally with the included recipe. On the reference machine their PCM matched all 64 slots read back from the DRUM.

[Source changes and notices](source/README.md) · [dishich music on YouTube](https://www.youtube.com/@dishich) · [Dato support](https://dato.mu/support)

### Find dishich

[SoundCloud](https://soundcloud.com/dishich) · [Spotify](https://open.spotify.com/artist/6jK0DQ3ACnUrtGZbe7AJnP) · [Apple Music](https://music.apple.com/us/artist/dishich/1538135274) · [Instagram](https://www.instagram.com/dishich.music/) · [Beatport](https://www.beatport.com/artist/dishich/1006741)
