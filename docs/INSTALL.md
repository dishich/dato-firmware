# Install and recover

Download the assets for your instrument from the [release](https://github.com/dishich/dato-firmware/releases/latest). Keep its SHA256SUMS file alongside them. Compare each downloaded file with its entry using `shasum -a 256 FILENAME` on macOS or `sha256sum FILENAME` on Linux. The procedure below was exercised on macOS. Connect one unit of the model being updated at a time with a data-capable USB cable. Keep power connected through the write.

## DUO Brains 1 only

1. Check the **normal-mode USB identity 1fc9:818a** before touching the update button. On macOS look in System Information → USB, or use `system_profiler SPUSBDataType`. On Linux use `lsusb`. A Brains 2 or an unidentified board must use its own manufacturer guidance. Record any pattern you want to recreate after restart.
2. Install dfu-util (macOS: `brew install dfu-util`). Enter the original DUO bootloader using the recessed update button beside the headphone socket. Run `dfu-util -l`. Expect exactly one target with ID **1fc9:8189**.
3. In the download directory run `dfu-util -d 1fc9:8189 -D DUO-Brains-1-1.2.66.bin`. Wait for transfer and manifestation to finish. The normal MIDI port reappears on restart. Sending MIDI SysEx `F0 7D 64 01 F7` should return `F0 7D 64 01 02 42 F7` (1.2.66).
4. For rollback, download the official Brains 1 binary and repeat the same DFU procedure using its filename. [Official DUO release](https://github.com/datomusic/duo-firmware/releases/tag/v1.2.0-rc.1)

## Dato DRUM

Start from a unit supporting firmware and sample transfer over USB MIDI. If an older stock unit cannot answer the transfer commands, first consult the [official DRUM release](https://github.com/datomusic/drum-firmware/releases/tag/v1.0.1). The regular application update targets the inactive firmware partition. Factory images and filesystem formatting are separate operations.

Install Node.js, npm and the native build tools required by the upstream MIDI package. From your project folder:

```sh
git clone --branch v1.0.1 https://github.com/datomusic/drum-firmware.git dato-upstream
cd dato-upstream
npm install
cd tools/drumtool
node drumtool.js identity
node drumtool.js version
node drumtool.js receive --all backup-samples
```

Verify the backups and record your pattern and settings before updating. With DRUM stopped:

```sh
node drumtool.js flash /absolute/path/to/DRUM-1.0.1-dishich.uf2
```

Wait for the device to restart. The version query still reports the 1.0.1 base. To verify the custom build, use the two-track next-sample chord and listen for the embedded Factory sounds. For firmware rollback, flash Dato's regular **drum-1.0.1.uf2** using the same command. Restore your saved samples to their original slots if you replaced them.

## Load either pair of kits

Unzip the original kit asset, or run the [demo recipe](../samples/RECIPE.md). Both produce Techno and Organic folders with the slot in each filename. **Sending these files overwrites slots 30–93.** Preview a WAV and confirm your backups before transfer. From the drumtool directory, use the helper in this repository. By default it prints the transfers. Add `--write` to perform them.

```sh
python3 /path/to/dato-firmware/tools/load_kits.py /path/to/unpacked-kits
```

After loading, audition each bank. To verify the transfers, use `node drumtool.js receive 30-93 verify-samples` and compare decoded mono PCM against the source files. Select Factory with the bank chord to play the embedded kit again.
