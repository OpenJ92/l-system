# lsystems

A small, compositional Python library for defining and generating **L-systems**.

This project is built around a simple idea:

- a **sentence** is an iterable monoidal container of symbols,
- a **production** rewrites one symbol into a new sentence,
- a **generator** applies productions across generations,
- and a **scope system** carries contextual information into each rewrite.

The result is a compact framework for deterministic and stochastic rewriting that is already useful for procedural generation, grammar experiments, and generative art pipelines.

## Current status

Implemented now:

- deterministic productions
- stochastic productions
- generic sentence protocol
- string-backed and tuple-backed sentence types
- scoped generation with run / generation / position context
- fallback identity rewrites for symbols without explicit productions

Planned next:

- context-sensitive productions
- additional production types
- interpreters (for example turtle or geometry backends)
- richer reproducible randomness via scoped RNGs
- tests and more examples

## Why this project exists

Most L-system examples are written as one-off scripts over strings. That is fine for a toy system, but it becomes limiting when you want to:

- swap out the underlying sentence representation,
- attach contextual information to rewrites,
- mix deterministic and stochastic rules,
- experiment with non-string symbol types,
- or treat rewriting as part of a larger compositional system.

`lsystems` tries to keep the core model small while making those extensions natural.

## Design overview

The package is centered on four concepts.

### 1. `Sentence`

A sentence is any type that behaves like an iterable sequence of symbols and supports a monoidal interface:

- `empty()`
- `lift(symbol)`
- `combine(other)`
- `clone()`

This lets the generator stay generic. A rewrite step does not care whether it is operating on a `str`, a `tuple`, or some future structured sentence type.

Currently included:

- `lsystems.sentences.string.String`
- `lsystems.sentences.tuple.Tuple`

### 2. `Production`

A production is anything callable with the shape:

```python
production(symbol, scope) -> Sentence
```

This is intentionally minimal. It means a production can be:

- a constant rewrite,
- a stochastic chooser,
- a context-sensitive rule,
- a parametric rule,
- or a production that inspects the current run, generation, or position.

### 3. `Productions`

`Productions` stores the mapping from symbols to production objects.

If a symbol has no registered production, the system falls back to an identity-style rewrite by lifting the symbol back into the sentence type. In other words, unspecified symbols persist automatically.

### 4. `Generate`

`Generate` performs the derivation over a fixed number of generations.

For each generation:

1. iterate through the current sentence,
2. retrieve the production for each symbol,
3. build a `ScopeBundle` for that symbol,
4. rewrite each symbol into a sentence,
5. combine all rewrites into the next sentence.

This makes the derivation pipeline explicit and easy to extend.

## Package layout

```text
src/lsystems/
├── __main__.py
├── generate.py
├── lsystem.py
├── productions/
│   ├── productions.py
│   ├── static.py
│   └── stocastic.py
├── protocols/
│   ├── production.py
│   └── sentence.py
└── sentences/
    ├── string.py
    └── tuple.py
```

### Important modules

- `lsystems.lsystem.LSystem`  
  Holds the alphabet, productions, and starting sentence.

- `lsystems.generate.Generate`  
  Executes the rewriting process.

- `lsystems.productions.static.Static`  
  Deterministic production that always returns the same sentence.

- `lsystems.productions.stocastic.Stochastic`  
  Weighted stochastic production.

- `lsystems.productions.productions.Productions`  
  Symbol-to-production registry with default identity lifting.

## Installation

From the project root:

```bash
pip install .
```

For development:

```bash
pip install -e .[dev]
```

The package currently targets Python 3.14+ as declared in `pyproject.toml`.

## Quick start

### Deterministic example

```python
from lsystems.sentences.string import String
from lsystems.productions.static import Static
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate

sentence = String("X")

productions = Productions(String)
productions.add("X", Static(String("F+[[X]-X]-F[-FX]+X")))
productions.add("F", Static(String("FF")))

alphabet = set("FX+-[]")
lsys = LSystem(alphabet, productions, sentence)

result = Generate(lsys, depth=2).run()
print(result)
```

This is the classic shape of an L-system:

- start from an axiom,
- define symbol rewrites,
- iterate for a fixed depth,
- inspect the generated sentence.

### What happens to symbols without a rule?

They are preserved automatically.

That means symbols such as `+`, `-`, `[`, and `]` do not need explicit productions unless you want them rewritten. `Productions.get()` falls back to lifting the current symbol into the sentence type.

## Stochastic productions

The library already includes weighted stochastic rewriting.

```python
from lsystems.sentences.string import String
from lsystems.productions.stocastic import Stochastic
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate

sentence = String("X")
productions = Productions(String)

x_prod = Stochastic()
x_prod.add(10, String("F[+X]F[-X]+X"))
x_prod.add(8,  String("F[-X]F[+X]-X"))
x_prod.add(6,  String("F[+X]-X"))
x_prod.add(6,  String("F[-X]+X"))
x_prod.add(4,  String("F[X]+X"))
x_prod.add(3,  String("F[-X]-X"))
x_prod.add(2,  String("FX"))

f_prod = Stochastic()
f_prod.add(12, String("FF"))
f_prod.add(6,  String("F"))
f_prod.add(4,  String("F+F"))
f_prod.add(4,  String("F-F"))
f_prod.add(2,  String("FF[+F]"))
f_prod.add(2,  String("FF[-F]"))

productions.add("X", x_prod)
productions.add("F", f_prod)

alphabet = set("FX+-[]")
lsys = LSystem(alphabet, productions, sentence)

result = Generate(lsys, depth=3).run()
print(result)
```

### How stochastic selection works

`Stochastic` stores a histogram compactly using cumulative cutoffs rather than expanding weights into a giant repeated list.

So instead of this inefficient idea:

```python
["A", "A", "A", "B", "B", "C", ...]
```

it stores something closer to:

```python
cutoffs = [3, 5, 9, ...]
```

and samples by:

1. drawing a random integer in `[0, total)`,
2. locating the matching cutoff with `bisect`.

That keeps memory usage proportional to the number of alternatives, not the total weight mass.

## Scope system

One of the most interesting parts of the project is the scope model in `generate.py`.

Every production receives a `ScopeBundle` containing:

- `run` scope
- `generation` scope
- `position` scope

### `RunScope`

Created once for the full derivation.

Current fields:

- `name`
- `lsystem`

### `GenerationScope`

Created once per generation.

Current fields:

- `depth`
- `generation`
- `sentence`

### `PositionScope`

Created once per symbol.

Current fields:

- `index`
- `symbol`

### Why this matters

This gives productions access to context without hardwiring context sensitivity into the entire engine.

Examples of future use:

- position-based variation,
- generation-based parameter decay,
- run-level seeded randomness,
- neighborhood inspection for context-sensitive rules,
- structured symbol metadata.

The scope system is the main reason this project is more than a string rewriting script.

## Custom scopes

`Generate` accepts a `ScopeClasses` object, so you can swap the concrete scope types.

That means you can extend the runtime context without changing the rewriting loop itself.

For example, a future seeded implementation could attach:

- a shared RNG at run scope,
- derived RNG streams at generation or position scope,
- external environment data,
- rendering state.

This is a strong extension point for procedural art and simulation use cases.

## Sentence types

### `String`

`String` is the most familiar representation and is great for classic symbolic L-systems.

```python
from lsystems.sentences.string import String

s = String("AB")
t = String("CD")
print(s.combine(t))  # "ABCD"
```

### `Tuple`

`Tuple` is useful when your symbols are not best represented as characters.

You can use richer hashable symbols and still reuse the same generation machinery.

```python
from lsystems.sentences.tuple import Tuple

sentence = Tuple(("A", "B", "C"))
```

This becomes especially important once you move toward:

- parametric symbols,
- structured tokens,
- parser-assisted productions,
- geometry or command tuples.

## Identity fallback behavior

A useful property of the current design is that you only need to define productions for symbols that actually rewrite.

For example:

```python
productions.add("F", Static(String("FF")))
```

and nothing for `+`, `-`, `[`, or `]`.

Those symbols remain present because the default production is effectively:

```python
lambda symbol, scope: sentence_type.lift(symbol)
```

This is elegant and keeps grammars concise.

## Example: tuple-backed symbols

Here is the same style of system using tuple symbols instead of characters.

```python
from lsystems.sentences.tuple import Tuple
from lsystems.productions.static import Static
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate

sentence = Tuple(("A",))
productions = Productions(Tuple)
productions.add("A", Static(Tuple(("A", "B"))))
productions.add("B", Static(Tuple(("A",))))

alphabet = {"A", "B"}
lsys = LSystem(alphabet, productions, sentence)

result = Generate(lsys, depth=5).run()
print(result)
```

The generator logic stays exactly the same.

## Roadmap

### Next priority: context-sensitive productions

This is the natural next feature.

The current scope design already points toward it. A context-sensitive production should be able to inspect information around the current symbol and decide whether or how to rewrite.

There are at least two strong directions here:

#### 1. Neighbor-aware scope

Extend `PositionScope` or `ScopeBundle` so productions can inspect left / right context.

For example, a rule like:

```text
A < B > C  ->  X
```

could be implemented by checking the surrounding symbols of the current `B`.

#### 2. Parser-based matching

Instead of treating context as direct indexing only, use parser-style or zipper-style matching to describe local rewrite environments more compositionally.

That path is especially interesting if this project later interfaces with your broader typeclass / parser work.

### Other likely production types

After context sensitivity, good additions would be:

- conditional productions
- parametric productions
- callable function productions
- probabilistic productions with seeded RNG support
- productions over structured symbol objects

## Planned seeded randomness

Right now `Stochastic` samples using the standard library RNG directly.

The likely direction is to move seeded randomness into the generation scopes rather than the production instance itself.

Why that is attractive:

- a seed can control the entire derivation,
- multiple stochastic productions can share one run-level random process,
- generation- or position-local randomness can later be derived cleanly,
- reproducibility becomes a feature of execution rather than of one isolated rule.

That would fit the current architecture very well.

## Development philosophy

This project seems to be aiming for a sweet spot:

- **small enough** to understand completely,
- **generic enough** to support nontrivial extensions,
- **compositional enough** to connect with larger systems later.

That is a strong direction.

It keeps the core loop legible while leaving room for richer grammars, interpreters, and procedural pipelines.

## Running the examples

There are example snippets in `src/lsystems/__main__.py`.

From the project root, try:

```bash
python -m lsystems
```

Depending on your environment, you may also prefer:

```bash
PYTHONPATH=src python -m lsystems
```

## Known rough edges

This is still early-stage and evolving. A few things are intentionally unfinished or likely to change:

- tests are not written yet,
- context-sensitive rewriting is not implemented yet,
- seeded reproducibility is not wired into generation yet,
- module names and API details may still shift as the design settles.

That said, the core model is already coherent and useful.

## Contributing direction

If you are extending the library, the highest-value next work is probably:

1. context-sensitive productions,
2. reproducible seeded stochastic generation,
3. tests for deterministic and stochastic derivations,
4. richer sentence types and symbol structures,
5. interpreters that consume generated sentences.

## License

See `LICENSE`.

