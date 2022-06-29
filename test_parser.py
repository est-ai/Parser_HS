from unittest import TestCase

from functional_parser import CalculatorParser
from exceptions import RuleSyntaxError, InvalidString
from tokens import ParenToken, NumberToken, OperatorToken


class FunctionalParserTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(FunctionalParserTest, self).__init__(*args, **kwargs)
        self.parser = CalculatorParser()

    def test_tokenize(self):
        equation = "(1.2+1) * 2 / 3 - 3"
        tokens = self.parser.tokenize(equation)
        self.assertEqual(tokens,
                         [ParenToken(value='('), NumberToken(value='1.2'), OperatorToken(value='+'),
                          NumberToken(value='1'), ParenToken(value=')'), OperatorToken(value='*'),
                          NumberToken(value='2'), OperatorToken(value='/'), NumberToken(value='3'),
                          OperatorToken(value='-'), NumberToken(value='3')])

    def test_invalid_string(self):
        equation = "1.2.2 + 3"  # 소수점이 두개 이상
        self.assertRaises(InvalidString, lambda: self.parser.tokenize(equation))

        equation = "01 + 3"     # 0으로 시작되는 숫자
        self.assertRaises(InvalidString, lambda: self.parser.tokenize(equation))

        equation = "2. + 3"     # 소수점 뒷자리가 없는 경우
        self.assertRaises(InvalidString, lambda: self.parser.tokenize(equation))

        equation = ".32 + 3"     # 소수점 앞자리수가 없는 경우
        self.assertRaises(InvalidString, lambda: self.parser.tokenize(equation))

    def test_plus(self):
        equation = "1+1"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_minus(self):
        equation = "1-1"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_multiple(self):
        equation = "1*2"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_divide(self):
        equation = "1/2"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_bracket(self):
        equation = "(1-2)*2/4 * (-2)"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_decimal_point(self):
        equation = "(3+5)*2.1*(1.1234-3)/2.2234"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_multiple_bracket(self):
        equation = "(((-2 + 5) * 2 + 1) /2 -1 * (5 -3)) + 2"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_negative_number(self):
        equation = "-3+5*2*-1/1-1"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_negative_bracket(self):
        equation = "-(2+3) / 2"
        tree = self.parser.parse(equation)
        self.assertEqual(tree.evaluate(), eval(equation))

    def test_invalid_syntax(self):
        equation = "(1 + 2"     # 닫는 괄호가 없는 경우
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))

        equation = "1 - "       # +,-의 피연산자가 부족한 경우
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))

        equation = "1  2"       # 연산자가 부족한 경우
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))

        equation = "1 * 2)"     # 여는 괄호가 없는 경우
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))

        equation = "1 / "       # *, / 의 피연산자가 부족한 경우
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))

        equation = "1 / x"      # 글자가 있는 수식
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))

        equation = "1.2 % 2"    # +, -, *, / 를 제외한 다른 특수문자가 있는 수식
        self.assertRaises(RuleSyntaxError, lambda: self.parser.parse(equation))
