from __future__ import annotations
from itertools import chain
from typing import Dict, List, Optional, Set

ALPHABET = [chr(i) for i in chain(range(48, 58), range(65, 91), range(97, 123))]
EPSILON = 'ε'
OP_CONCAT = '.'
OP_KLEENE_PLUS = '+'
OP_KLEENE_STAR = '*'
OP_OPTIONAL = '?'
OP_UNION = '|'
OPERANDS_SINGLE = [OP_KLEENE_PLUS, OP_KLEENE_STAR, OP_OPTIONAL]
OPERANDS_DOUBLE = [OP_CONCAT, OP_UNION]
PARENTHESIS_CLOSE = ')'
PARENTHESIS_OPEN = '('


class Automaton:

    states: Set[int]
    start_state: Optional[int]
    final_states: Optional[Set[int]]
    transitions: Dict[int, Dict[int, Set[str]]]

    def __init__(self):
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = dict()

    def __repr__(self):
        representation = [
            f'alphabet: {{ {", ".join(map(str, self.get_alphabet()))} }}',
            f'states: {{ {", ".join(map(str, self.states))} }}',
            f'start state: {str(self.start_state)}',
            f'final states: {{ {", ".join(map(str, self.final_states))} }}',
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
    def create_concat(automaton_1: Automaton, automaton_2: Automaton) -> Automaton:
        reindexed_1 = Automaton.reindex(automaton_1, 2)
        reindexed_2 = Automaton.reindex(automaton_2, len(reindexed_1.states) + 2)

        start_state = 1
        end_state = len(reindexed_1.states) + len(reindexed_2.states) + 2

        concat = Automaton()
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
    def create_from_regex(regex: str) -> Automaton:

        prev_char = EPSILON
        operator_stack = []
        automata_stack = []

        def process_operator(operator: str) -> None:
            len_automata_stack = len(automata_stack)
            if len_automata_stack == 0:
                raise Exception(f'Error processing "{operator}" operator. automata_stack is empty.')
            if operator in OPERANDS_SINGLE:
                a = automata_stack.pop()
                if operator == OP_KLEENE_PLUS:
                    automata_stack.append(Automaton.create_kleene_plus(a))
                elif operator == OP_KLEENE_STAR:
                    automata_stack.append(Automaton.create_kleene_star(a))
                elif operator == OP_OPTIONAL:
                    automata_stack.append(Automaton.create_optional(a))
            elif operator in OPERANDS_DOUBLE:
                if len_automata_stack < 2:
                    raise Exception(f'Error processing "{operator}" operator. Inadequate operands.')
                b = automata_stack.pop()
                a = automata_stack.pop()
                if operator == OP_CONCAT:
                    automata_stack.append(Automaton.create_concat(a, b))
                elif operator == OP_UNION:
                    automata_stack.append(Automaton.create_union(a, b))

        def add_operator(operator: str) -> None:
            len_operator_stack = len(operator_stack)
            while True:
                if len_operator_stack == 0:
                    break
                top = operator_stack[-1]
                if top == PARENTHESIS_OPEN:
                    break
                if top == OP_CONCAT or top == operator:
                    op = operator_stack.pop()
                    process_operator(op)
                else:
                    break
            operator_stack.append(operator)

        for char in regex:
            if char in ALPHABET:
                if (prev_char != OP_CONCAT and
                        (prev_char in ALPHABET or prev_char in [PARENTHESIS_CLOSE, *OPERANDS_SINGLE])):
                    add_operator(OP_CONCAT)
                automata_stack.append(Automaton.create_struct(char))
            elif char == PARENTHESIS_OPEN:
                if (prev_char != OP_CONCAT and
                        (prev_char in ALPHABET or prev_char in [PARENTHESIS_CLOSE, *OPERANDS_SINGLE])):
                    add_operator(OP_CONCAT)
                operator_stack.append(PARENTHESIS_OPEN)
            elif char == PARENTHESIS_CLOSE:
                if prev_char in OPERANDS_DOUBLE:
                    raise Exception(f'Error processing "{char}" after "{prev_char}".')
                while True:
                    if len(operator_stack) == 0:
                        raise Exception(f'Error processing "{char}" operator. operator_stack is empty.')
                    oper = operator_stack.pop()
                    if oper == PARENTHESIS_OPEN:
                        break
                    elif oper in OPERANDS_DOUBLE:
                        process_operator(oper)
            elif char in OPERANDS_SINGLE:
                if (prev_char == PARENTHESIS_OPEN or
                        prev_char in OPERANDS_SINGLE or
                        prev_char in OPERANDS_DOUBLE):
                    raise Exception(f'Error processing "{char}" after "{prev_char}".')
                process_operator(char)
            elif char in OPERANDS_DOUBLE:
                if (prev_char in OPERANDS_SINGLE or
                        prev_char in OPERANDS_DOUBLE):
                    raise Exception(f'Error processing "{char}" after "{prev_char}".')
                add_operator(char)
            else:
                raise Exception(f'Symbol "{char}" is not allowed.')

            prev_char = char

        while len(operator_stack) != 0:
            oper = operator_stack.pop()
            process_operator(oper)

        if len(automata_stack) > 1:
            raise Exception(f'Unable to parse "{regex}" regular expression.')

        return automata_stack.pop()

    @staticmethod
    def create_kleene_plus(automaton: Automaton) -> Automaton:
        reindexed = Automaton.reindex(automaton, 2)

        start_state = 1
        end_state = len(reindexed.states) + 2

        kleene_plus = Automaton()
        kleene_plus.set_start_state(start_state)
        kleene_plus.add_final_state(end_state)

        kleene_plus.add_transition(start_state, reindexed.start_state, EPSILON)

        for reindexed_final_state in reindexed.final_states:
            kleene_plus.add_transition(reindexed_final_state, start_state, EPSILON)
            kleene_plus.add_transition(reindexed_final_state, end_state, EPSILON)

        kleene_plus.copy_transitions(reindexed)

        return kleene_plus

    @staticmethod
    def create_kleene_star(automaton: Automaton) -> Automaton:
        reindexed = Automaton.reindex(automaton, 2)

        start_state = 1
        end_state = len(reindexed.states) + 2

        kleene_star = Automaton()
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
    def create_optional(automaton: Automaton) -> Automaton:
        reindexed = Automaton.reindex(automaton, 2)

        start_state = 1
        end_state = len(reindexed.states) + 2

        optional = Automaton()
        optional.set_start_state(start_state)
        optional.add_final_state(end_state)

        optional.add_transition(start_state, reindexed.start_state, EPSILON)

        optional.add_transition(start_state, end_state, EPSILON)

        for reindexed_final_state in reindexed.final_states:
            optional.add_transition(reindexed_final_state, end_state, EPSILON)

        optional.copy_transitions(reindexed)

        return optional

    @staticmethod
    def create_struct(input_str: str) -> Automaton:
        if input_str not in ALPHABET:
            raise SyntaxError

        automaton = Automaton()
        automaton.set_start_state(1)
        automaton.add_final_state(2)
        automaton.add_transition(1, 2, input_str)

        return automaton

    @staticmethod
    def create_union(automaton_1: Automaton, automaton_2: Automaton) -> Automaton:
        reindexed_1 = Automaton.reindex(automaton_1, 2)
        reindexed_2 = Automaton.reindex(automaton_2, len(reindexed_1.states) + 2)

        start_state = 1
        end_state = len(reindexed_1.states) + len(reindexed_2.states) + 2

        union = Automaton()

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
    def reindex(automaton: Automaton, start_index: int = 1) -> Automaton:
        index = start_index
        mapping = {}
        for i in automaton.states:
            mapping[i] = index
            index += 1
        reindexed = Automaton()
        reindexed.set_start_state(mapping[automaton.start_state])
        reindexed.add_final_states([mapping[final_state] for final_state in automaton.final_states])
        for from_state, to_states in automaton.transitions.items():
            for to_state in to_states:
                reindexed.add_transition(
                    mapping[from_state],
                    mapping[to_state],
                    *to_states[to_state])

        return reindexed

    def get_alphabet(self) -> Set[str]:
        alphabet = set()

        for from_state, to_states in self.transitions.items():
            for to_state in to_states:
                for input_str in to_states[to_state]:
                    alphabet.add(input_str)

        return alphabet

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

    def copy_transitions(self, automaton: Automaton) -> None:
        for from_state, to_states in automaton.transitions.items():
            for to_state in to_states:
                self.add_transition(from_state, to_state, *to_states[to_state])
