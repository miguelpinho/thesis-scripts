# Thesis scripts

Set of scripts to automate running simulations on gem5.

Currently functional:

- Splash-2 benchmarks (most of them)
- some PARSEC-3.0 benchmarks
- at least two SPEC2006 (probably several more)

Todo:

[ ] improve README
[ ] refactor script set (so much redundant code for now...)
[x] automatically fetch date
[ ] find a cleaner way to get all script names (argfile? ``parallel`` is very
useful for [this](https://www.gnu.org/software/parallel/parallel_tutorial.html#Linking-arguments-from-input-sources)
