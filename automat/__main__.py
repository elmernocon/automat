from automat import Automaton


def main():
    # 0
    zero = Automaton.create_struct('0')
    print('0')
    print(zero)
    print()

    # a*
    a = Automaton.create_struct('a')
    a_star = Automaton.create_kleene_star(a)
    print('a*')
    print(a_star)
    print()

    # b+
    b = Automaton.create_struct('b')
    b_plus = Automaton.create_kleene_plus(b)
    print('b+')
    print(b_plus)
    print()

    # c?
    c = Automaton.create_struct('c')
    c_optional = Automaton.create_optional(c)
    print('c?')
    print(c_optional)
    print()

    # a|b
    ab_union = Automaton.create_union(a, b)
    print('a|b')
    print(ab_union)
    print()

    # ab
    ab_concat = Automaton.create_concat(a, b)
    print('ab')
    print(ab_concat)
    print()


if __name__ == '__main__':
    main()
