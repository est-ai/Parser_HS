from __future__ import annotations

from operator import sub, add, mul, truediv
from typing import List, Union

from exceptions import ExistedData
from tokens import BaseToken


class BasedParseTree:
    def __init__(self, data: BaseToken):
        self.data = data
        self.left = None
        self.right = None

    def print_tree(self, idx: int = 0) -> None:
        """
        Tree 를 출력해주는 함수
        Args:
            idx(int): tree depth(default: 0)

        """
        print('  ' * idx, f"{idx}:  {self.data}")
        if self.left:
            self.left.print_tree(idx + 1)

        if self.right:
            self.right.print_tree(idx + 1)

    def insert(self, tree: BasedParseTree) -> None:
        if not self.left:
            self.left = tree

        elif not self.right:
            self.right = tree

        else:
            raise ExistedData(f"left leaf and right leaf already exist.")

    def evaluate(self) -> float:
        result = self.traverse()
        return result[0]

    def traverse(self) -> List[Union[str, float]]:
        result = []
        if self.data.value:
            result.append(self.data.value)

        elif self.left:
            result += self.left.traverse()

            if self.right:
                result += self.right.traverse()

        return self.calculate(result)

    def calculate(self, equation: List[Union[str, float]]) -> List[Union[str, float]]:
        return equation


class NegativeTree(BasedParseTree):
    def calculate(self, equation: List[Union[str, float]]):
        if len(equation) == 2:
            return [-equation[1]]
        raise ValueError('Left or right leaves do not exist.')


class IncrementsTree(BasedParseTree):
    def __init__(self, data: BaseToken):
        super().__init__(data)
        self.binary_calculate_map = {"+": add, "-": sub}

    def calculate(self, equation: List[Union[str, float]]) -> List[Union[str, float]]:
        if len(equation) == 4:
            return list(equation[0]) + [self.binary_calculate_map[equation[2]](equation[1], equation[3])]
        return equation


class ScalingsTree(BasedParseTree):
    def __init__(self, data: BaseToken):
        super().__init__(data)
        self.binary_calculate_map = {"*": mul, "/": truediv}

    def calculate(self, equation: List[Union[str, float]]) -> List[Union[str, float]]:
        if len(equation) == 4:
            return list(equation[0]) + [self.binary_calculate_map[equation[2]](equation[1], equation[3])]
        return equation


class TermTree(ScalingsTree):
    def calculate(self, equation: List[Union[str, float]]):
        if len(equation) == 3:
            return [self.binary_calculate_map[equation[1]](equation[0], equation[2])]
        return equation


class ExpressionTree(IncrementsTree):
    def calculate(self, equation: List[Union[str, float]]):
        if len(equation) == 3:
            return [self.binary_calculate_map[equation[1]](equation[0], equation[2])]
        return equation
