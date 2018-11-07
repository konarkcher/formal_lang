# Formal languages

## Automata library

[minimize.py](minimize/minimize.py)

### Features:

* automata input and backups
* automata print
* inverse
* determinization
* minimization
* equivalence check

### Example of use:

1. Determinization

```
Input alphabet: a
Input state count: 1
Input terminal states: 0
Input edge count: 0
--------------------------------------------------------------------------------
State frozenset({'0'}) is terminal:
a -> {frozenset({'1'})}
State frozenset({'1'}) is not terminal:
a -> {frozenset({'1'})}
--------------------------------------------------------------------------------
```

2. minimization

```
Input alphabet: a b
Input state count: 8
Input terminal states: 0 1 2 3 4 7
Input edge count: 16
Input edge <from> <letter> <to>: 0 b 0
Input edge <from> <letter> <to>: 0 a 1
Input edge <from> <letter> <to>: 1 b 0
Input edge <from> <letter> <to>: 1 a 2
Input edge <from> <letter> <to>: 2 a 5
Input edge <from> <letter> <to>: 2 b 3
Input edge <from> <letter> <to>: 3 b 3
Input edge <from> <letter> <to>: 3 a 4
Input edge <from> <letter> <to>: 4 a 5
Input edge <from> <letter> <to>: 4 b 3
Input edge <from> <letter> <to>: 5 a 7
Input edge <from> <letter> <to>: 5 b 6
Input edge <from> <letter> <to>: 6 a 5
Input edge <from> <letter> <to>: 6 b 6
Input edge <from> <letter> <to>: 7 a 7
Input edge <from> <letter> <to>: 7 b 7
--------------------------------------------------------------------------------
State frozenset({'0'}) is terminal:
a -> {frozenset({'1'})}
b -> {frozenset({'0'})}
State frozenset({'1'}) is terminal:
a -> {frozenset({'2'})}
b -> {frozenset({'0'})}
State frozenset({'2'}) is terminal:
a -> {frozenset({'4'})}
b -> {frozenset({'3'})}
State frozenset({'3'}) is terminal:
a -> {frozenset({'2'})}
b -> {frozenset({'3'})}
State frozenset({'4'}) is not terminal:
a -> {frozenset({'5'})}
b -> {frozenset({'6'})}
State frozenset({'5'}) is terminal:
a -> {frozenset({'5'})}
b -> {frozenset({'5'})}
State frozenset({'6'}) is not terminal:
a -> {frozenset({'4'})}
b -> {frozenset({'6'})}
--------------------------------------------------------------------------------
```

## Regex parsing

[shortest_path.py](shortest_word/shortest_word.py)

[Explanation](shortest_word/explanation.pdf)