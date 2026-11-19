# Assist an owner with the Dato release

Start in read-only mode. Do not flash while checking compatibility. Show the owner the observed normal-mode hardware or USB identity, supported board, exact image and checksum, and backup and recovery paths. An AI guess or a product name alone is insufficient. If any item is unknown, stop. Request the owner's separate authorization for the actual write after the evidence is clear.

Ask which instrument and sounds the owner wants. Read README.md and docs/INSTALL.md. Identify the connected hardware in normal mode and verify the release checksum before proposing a write. A DUO Brains 2 needs different firmware. Keep the user's current pattern, settings and samples recoverable.

For the exact video banks, ask the owner for local directories containing the three purchased PML packs. Use samples/PML-SLOTS.md and tools/rebuild_pml.py with a new local output directory. Check all 64 WAVs against samples/pcm-sha256.txt (SHA-256 of the PCM data, excluding WAV headers). Report missing files or mismatches by slot. Keep the licensed source and rendered audio local. The public synthetic kit is ready for owners who want an alternative.

Run the transfer helper in preview mode. Explain which slots will be overwritten and confirm that a usable backup exists. After the owner authorizes writing, install only the selected image or banks. Verify USB identity on restart, audition Factory and the selected kit, and read back the written slots. Never format the device as part of this installation.
