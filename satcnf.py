# Generates the CNF whose satisfying assignment has the following properties:
# [ 1 ] There is no SET among the variables which are True, where each
#       variable x_1 ... x_81 represents a SET card.
# [ 2 ] There are at least n cards set to True.
#
# We also add the third property:
# [ 3 ] Some of the isomorphisms are eliminated
# This is to increase performance.

import itertools

# This is the minimum number of cards set to True. At 21, the problem is UNSAT.
k = 20

# This is a list of tuples, each containing a single clause's variables.
clauses = []

def add_clause(*args):
    clauses.append(tuple(*args))

features = 4
cards = itertools.product(*[range(3)]*features)
num_cards = 3**features

def is_SET(tup):
    return all(
    (tup[0][x] + tup[1][x] + tup[2][x]) % 3 == 0
    for x
    in range(features))

def card_to_var(tup):
    return 1 + tup[0] + 3*tup[1] + 9*tup[2] + 27*tup[3]

def disallow_SET(tup):
    return tuple(-card_to_var(card) for card in tup)

# [ 1 ]
clauses += [disallow_SET(s)
            for s
            in itertools.combinations(cards, 3)
            if is_SET(s)]

# Now we make a circuit to count the variables that are true, in unary.
# Doing this the naive, combinatorial way would generate a multi-exabyte file.
# This uses a modified version of the Sequential Counter Encoding found in
# the paper "SAT Encodings of the At-Most-k Constraint" by Frisch and Giannaros.

# The variable number for the bitth bit in the cardth register
def register(card, bit):
    return num_cards + card + num_cards * (bit - 1)

# [ 2.1 ]
add_clause((1, -register(1,1)))

# [ 2.2 ]
for j in range(2, k + 1):
    add_clause((-register(1, j),))

# [ 2.3 ]
for i in range(2, num_cards + 1):
    add_clause((-register(i, 1), register(i-1, 1), i))

# [ 2.4 ]
for i in range(2, num_cards + 1):
    for j in range(2, k + 1):
        add_clause((-register(i, j), register(i-1, j), register(i-1, j-1)))
        add_clause((-register(i, j), register(i-1, j), i))

# [ 2.5 ]
add_clause((register(num_cards, k),))

# [ 3 ]
# Remove symmetry (say, by fixing three cards)
add_clause((1,))
add_clause((2,))
add_clause((4,))

# Output the DIMACS
print('p cnf {} {}'.format(register(num_cards, k), len(clauses)))
for clause in clauses:
    print(' '.join(str(i) for i in clause) + ' 0')
