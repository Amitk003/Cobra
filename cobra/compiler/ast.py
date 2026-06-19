from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto


class NodeType(Enum):
    PROGRAM = auto()
    PRINT = auto()
    LET = auto()
    ASSIGN = auto()
    IF = auto()
    WHILE = auto()
    FOR = auto()
    FUNC = auto()
    RETURN = auto()
    CALL = auto()
    IMPORT = auto()
    BLOCK = auto()
    BINARY_OP = auto()
    UNARY_OP = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    IDENTIFIER = auto()
    GROUP = auto()
    MEMBER_ACCESS = auto()


@dataclass
class Node:
    type: NodeType
    value: object | None = None
    children: list["Node"] | None = None
    op: str | None = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


def node(type_: NodeType, value=None, children=None, op=None):
    return Node(type=type_, value=value, children=children or [], op=op)


def program(stmts: list[Node]) -> Node:
    return node(NodeType.PROGRAM, children=stmts)


def print_stmt(expr: Node) -> Node:
    return node(NodeType.PRINT, children=[expr])


def let_assign(name: str, expr: Node) -> Node:
    return node(NodeType.LET, value=name, children=[expr])


def assign(name: str, expr: Node) -> Node:
    return node(NodeType.ASSIGN, value=name, children=[expr])


def if_stmt(cond: Node, body: Node, else_body: Node | None = None) -> Node:
    children = [cond, body]
    if else_body:
        children.append(else_body)
    return node(NodeType.IF, children=children)


def while_loop(cond: Node, body: Node) -> Node:
    return node(NodeType.WHILE, children=[cond, body])


def for_loop(var: str, start: Node, end: Node, body: Node) -> Node:
    return node(NodeType.FOR, value=var, children=[start, end, body])


def func_def(name: str, params: list[str], body: Node) -> Node:
    return node(NodeType.FUNC, value=(name, params), children=[body])


def return_stmt(expr: Node) -> Node:
    return node(NodeType.RETURN, children=[expr])


def call(name: str, args: list[Node]) -> Node:
    return node(NodeType.CALL, value=name, children=args)


def import_stmt(name: str) -> Node:
    return node(NodeType.IMPORT, value=name)


def block(stmts: list[Node]) -> Node:
    return node(NodeType.BLOCK, children=stmts)


def binary_op(left: Node, op: str, right: Node) -> Node:
    return node(NodeType.BINARY_OP, op=op, children=[left, right])


def unary_op(op: str, expr: Node) -> Node:
    return node(NodeType.UNARY_OP, op=op, children=[expr])


def int_lit(value: int) -> Node:
    return node(NodeType.INT, value=value)


def float_lit(value: float) -> Node:
    return node(NodeType.FLOAT, value=value)


def string_lit(value: str) -> Node:
    return node(NodeType.STRING, value=value)


def bool_lit(value: bool) -> Node:
    return node(NodeType.BOOL, value=value)


def identifier(name: str) -> Node:
    return node(NodeType.IDENTIFIER, value=name)


def member_access(obj: Node, member: str) -> Node:
    return node(NodeType.MEMBER_ACCESS, value=member, children=[obj])
