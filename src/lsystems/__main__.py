from lsystems.sentences.string import String
from lsystems.sentences.tuple import Tuple
from lsystems.productions.static import Static
from lsystems.productions.stocastic import Stochastic
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate

## Example 1

# Start symbol
sentence = String("X")

# Productions (deterministic)
productions = Productions(String)
productions.add("X", Static(String("F+[[X]-X]-F[-FX]+X")))
productions.add("F", Static(String("FF")))

# Alphabet includes every symbol we might emit
alphabet = set("FX+-[]")

lsys = LSystem(alphabet, productions, sentence)

gen = Generate(lsys, depth=2)
result = gen.run()

print(result)
print(result == "FF+[[F+[[X]-X]-F[-FX]+X]-F+[[X]-X]-F[-FX]+X]-FF[-FFF+[[X]-X]-F[-FX]+X]+F+[[X]-X]-F[-FX]+X")

from lsystems.sentences.string import String
from lsystems.productions.static import Static
from lsystems.productions.stocastic import Stochastic
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate, ScopeClasses, RunScope

# ============================================================
# Example 2: stochastic plant-ish branching
# ============================================================

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
gen = Generate(lsys, depth=3)

print("Example 2")
print(gen.run())
print()


# ============================================================
# Example 3: stochastic algae / rewriting toy
# ============================================================

sentence = String("A")

productions = Productions(String)

a_prod = Stochastic()
a_prod.add(10, String("AB"))
a_prod.add(7,  String("BA"))
a_prod.add(5,  String("AA"))
a_prod.add(4,  String("A[B]A"))
a_prod.add(3,  String("A+A"))
a_prod.add(2,  String("A-A"))

b_prod = Stochastic()
b_prod.add(10, String("A"))
b_prod.add(8,  String("BB"))
b_prod.add(6,  String("BA"))
b_prod.add(4,  String("B[A]"))
b_prod.add(3,  String("B+B"))
b_prod.add(2,  String("B-B"))

productions.add("A", a_prod)
productions.add("B", b_prod)

alphabet = set("AB+-[]")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=4)

print("Example 3")
print(gen.run())
print()


# ============================================================
# Example 4: stochastic corridor / geometric doodle
# ============================================================

sentence = String("G")

productions = Productions(String)

g_prod = Stochastic()
g_prod.add(12, String("F+G"))
g_prod.add(10, String("F-G"))
g_prod.add(8,  String("F[+G]"))
g_prod.add(8,  String("F[-G]"))
g_prod.add(6,  String("F[+G][-G]"))
g_prod.add(4,  String("FG"))
g_prod.add(2,  String("G"))

f_prod = Stochastic()
f_prod.add(10, String("FF"))
f_prod.add(7,  String("F"))
f_prod.add(5,  String("F+F"))
f_prod.add(5,  String("F-F"))
f_prod.add(3,  String("F[+F]"))
f_prod.add(3,  String("F[-F]"))

productions.add("G", g_prod)
productions.add("F", f_prod)

alphabet = set("FG+-[]")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=15, seed=None)

print("Example 4")
print(gen.run())
