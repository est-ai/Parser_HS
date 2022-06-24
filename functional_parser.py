import re
from typing import List

from tree import ParsedTree
from exceptions import InvalidString, RuleSyntaxError
from tokens import BaseToken, NumberToken, OperatorToken, ParenToken, NonTerminalToken


class CalculatorParser:
    def __init__(self):
        self.tokens, self.current_token, self.next_token, self.equation = None, None, None, None

    def parse(self, equation: str) -> ParsedTree:
        """
        수식 parsing 함수
        Args:
            equation(str): string 형태의 수식

        Returns:
            ParsedTree: Parsing 된 Token 의 Tree

        Raises:
            RuleSyntaxError: 완전하지 않은 문장이 존재할 때

        Examples:
            >>> equation = "1 2"
            >>> parser = CalculatorParser()
            >>> parser.parse(equation)
            RuleSyntaxError("The equation is not complete.")

        """
        self.equation = equation
        self.tokens = iter(self.tokenize(equation))
        self.current_token = None
        self.next_token = next(self.tokens, None)
        self._advance()
        result = self.expression()
        if self.current_token:
            raise RuleSyntaxError("The equation is not complete.")
        return result

    def tokenize(self, equation: str) -> List[BaseToken]:
        """
        equation 을 tokenize 하는 함수
        Args:
            equation(str): Parsing 하고자 하는 수식

        Returns:
            List[BaseToken]: Tokenizing 된 Token의 List

        Raises:
            InvalidString: 정규표현식으로 걸러지지 않는 string이 있을 때

        """
        tokens = []
        split_expr = re.findall(f"[\d.]+|[+\-*/()]", equation)

        for i in split_expr:
            if NumberToken.is_valid(i):
                tokens.append(NumberToken(i))

            elif OperatorToken.is_valid(i):
                tokens.append(OperatorToken(i))

            elif ParenToken.is_valid(i):
                tokens.append(ParenToken(i))

            else:
                raise InvalidString(f"`{i}` is an invalid string")
        return tokens

    def _advance(self):
        """ current, next token 을 다음 스텝으로 진행 함수 """
        self.current_token, self.next_token = self.next_token, next(self.tokens, None)

    def is_accept(self, token_type: str) -> bool:
        """
        current token type 이 Rule이 요구하는 type가 일치하는지 판별하는 함수
        Args:
            token_type(str): Rule 이 요구하는 type

        Returns:
            bool: 일치하면 True, 불일치하면 False

        """
        if self.current_token and self.current_token.token_type == token_type:
            return True
        return False

    def _expect(self, token_type: str) -> None:
        """
        반드시 필요한 token 이 존재하지만 그 token을 사용하지는 않을 때
        확인하고 다음 token으로 넘어가는 함수 ex) RParen
        Args:
            token_type(str): Rule 이 요구하는 Token Type

        """
        if not self.is_accept(token_type):
            if self.next_token:
                current_type = self.next_token.token_type
            else:
                current_type = None
            raise RuleSyntaxError(f"The Type of the next token must be {token_type}, "
                                  f"but it is {current_type}")
        self._advance()

    def expression(self) -> ParsedTree:
        """
        Expr -> Term Increments
        """
        tree = ParsedTree(NonTerminalToken("Expr"))
        tree.insert(self.term())
        tree.insert(self.increments())
        return tree

    def term(self) -> ParsedTree:
        """ Term -> Factor Scalings """
        tree = ParsedTree(NonTerminalToken("Term"))
        tree.insert(self.factor())
        tree.insert(self.scalings())
        return tree

    def factor(self) -> ParsedTree:
        """ Factor -> Number | Enclosed | Negative """
        tree = ParsedTree(NonTerminalToken("Factor"))
        if self.is_accept("Number"):
            tree.insert(ParsedTree(self.current_token))
            self._advance()
            return tree

        elif self.is_accept("LParen"):
            self._advance()
            tree.insert(self.enclosed())
            return tree

        elif self.is_accept("AddOp") and self.current_token.value == "-" and self.next_token.token_type == "Number":
            tree.insert(self.negative())
            return tree

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")

    def enclosed(self) -> ParsedTree:
        expr_value = self.expression()
        self._expect("RParen")
        return expr_value

    def negative(self) -> ParsedTree:
        """ Negative -> - Number"""
        tree = ParsedTree(NonTerminalToken("Negative"))
        tree.insert(ParsedTree(self.current_token))
        self._advance()
        tree.insert(ParsedTree(self.current_token))
        self._advance()
        return tree

    def scalings(self) -> ParsedTree:
        """ Scalings -> Scaling Scalings | ε """
        tree = ParsedTree(NonTerminalToken("Scalings"))
        if self.is_accept("MulOp"):
            tree.insert(self.scaling())
            tree.insert(self.scalings())

        else:   # epsilon
            pass

        return tree

    def scaling(self) -> ParsedTree:
        """ Scaling -> MulOp Factor"""
        tree = ParsedTree(NonTerminalToken("Scaling"))
        tree.insert(self.mul_operator())
        tree.insert(self.factor())
        return tree

    def increments(self) -> ParsedTree:
        """ Increments -> Increment Increments | ε """
        tree = ParsedTree(NonTerminalToken("Increments"))
        if self.is_accept("AddOp"):
            tree.insert(self.increment())
            tree.insert(self.increments())

        else:   # epsilon
            pass

        return tree

    def increment(self) -> ParsedTree:
        """ Increment -> AddOp term """
        tree = ParsedTree(NonTerminalToken("Increment"))
        tree.insert(self.add_operator())
        tree.insert(self.term())
        return tree

    def add_operator(self) -> ParsedTree:
        """ AddOp -> + | - """
        if self.is_accept("AddOp"):
            result = ParsedTree(self.current_token)
            self._advance()
            return result

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")

    def mul_operator(self) -> ParsedTree:
        """ MulOp -> * | / """
        if self.is_accept("MulOp"):
            result = ParsedTree(self.current_token)
            self._advance()
            return result

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")
