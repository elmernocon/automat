from automat import Automaton


def main():
    regular_expressions = [
        '10+',                              # L(M1)
        '1+1*',                             # L(M2)
        '01*101+',                          # L(M3)
        '1(00)*1',                          # L(M4)
        '1(00)*1',                          # L(M4)
        '(10+1+1*)|(01*101+)|(1(00)*1)',    # L(M5)

        '101',                              # L(M1)
        '11*',                              # L(M2)
        '0*1010*',                          # L(M3)
        '0*11*0*',                          # L(M4)
        '(10111*)|(0*1010*0*11*0*)',        # L(M5)
    ]

    for regular_expression in regular_expressions:
        automaton = Automaton.create_from_regex(regular_expression)
        print(regular_expression)
        print(automaton)
        print()


def sample():
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
