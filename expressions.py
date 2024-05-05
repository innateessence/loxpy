from .token import Token


class AbstractExpression:
    """Abstract class for expressions"""

    pass


class BinaryExpr(AbstractExpression):
    def __init__(
        self, left: AbstractExpression, operator: Token, right: AbstractExpression
    ):
        self.left = left
        self.operator = operator
        self.right = right



