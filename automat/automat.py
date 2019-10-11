from __future__ import annotations
from itertools import chain
from typing import Dict, List, Optional, Set

ALPHABET = [chr(i) for i in chain(range(48, 58), range(65, 91), range(97, 123))]
EPSILON = '~'
OP_CONCAT = '.'
OP_KLEENE_PLUS = '+'
OP_KLEENE_STAR = '*'
OP_OPTIONAL = '?'
OP_UNION = '|'
OPERANDS_SINGLE = [OP_KLEENE_STAR, OP_KLEENE_STAR, OP_OPTIONAL]
OPERANDS_DOUBLE = [OP_CONCAT, OP_UNION]
PARENTHESIS_CLOSE = ')'
PARENTHESIS_OPEN = '('


class Automata:

    states: Set[int]
    start_state: Optional[int]
    final_states: Optional[Set[int]]
    transitions: Dict[int, Dict[int, Set[str]]]
    alphabet = Set[str]

    def __init__(self):
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = dict()

    def __repr__(self):
        representation = [
            f'states: {{ {", ".join(map(str, self.states))} }}',
            f'start state: {str(self.start_state)}',
            f'final state: {{ {", ".join(map(str, self.final_states))} }}',
            f'transitions:',
        ]

        for from_state, to_states in self.transitions.items():
            for to_state in to_states:
                for input_str in to_states[to_state]:
                    representation.append(f'  '
                                          f'{self.__repr_state(from_state)}'
                                          f' -- {input_str} --> '
                                          f'{self.__repr_state(to_state)}')

        return '\n'.join(representation)

    def __repr_state(self, state: int):
        is_start = state == self.start_state
        is_final = state in self.final_states
        return f'{">" if is_start else " "}' \
               f'{("((" if is_final else " (")} ' \
               f'{str(state)} ' \
               f'{("))" if is_final else ") ")}'

    @staticmethod
    def create_concat(automata_1: Automata, automata_2: Automata) -> Automata:
        reindexed_1 = Automata.reindex(automata_1, 2)
        reindexed_2 = Automata.reindex(automata_2, len(reindexed_1.states) + 2)

        start_state = 1
        end_state = len(reindexed_1.states) + len(reindexed_2.states) + 2

        concat = Automata()
        concat.set_start_state(start_state)
        concat.add_final_state(end_state)

        concat.add_transition(start_state, reindexed_1.start_state, EPSILON)

        for reindexed_1_final_state in reindexed_1.final_states:
            concat.add_transition(reindexed_1_final_state, reindexed_2.start_state, EPSILON)

        for reindexed_2_final_state in reindexed_2.final_states:
            concat.add_transition(reindexed_2_final_state, end_state, EPSILON)

        concat.copy_transitions(reindexed_1)
        concat.copy_transitions(reindexed_2)

        return concat

    @staticmethod
    def create_kleene_plus(automata: Automata) -> Automata:
        reindexed = Automata.reindex(automata, 2)

        start_state = 1
        end_state = len(reindexed.states) + 2

        kleene_plus = Automata()
        kleene_plus.set_start_state(start_state)
        kleene_plus.add_final_state(end_state)

        kleene_plus.add_transition(start_state, reindexed.start_state, EPSILON)

        for reindexed_final_state in reindexed.final_states:
            kleene_plus.add_transition(reindexed_final_state, start_state, EPSILON)
            kleene_plus.add_transition(reindexed_final_state, end_state, EPSILON)

        kleene_plus.copy_transitions(reindexed)

        return kleene_plus

    @staticmethod
    def create_kleene_star(automata: Automata) -> Automata:
        reindexed = Automata.reindex(automata, 2)

        start_state = 1
        end_state = len(reindexed.states) + 2

        kleene_star = Automata()
        kleene_star.set_start_state(start_state)
        kleene_star.add_final_state(end_state)

        kleene_star.add_transition(start_state, reindexed.start_state, EPSILON)

        kleene_star.add_transition(start_state, end_state, EPSILON)

        for reindexed_final_state in reindexed.final_states:
            kleene_star.add_transition(reindexed_final_state, start_state, EPSILON)
            kleene_star.add_transition(reindexed_final_state, end_state, EPSILON)

        kleene_star.copy_transitions(reindexed)

        return kleene_star

    @staticmethod
    def create_optional(automata: Automata) -> Automata:
        reindexed = Automata.reindex(automata, 2)

        start_state = 1
        end_state = len(reindexed.states) + 2

        optional = Automata()
        optional.set_start_state(start_state)
        optional.add_final_state(end_state)

        optional.add_transition(start_state, reindexed.start_state, EPSILON)

        optional.add_transition(start_state, end_state, EPSILON)

        for reindexed_final_state in reindexed.final_states:
            optional.add_transition(reindexed_final_state, end_state, EPSILON)

        optional.copy_transitions(reindexed)

        return optional

    @staticmethod
    def create_struct(input_str: str) -> Automata:
        if str not in ALPHABET:
            raise SyntaxError

        automata = Automata()
        automata.set_start_state(1)
        automata.add_final_state(2)
        automata.add_transition(1, 2, input_str)

        return automata

    @staticmethod
    def create_union(automata_1: Automata, automata_2: Automata) -> Automata:
        reindexed_1 = Automata.reindex(automata_1, 2)
        reindexed_2 = Automata.reindex(automata_2, len(reindexed_1.states) + 2)

        start_state = 1
        end_state = len(reindexed_1.states) + len(reindexed_2.states) + 2

        union = Automata()

        union.set_start_state(start_state)
        union.add_final_state(end_state)

        union.add_transition(start_state, reindexed_1.start_state, EPSILON)
        union.add_transition(start_state, reindexed_2.start_state, EPSILON)

        for reindexed_1_final_state in reindexed_1.final_states:
            union.add_transition(reindexed_1_final_state, end_state, EPSILON)

        for reindexed_2_final_state in reindexed_2.final_states:
            union.add_transition(reindexed_2_final_state, end_state, EPSILON)

        union.copy_transitions(reindexed_1)
        union.copy_transitions(reindexed_2)

        return union

    @staticmethod
    def reindex(automata: Automata, start_index: int = 1) -> Automata:
        index = start_index
        mapping = {}
        for i in automata.states:
            mapping[i] = index
            index += 1
        reindexed = Automata()
        reindexed.set_start_state(mapping[automata.start_state])
        reindexed.add_final_states([mapping[final_state] for final_state in automata.final_states])
        for from_state, to_states in automata.transitions.items():
            for to_state in to_states:
                reindexed.add_transition(
                    mapping[from_state],
                    mapping[to_state],
                    *to_states[to_state])

        return reindexed

    def set_start_state(self, state: int) -> None:
        self.start_state = state
        self.states.add(state)

    def add_final_state(self, state: int) -> None:
        self.final_states.add(state)
        self.states.add(state)

    def add_final_states(self, states: List[int]) -> None:
        for state in states:
            self.add_final_state(state)

    def add_transition(self, from_state: int, to_state: int, *args: str) -> None:
        inputs = set(*args)
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions:
            if to_state in self.transitions[from_state]:
                self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(inputs)
            else:
                self.transitions[from_state][to_state] = inputs
        else:
            self.transitions[from_state] = {
                to_state: inputs
            }

    def copy_transitions(self, automata: Automata) -> None:
        for from_state, to_states in automata.transitions.items():
            for to_state in to_states:
                self.add_transition(from_state, to_state, *to_states[to_state])
