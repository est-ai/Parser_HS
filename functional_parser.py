import re
from typing import List

from exceptions import InvalidString, RuleSyntaxError
from tokens import BaseToken, NumberToken, OperatorToken, ParenToken, NonTerminalToken
from tree import NegativeTree, BasedParseTree, ScalingsTree, IncrementsTree, TermTree, ExpressionTree


class CalculatorParser:
    def __init__(self):
        self.tokens, self.current_token, self.next_token, self.equation = None, None, None, None

    def parse(self, equation: str) -> BasedParseTree:
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
        self.current_token = next(self.tokens, None)
        self.next_token = next(self.tokens, None)
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
        print(split_expr)
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

    def advance(self) -> BasedParseTree:
        """ current, next token 을 다음 스텝으로 진행 함수 """
        result = BasedParseTree(self.current_token)
        self.current_token, self.next_token = self.next_token, next(self.tokens, None)
        return result

    def is_accept(self, token_type: str) -> bool:
        """
        current token type 이 Rule이 요구하는 type가 일치하는지 판별하는 함수
        Args:
            token_type(str): Rule 이 요구하는 type

        Returns:
            bool: 일치하면 True, 불일치하면 False

        """
        return self.current_token and self.current_token.token_type == token_type

    def expression(self) -> BasedParseTree:
        """
        Expr -> Term Increments
        """
        tree = ExpressionTree(NonTerminalToken("Expr"))
        tree.insert(self.term())
        tree.insert(self.increments())
        return tree

    def term(self) -> BasedParseTree:
        """ Term -> Factor Scalings """
        tree = TermTree(NonTerminalToken("Term"))
        tree.insert(self.factor())
        tree.insert(self.scalings())
        return tree

    def factor(self) -> BasedParseTree:
        """ Factor -> Number | Enclosed | Negative """
        tree = BasedParseTree(NonTerminalToken("Factor"))
        if self.is_accept("Number"):
            tree.insert(self.advance())
            return tree

        elif self.is_accept("LParen"):
            tree.insert(self.enclosed())
            return tree

        elif self.is_accept("AddOp") and self.current_token.value == "-":
            tree.insert(self.negative())
            return tree

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")

    def enclosed(self) -> BasedParseTree:
        self.advance()
        expr_value = self.expression()
        if self.is_accept("RParen"):
            self.advance()

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")
        return expr_value

    def negative(self) -> NegativeTree:
        """ Negative -> - Number"""
        tree = NegativeTree(NonTerminalToken("Negative"))
        if self.is_accept("AddOp"):
            tree.insert(self.advance())

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")

        if self.is_accept("Number"):
            tree.insert(self.advance())

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")
        return tree

    def scalings(self) -> BasedParseTree:
        """ Scalings -> Scaling Scalings | ε """
        tree = ScalingsTree(NonTerminalToken("Scalings"))
        if self.is_accept("MulOp"):
            tree.insert(self.scaling())
            tree.insert(self.scalings())

        else:   # epsilon
            pass

        return tree

    def scaling(self) -> BasedParseTree:
        """ Scaling -> MulOp Factor"""
        tree = BasedParseTree(NonTerminalToken("Scaling"))
        tree.insert(self.mul_operator())
        tree.insert(self.factor())
        return tree

    def increments(self) -> BasedParseTree:
        """ Increments -> Increment Increments | ε """
        tree = IncrementsTree(NonTerminalToken("Increments"))
        if self.is_accept("AddOp"):
            tree.insert(self.increment())
            tree.insert(self.increments())

        else:   # epsilon
            pass

        return tree

    def increment(self) -> BasedParseTree:
        """ Increment -> AddOp term """
        tree = BasedParseTree(NonTerminalToken("Increment"))
        tree.insert(self.add_operator())
        tree.insert(self.term())
        return tree

    def add_operator(self) -> BasedParseTree:
        """ AddOp -> + | - """
        if self.is_accept("AddOp"):
            return self.advance()

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")

    def mul_operator(self) -> BasedParseTree:
        """ MulOp -> * | / """
        if self.is_accept("MulOp"):
            return self.advance()

        else:
            raise RuleSyntaxError(f"Should not arrive here {self.current_token}")
