from automat import Automata


def main():
    # a*
    a = Automata.create_struct('a')
    a_star = Automata.create_kleene_star(a)
    print(a_star)

    # b+
    b = Automata.create_struct('b')
    b_plus = Automata.create_kleene_plus(b)
    print(b_plus)

    # c?
    c = Automata.create_struct('c')
    c_optional = Automata.create_optional(c)
    print(c_optional)

    # a|b
    ab_union = Automata.create_union(a, b)
    print(ab_union)

    # ab
    ab_concat = Automata.create_concat(a, b)
    print(ab_concat)


if __name__ == '__main__':
    main()
