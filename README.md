# Galveston

An experimental engine and compiler for interactive ω-word games.

Galveston is an ω-language over the alphabet `Σ = {NUL, v1, v2, ...}`. A program in Galveston is a single ω-word from that language,
 i.e. a countably infinite sequence made up of symbols from a countably infinite totally-ordered alphabet.

The only fixed symbol in the alphabet `Σ` is the 0 indexed `NUL` character, `v0` / `\x00` / ␀ (visual). The remaining characters may be interpreted in any way convenient. A practical convention is to use ASCII and its superset Unicode to occupy the initial slots of this infinite alphabet, but it is not strictly required by the specification.

The concept of this language was inspired by Choose-your-own-Adventure style game books, and as such it may have some practical application as an interactive fiction engine.

* [galveston.py](galveston.py) : ω-word explorer / engine.
* [galvasm.py](galvasm.py): ω-word assembler.

