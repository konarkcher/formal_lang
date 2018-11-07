import pickle
from copy import deepcopy


# -----------------------------------------------------------------------------
# Automata classes
# -----------------------------------------------------------------------------

class State:
    def __init__(self, abc):
        self.next = {symb: set() for symb in abc}
        self.is_terminal = False

    def get_next(self, letter):
        return next(iter(self.next[letter]))


class Automata:
    def __init__(self, abc):
        self.abc = abc
        self.state = dict()

    def print(self):
        for state_id, state in self.state.items():
            not_term = '' if state.is_terminal else 'not '
            print('State {} is {}terminal:'.format(state_id, not_term))
            for letter, v_to in state.next.items():
                print(letter, '->', v_to)

        print_delimiter()


def print_delimiter():
    print('-' * 80)


# -----------------------------------------------------------------------------
# Input
# -----------------------------------------------------------------------------

def get_id(state_id):
    return frozenset([str(state_id)])


def input_automata():
    abc = input('Input alphabet: ').split()
    state_count = int(input('Input state count: '))
    terminal_states = input('Input terminal states: ').split()

    automata = Automata(abc)
    for i in range(state_count):
        automata.state[get_id(i)] = State(abc)

    for terminal in terminal_states:
        automata.state[get_id(terminal)].is_terminal = True

    edge_count = int(input('Input edge count: '))
    for i in range(edge_count):
        edge = input('Input edge <from> <letter> <to>: ').split()
        v_from, letter, v_to = edge
        automata.state[get_id(v_from)].next[letter].add(get_id(v_to))

    print_delimiter()
    return automata


def input_and_save():
    with open('automata.pickle', 'wb') as f:
        pickle.dump(input_automata(), f)


def load_and_get():
    with open('automata.pickle', 'rb') as f:
        auto = pickle.load(f)
    return auto


# -----------------------------------------------------------------------------
# Determinization
# -----------------------------------------------------------------------------


def merge_states(state_id_list, automata):
    new_state = State(automata.abc)

    for state_id in state_id_list:
        state = automata.state[get_id(state_id)]

        new_state.is_terminal |= state.is_terminal
        for letter in new_state.next.keys():
            new_state.next[letter] |= state.next[letter]

    return new_state


def add_steps_to_trash(state):
    need_trash = False

    for letter in state.next.keys():
        if len(state.next[letter]) == 0:
            need_trash = True
            state.next[letter].add(get_id('trash'))
    return need_trash


def determinize(automata):
    det_auto = Automata(automata.abc)
    queue = {get_id(0)}
    processed_states = set()

    while len(queue) > 0:
        state_id = queue.pop()
        processed_states.add(state_id)

        # combine the sets of states in which transitions on letters
        state = merge_states(state_id, automata)
        det_auto.state[state_id] = state

        # transform sets into new states
        for letter in state.next.keys():
            if len(state.next[letter]) > 0:
                next_state_id = []
                for next_id in state.next[letter]:
                    next_state_id += list(next_id)

                new_next_id = frozenset(next_state_id)
                state.next[letter] = {new_next_id}

                if new_next_id not in processed_states:
                    queue.add(new_next_id)

    need_trash = False
    for state in det_auto.state.values():
        need_trash |= add_steps_to_trash(state)
    if need_trash:
        trash_state = State(det_auto.abc)
        add_steps_to_trash(trash_state)
        det_auto.state[get_id('trash')] = trash_state

    return det_auto


# -----------------------------------------------------------------------------
# Inverse
# -----------------------------------------------------------------------------

def inverse(automata):
    automata = determinize(automata)
    for state in automata.state.values():
        state.is_terminal = not state.is_terminal
    return automata


# -----------------------------------------------------------------------------
# Minimization
# -----------------------------------------------------------------------------

def get_identity(state_id, state, classes, abc):
    identity = [classes[state_id]]
    identity += [classes[state.get_next(letter)] for letter in abc]
    return tuple(identity)


def get_min_state_id(classes, i):
    for state_id, class_id in classes.items():
        if class_id == i:
            return state_id


def minimize(automata):
    automata = determinize(automata)

    previous_classes = dict()
    for state_id, state in automata.state.items():
        previous_classes[state_id] = int(state.is_terminal)

    while True:
        mapping = dict()
        classes = dict()
        class_count = 0

        for state_id, state in automata.state.items():
            state_identity = get_identity(state_id, state, previous_classes,
                                          automata.abc)
            if state_identity not in mapping:
                mapping[state_identity] = class_count
                class_count += 1
            classes[state_id] = mapping[state_identity]

        if classes == previous_classes:
            break
        previous_classes = classes

    min_auto = Automata(automata.abc)
    for i in range(class_count):
        state = deepcopy(automata.state[get_min_state_id(classes, i)])
        for letter in state.next.keys():
            state.next[letter] = {get_id(classes[state.get_next(letter)])}
        min_auto.state[get_id(i)] = state

    print(classes)
    return min_auto


# -----------------------------------------------------------------------------
# Equivalence
# -----------------------------------------------------------------------------

def dfs(auto1, cur1, visited1, auto2, cur2, visited2, letter):
    visited1.add((letter, cur1))
    visited2.add((letter, cur2))

    if auto1.state[cur1].is_terminal != auto2.state[cur2].is_terminal:
        return False

    for letter in auto1.state[cur1].next.keys():
        next1 = (letter, auto1.state[cur1].get_next(letter))
        next2 = (letter, auto2.state[cur2].get_next(letter))
        if (next1 in visited1) != (next2 in visited2):
            return False

        if next1 not in visited1:
            res = dfs(auto1, next1[1], visited1, auto2, next2[1], visited2,
                      letter)
            if not res:
                return False

    return True


def equiv(auto1, auto2):
    auto1 = minimize(auto1)
    auto2 = minimize(auto2)
    if len(auto1.state) != len(auto2.state):
        return False

    visited1 = set()
    visited2 = set()

    return dfs(auto1, get_id(0), visited1, auto2, get_id(0), visited2, '0')


if __name__ == '__main__':
    # example of backup and restore
    # input_and_save()
    my_auto = load_and_get()

    edge_count = int(input('Input edge count: '))
    for i in range(edge_count):
        edge = input('Input edge <from> <letter> <to>: ').split()
        v_from, letter, v_to = edge
        my_auto.state[get_id(v_from)].next[letter].add(get_id(v_to))
    my_auto.print()

    # my_auto = input_automata()
    minimize(my_auto).print()
