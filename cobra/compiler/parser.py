from cobra.compiler.lexer import Token
from cobra.compiler import ast


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def peek_type(self) -> str:
        return self.peek().type

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, *types: str) -> Token:
        if self.peek_type() in types:
            return self.advance()
        got = self.peek()
        expected = " or ".join(types)
        raise ParseError(f"Expected {expected}, got {got.type}({got.value!r}) at L{got.line}:{got.col}")

    def skip_newlines(self):
        while self.peek_type() == "NEWLINE":
            self.advance()

    def parse(self) -> ast.Node:
        stmts = []
        self.skip_newlines()
        while self.peek_type() != "EOF":
            stmts.append(self.parse_stmt())
            self.skip_newlines()
        return ast.program(stmts)

    def parse_stmt(self) -> ast.Node:
        tok = self.peek()

        if tok.type == "LET":
            return self.parse_let()
        if tok.type == "IF":
            return self.parse_if()
        if tok.type == "WHILE":
            return self.parse_while()
        if tok.type == "FOR":
            return self.parse_for()
        if tok.type == "FUNC":
            return self.parse_func()
        if tok.type == "RETURN":
            return self.parse_return()
        if tok.type == "IMPORT":
            return self.parse_import()
        if tok.type == "LBRACE":
            return self.parse_block()
        if tok.type == "NEWLINE":
            self.advance()
            return self.parse_stmt()

        if tok.type == "IDENTIFIER" and self._peek_next().type == "EQ":
            name = self.advance().value
            self.expect("EQ")
            val = self.parse_expr()
            return ast.assign(name, val)

        expr = self.parse_expr()
        return expr

    def _peek_next(self) -> Token:
        idx = self.pos + 1
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def parse_let(self) -> ast.Node:
        self.expect("LET")
        name = self.expect("IDENTIFIER").value
        self.expect("EQ")
        val = self.parse_expr()
        return ast.let_assign(name, val)

    def parse_if(self) -> ast.Node:
        self.expect("IF")
        cond = self.parse_expr()
        body = self.parse_block()
        else_body = None
        if self.peek_type() == "ELSE":
            self.advance()
            else_body = self.parse_block()
        return ast.if_stmt(cond, body, else_body)

    def parse_while(self) -> ast.Node:
        self.expect("WHILE")
        cond = self.parse_expr()
        body = self.parse_block()
        return ast.while_loop(cond, body)

    def parse_for(self) -> ast.Node:
        self.expect("FOR")
        var = self.expect("IDENTIFIER").value
        self.expect("IN")
        start = self.parse_expr()
        self.expect("RANGE")
        end = self.parse_expr()
        body = self.parse_block()
        return ast.for_loop(var, start, end, body)

    def parse_func(self) -> ast.Node:
        self.expect("FUNC")
        name = self.expect("IDENTIFIER").value
        self.expect("LPAREN")
        params = []
        if self.peek_type() != "RPAREN":
            params.append(self.expect("IDENTIFIER").value)
            while self.peek_type() == "COMMA":
                self.advance()
                params.append(self.expect("IDENTIFIER").value)
        self.expect("RPAREN")
        body = self.parse_block()
        return ast.func_def(name, params, body)

    def parse_return(self) -> ast.Node:
        self.expect("RETURN")
        expr = self.parse_expr()
        return ast.return_stmt(expr)

    def parse_import(self) -> ast.Node:
        self.expect("IMPORT")
        name = self.expect("IDENTIFIER").value
        return ast.import_stmt(name)

    def parse_block(self) -> ast.Node:
        self.expect("LBRACE")
        stmts = []
        while self.peek_type() not in ("RBRACE", "EOF"):
            self.skip_newlines()
            if self.peek_type() == "RBRACE":
                break
            stmts.append(self.parse_stmt())
            self.skip_newlines()
        self.expect("RBRACE")
        return ast.block(stmts)

    def parse_expr(self) -> ast.Node:
        return self.parse_or()

    def parse_or(self) -> ast.Node:
        left = self.parse_and()
        while self.peek_type() in ("OR",):
            op = self.advance().value
            right = self.parse_and()
            left = ast.binary_op(left, op, right)
        return left

    def parse_and(self) -> ast.Node:
        left = self.parse_comparison()
        while self.peek_type() in ("AND",):
            op = self.advance().value
            right = self.parse_comparison()
            left = ast.binary_op(left, op, right)
        return left

    def parse_comparison(self) -> ast.Node:
        left = self.parse_addition()
        while self.peek_type() in ("EQEQ", "NEQ", "LT", "GT", "LE", "GE"):
            op = self.advance().value
            right = self.parse_addition()
            left = ast.binary_op(left, op, right)
        return left

    def parse_addition(self) -> ast.Node:
        left = self.parse_multiplication()
        while self.peek_type() in ("PLUS", "MINUS"):
            op = self.advance().value
            right = self.parse_multiplication()
            left = ast.binary_op(left, op, right)
        return left

    def parse_multiplication(self) -> ast.Node:
        left = self.parse_unary()
        while self.peek_type() in ("STAR", "SLASH"):
            op = self.advance().value
            right = self.parse_unary()
            left = ast.binary_op(left, op, right)
        return left

    def parse_unary(self) -> ast.Node:
        if self.peek_type() in ("MINUS", "NOT"):
            op = self.advance().value
            expr = self.parse_unary()
            return ast.unary_op(op, expr)
        return self.parse_primary()

    def parse_primary(self) -> ast.Node:
        tok = self.peek()

        if tok.type == "NUMBER":
            self.advance()
            val = tok.value
            if "." in val:
                return ast.float_lit(float(val))
            return ast.int_lit(int(val))

        if tok.type == "STRING":
            self.advance()
            return ast.string_lit(tok.value[1:-1])

        if tok.type == "TRUE":
            self.advance()
            return ast.bool_lit(True)

        if tok.type == "FALSE":
            self.advance()
            return ast.bool_lit(False)

        if tok.type == "IDENTIFIER":
            name = self.advance().value
            if self.peek_type() == "LPAREN":
                self.advance()
                args = []
                if self.peek_type() != "RPAREN":
                    args.append(self.parse_expr())
                    while self.peek_type() == "COMMA":
                        self.advance()
                        args.append(self.parse_expr())
                self.expect("RPAREN")
                return ast.call(name, args)
            return ast.identifier(name)

        if tok.type == "LPAREN":
            self.advance()
            expr = self.parse_expr()
            self.expect("RPAREN")
            return ast.node(ast.NodeType.GROUP, children=[expr])

        if tok.type == "MINUS":
            self.advance()
            return ast.unary_op("-", self.parse_primary())

        raise ParseError(f"Unexpected token {tok.type}({tok.value!r}) at L{tok.line}:{tok.col}")
