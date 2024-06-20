# Galveston

An experimental engine and assembler for interactive ω-word games.

Galveston is an ω-language over the alphabet `Σ = {NUL, v1, v2, ...}`. A program in Galveston is a single ω-word from that language,
 i.e. a countably infinite sequence made up of symbols from a countably infinite totally-ordered alphabet.

The only fixed symbol in the alphabet `Σ` is the 0 indexed `NUL` character, `v0` / `\x00` / ␀ (visual). The remaining characters may be interpreted in any way convenient. A practical convention is to use ASCII and its superset Unicode to occupy the initial slots of this infinite alphabet, but it is not strictly required by the specification.

The concept of this language was inspired by Choose-your-own-Adventure style game books, and as such it may have some practical application as an interactive fiction engine.

* [galveston.py](galveston.py) : ω-word explorer / engine.
* [galvasm.py](galvasm.py): ω-word assembler.


## Galveston asm

Ignoring ω-languages and the compiled binary format, this can be thought of as a simple interactive fiction engine with the following notation:

* `[:label:]` Label / paragraph marker
* `(:label:)` Output the numeric (decimal) value of the label/paragraph to the player
* `{JMP}{:label:}` Jump to label / paragraph
* `{NUL}` Wait for player input
* `{LF}` The linefeed symbol to add a line break

`:label:` can be any string, excluding the reserved words `NUL`, `JMP`, `LF`, made from capital letters: `A–Z`, digits: `0–9`, and the underscore character: `_`.

This [small escape room example](examples/asm/small-room.gasm) demonstrates the syntax.

The symbolic representation of a Galveston game, like any other text based fiction laid out in a sequence, can be thought of as the output of a mathematical function on the set of natural numbers (i.e. the definition of a mathematical sequence).

It differs in that it adheres to this mathematical analogy far beyond what is necessary or sensible for the purpose of gameplay: every game can be thought of as an infite string over a (potentially) infinte alphabet of symbols. This is required because every input in ℕ must produce an output, also ∈ ℕ, which must be considered as a single 'symbol'. The jump convention requires that there is a symbol for every potential output in ℕ, hence the full alphabet of Galveston is countably infinite too. These considerations of infinity do not generally affect gameplay, and the particulr issues of infinite file sizes and infinite symbol representations are glossed over by various conventions.

Playing a game involves traversing the sequence quasi-linearly, using the output of `y = 0` bounded segments to make choices about the next input value to the function.

This does mean that any practical Galveston compiler or interpreter probably cannot process _all_ valid Galveston strings, since not all can be readily represented in digital form. Again, this should be a practical problem for standard interactive fiction.

In other words: it's a low capability interactive fiction engine hidden within a mathematical toy.

## Usage

View the help:

```
usage: galveston.py [-h] [--omega] file

Galveston (v0.2α)

Still climbing after knowledge infinite,
And always moving as the restless spheres,
Will us to wear ourselves, and never rest,
Until we reach the ripest fruit of all, 
That perfect bliss and sole felicity, 
The sweet fruition of an earthly crown.
    — Marlowe

positional arguments:
  file             Galveston source [.glv|.glv.gz]

options:
  -h, --help       show this help message and exit
  --omega, -ω, -O  Read past EOF indefinitely
```

Play the short escape room example:

    ./galveston.py examples/small-room.glv

"Play" the short non-branching story, A Little Fable, by Franz Kafka:

    ./galveston.py examples/little-fable.glv

Compile and "play" a fable by Aesop, in ancient Greek:

    ./galveston.py <(./galvasm.py examples/asm/Aesopus135.gasm)

Play a pre-compiled and compressed version of a Choose-your-own-adventure gamebook from 1980:

    ./galveston.py examples/chimney_rock.glvz

Participate in a comp-sci-experiment-cum-collaborative-game and prove this is a Turing complete programming language by helping simulate a cyclic tag system:

    ./galveston.py <(./galvasm.py examples/asm/BCT.gasm)  # you 'win' if you get any part of this one.
