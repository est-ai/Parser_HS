from functional_parser import CalculatorParser

if __name__ == '__main__':
    parser = CalculatorParser()
    test_cases = ["3 + 5 * 7", "4 + 3 * -7 -4", "(1.2+1) * 2 / 3 - 3"]
    for tc in test_cases:
        tree = parser.parse(tc)
        tree.print_tree()
        print("=" * 20)
        result = tree.evaluate()
        print(result)
        print(result == eval(tc))