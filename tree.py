from __future__ import annotations

from typing import Union, List
from operator import add, sub, mul, truediv

from tokens import BaseToken
from exceptions import ExistedData


class ParsedTree:
    def __init__(self, data: BaseToken = None):
        self.child = []
        self.data = data
        self.binary_calculate_map = {"+": add, "-": sub, "*": mul, "/": truediv}

    def print_tree(self, idx: int = 0) -> None:
        """
        Tree 를 출력해주는 함수
        Args:
            idx(int): tree depth(default: 0)

        """
        print('  ' * idx, f"{idx}:  {self.data}")
        for i in self.child:
            i.print_tree(idx + 1)

    def insert(self, token: Union[BaseToken, ParsedTree]) -> None:
        """
        Tree에 data 및 child를 추가하는 함수
            - input type 이 BaseToken일 경우
        Args:
            token(Union[BaseToken, ParsedTree]): 추가할 Token or Tree

        Raises:
            ExistedData: ParsedTree의 data를 변경을 시도할 때
            TypeError: Token의 type이 BaseToken이나 ParsedTree 가 아닌 경우

        """
        if type(token) is BaseToken:
            if self.data is None:
                raise ExistedData(f"Data already exists.")
            self.data = token

        elif type(token) is ParsedTree:
            self.child.append(token)

        else:
            raise TypeError(f"param `token` must only have an BaseToken or ParsedTree type.")

    def evaluate(self) -> float:
        """
        Tree를 traverse 하면서 계산하는 함수
        Returns:
            float: 수식의 계산값

        """
        equation_list = self.traverse()
        return self.calculate(equation_list)

    def traverse(self) -> List[Union[str, float]]:
        """
        ParsedTree를 분기하면서 return 값들을 계산하는 함수
        Returns:
            List[Union[str, float]]: Token의 value를 담은 리스트

        """
        result = []
        if self.child:
            for ch in self.child:
                value = ch.traverse()
                if ch.data.token_type == "Negative":  # 음수처리
                    value = [-value[1]]

                elif ch.data.token_type == "Term" and len(value) >= 3:    # 곱셈 / 나눗셈 처리
                    value = [self.calculate(value)]

                elif ch.data.token_type == "Expr" and len(value) >= 3:    # 덧셈 / 뺄셈 처리
                    value = [self.calculate(value)]

                if value:
                    result += value

        else:
            if self.data.value:
                result.append(self.data.value)
        return result

    def calculate(self, equation: List[Union[str, float]]) -> float:
        """
        Token의 Value를 담은 리스트를 받아 계산하는 하수
        Args:
            equation(List[Union[str, float]]: 계산이 필요한 숫자와 연산자를 담은 리스트

        Returns:
            float: 계산값

        """
        while len(equation) > 1:
            equation[:3] = [self.binary_calculate_map[equation[1]](equation[0], equation[2])]
        return equation[0]