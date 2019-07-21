# Solving a question about SET with a SAT-solver

**SET** is the game with the cards with the colored shapes:

![Three SET cards](https://upload.wikimedia.org/wikipedia/commons/8/8f/Set-game-cards.png)

Each card has four features, namely color, shape, fill, and quantity. Each of
these features have three possible values. For instance, a card can be red,
green, or purple. A SET is three cards where, for each attribute, either all of
the cards match or none of them do. For more information, consult the rules at
[setgame.com](https://www.setgame.com/).

The game is played with twelve cards on the table. However, there is not always
a SET in any twelve cards, so more cards are sometimes necessary. This leads to
a classic question: How many cards can be on the table without there being a SET
among them?

[Knuth solved this](https://www-cs-faculty.stanford.edu/~knuth/programs.html)
in 2001. And it turns out that a maximum of 20 out of the total 81 cards can be
on the table without there being a SET.

I wanted to find a set of 20 cards containing no SET among them, and I wanted to
do it in a novel way&mdash;by encoding this problem as a *boolean satisfiability
problem* and using a SAT solver to find the result.

I was inspired by several online articles describing how to solve sudoku with
a SAT solver.

My program outputs a
[CNF](https://en.wikipedia.org/wiki/Conjunctive_normal_form) that asserts the
following:

1. There are no SETs among the cards "on the table"
2. There are at least `k` cards "on the table"
3. There are certain specific cards "on the table"

Point 1 is fairly easy to encode. There are only 1080 possible sets, so I can
directly forbid these with one clause each. Note that the first 81 variables in
the CNF each represent whether a card is "on the table" or not. For every three
cards which form a SET, at least one of their corresponding variables must be
set to `false`.

Point 2 is more difficult to encode, because there is no direct way to add
so-called *cardinality constraints* to a SAT problem (i.e. at most/least this
many variables must be `true`). I consulted the paper
"SAT Encodings of the At-Most-k Constraint" by Alan M. Frisch and Paul A.
Giannaros. I used a modified version of their *Sequential Counter Encoding* in
my code. This introduces many extra variables whose purpose is to "count" the
number of card-variables set to `true`. These truth values can be ignored in the
final result, because they do not represent cards like the first 81 variables
do.

Point 3 is not strictly necessary, but it does improve performance by
eliminating a fair number of isomorphic solutions (See Knuth for more
discussion on this). I simply fix three arbitrary cards to be true that do not
form a set. If you come up with a cleverer way of eliminating these
isomorphisms, please let me know.

To use:

```
$ python3 satcnf.py > set.DIMACS
$ minisat set.DIMACS out.txt
```

It takes minisat about 0.08 seconds to find a satisfying assignment on my
laptop. If I increase `k` to 21, it takes minisat about an hour to find `UNSAT`.
