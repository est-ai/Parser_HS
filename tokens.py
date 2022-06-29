import re

from exceptions import InvalidToken


class BaseToken:
    def __init__(self, value: str = None):
        if not self.is_valid(value):
            raise InvalidToken(f"`{value}` is not {self.__class__}.")
        self.token_type = None
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, BaseToken):
            return NotImplemented
        return self.value == other.value and self.token_type == other.token_type

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}(type='{self.token_type}', value='{self.value}')"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        pass

    def select_type(self, value: str) -> str:
        raise ValueError("No type exists to select")


class NumberToken(BaseToken):
    def __init__(self, value: str):
        super().__init__(value)
        self.token_type = "Number"
        self.value = float(value)

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return True if re.match(r"^\d+\.?\d+$|^\d+$", value) else False


class OperatorToken(BaseToken):
    def __init__(self, value: str):
        super().__init__(value)
        self.token_type = self.select_type(value)

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in ["+", "-", "*", "/"]

    def select_type(self, value: str) -> str:
        return "AddOp" if value in ["+", "-"] else "MulOp"


class ParenToken(BaseToken):
    def __init__(self, value: str):
        super().__init__(value)
        self.token_type = self.select_type(value)

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in ["(", ")"]

    def select_type(self, value: str) -> str:
        return "LParen" if value == "(" else "RParen"


class NonTerminalToken(BaseToken):
    def __init__(self, token_type: str):
        super().__init__()
        self.token_type = token_type

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return True


class TerminalToken(BaseToken):
    def __init__(self, value: str, token_type: str = None):
        super().__init__(value)
        self.token_type = token_type

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return True
