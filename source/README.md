# Corresponding source

Apply each patch to a clean checkout of the specified public commit using git apply. Upstream repositories contain their original licenses, submodule pointers and build instructions.

- [DUO](https://github.com/datomusic/duo-firmware/tree/cbcb2986a7cd4cc2bb6318708f83a78493f4fc02) — initialize submodules recursively, apply duo.patch at the repository root, then apply duo-audio.patch inside libraries/Audio at 9c50f4649d8562a9719839739d0610786046fe62. Build using the supplied Makefile and ARM GCC 10.3.1. The target is duo-firmware.bin.
- [DRUM](https://github.com/datomusic/drum-firmware/tree/ddbab7b9be34911e55c65730ca0343607550f703) — initialize submodules recursively and apply drum.patch at the root. The factory PCM is generated from the upstream samples/factory_kit files during compilation. Consult the upstream build instructions and select build-only when working without a device.

Credits go to Dato, David Menting, PJRC and the authors of the upstream libraries. See the included notices and each upstream dependency for its terms.
