from automat import Automata


def main():
    # 0
    zero = Automata.create_struct('0')
    print('0')
    print(zero)
    print()

    # a*
    a = Automata.create_struct('a')
    a_star = Automata.create_kleene_star(a)
    print('a*')
    print(a_star)
    print()

    # b+
    b = Automata.create_struct('b')
    b_plus = Automata.create_kleene_plus(b)
    print('b+')
    print(b_plus)
    print()

    # c?
    c = Automata.create_struct('c')
    c_optional = Automata.create_optional(c)
    print('c?')
    print(c_optional)
    print()

    # a|b
    ab_union = Automata.create_union(a, b)
    print('a|b')
    print(ab_union)
    print()

    # ab
    ab_concat = Automata.create_concat(a, b)
    print('ab')
    print(ab_concat)
    print()


if __name__ == '__main__':
    main()
