from cobra.compiler import ast


class CodegenError(Exception):
    pass


class CodegenPy:
    def __init__(self):
        self.indent_level = 0
        self.output = []
        self._stdlib_imports = set()

    def indent(self):
        return "    " * self.indent_level

    def emit(self, line: str = ""):
        self.output.append(self.indent() + line)

    def generate(self, node: ast.Node) -> str:
        self.output = []
        self._stdlib_imports = set()
        self._uses_runtime = False
        self._visit(node)
        header_lines = []
        if self._uses_runtime:
            header_lines.append("from cobra.runtime.builtins import *")
        if self._stdlib_imports:
            header_lines.extend(sorted(self._stdlib_imports))
        header = ""
        if header_lines:
            header = "\n".join(header_lines) + "\n\n"
        return header + "\n".join(self.output)

    def _visit(self, node: ast.Node):
        method = f"_visit_{node.type.name.lower()}"
        visitor = getattr(self, method, None)
        if visitor is None:
            raise CodegenError(f"No codegen visitor for {node.type}")
        return visitor(node)

    def _visit_program(self, node: ast.Node):
        for child in node.children:
            result = self._visit(child)
            if result is not None:
                self.emit(f"{result}")

    def _visit_print(self, node: ast.Node):
        val = self._visit(node.children[0])
        self.emit(f"print({val})")

    def _visit_let(self, node: ast.Node):
        val = self._visit(node.children[0])
        self.emit(f"{node.value} = {val}")

    def _visit_assign(self, node: ast.Node):
        val = self._visit(node.children[0])
        self.emit(f"{node.value} = {val}")

    def _visit_if(self, node: ast.Node):
        cond = self._visit(node.children[0])
        self.emit(f"if {cond}:")
        self.indent_level += 1
        self._visit(node.children[1])
        self.indent_level -= 1
        if len(node.children) > 2:
            self.emit("else:")
            self.indent_level += 1
            self._visit(node.children[2])
            self.indent_level -= 1

    def _visit_while(self, node: ast.Node):
        cond = self._visit(node.children[0])
        self.emit(f"while {cond}:")
        self.indent_level += 1
        self._visit(node.children[1])
        self.indent_level -= 1

    def _visit_for(self, node: ast.Node):
        var = node.value
        start = self._visit(node.children[0])
        end = self._visit(node.children[1])
        self.emit(f"for {var} in range({start}, {end}):")
        self.indent_level += 1
        self._visit(node.children[2])
        self.indent_level -= 1

    def _visit_func(self, node: ast.Node):
        name, params = node.value
        param_str = ", ".join(params)
        self.emit(f"def {name}({param_str}):")
        self.indent_level += 1
        self._visit(node.children[0])
        self.indent_level -= 1

    def _visit_return(self, node: ast.Node):
        val = self._visit(node.children[0])
        self.emit(f"return {val}")

    _RUNTIME_FUNCS = {
        "print": "cobra_print",
        "input": "cobra_input",
        "str": "cobra_str",
        "int": "cobra_int",
        "bool": "cobra_bool",
        "float": "cobra_float",
        "len": "cobra_len",
        "type": "cobra_type",
        "range": "cobra_range",
    }

    def _visit_call(self, node: ast.Node):
        name = node.value
        args = ", ".join(self._visit(child) for child in node.children)
        if name in self._RUNTIME_FUNCS and "." not in name:
            self._uses_runtime = True
            return f"{self._RUNTIME_FUNCS[name]}({args})"
        return f"{name}({args})"

    def _visit_member_access(self, node: ast.Node):
        obj = self._visit(node.children[0])
        return f"{obj}.{node.value}"

    _MODULE_MAP = {
        "json": "json_",
    }

    def _visit_import(self, node: ast.Node):
        name = node.value
        module_name = self._MODULE_MAP.get(name, name)
        self._stdlib_imports.add(f"import cobra.stdlib.{module_name} as {name}")

    def _visit_block(self, node: ast.Node):
        for child in node.children:
            result = self._visit(child)
            if result is not None:
                self.emit(f"{result}")

    def _visit_binary_op(self, node: ast.Node):
        left = self._visit(node.children[0])
        right = self._visit(node.children[1])
        op_map = {"and": " and ", "or": " or ", "=": " == ", "==": " == ", "!=": " != ",
                   "<": " < ", ">": " > ", "<=": " <= ", ">=": " >= "}
        op = op_map.get(node.op, f" {node.op} ")
        return f"({left}{op}{right})"

    def _visit_unary_op(self, node: ast.Node):
        expr = self._visit(node.children[0])
        if node.op == "not":
            return f"(not {expr})"
        return f"({node.op}{expr})"

    def _visit_int(self, node: ast.Node):
        return str(node.value)

    def _visit_float(self, node: ast.Node):
        return str(node.value)

    def _visit_string(self, node: ast.Node):
        return repr(node.value)

    def _visit_bool(self, node: ast.Node):
        return "True" if node.value else "False"

    def _visit_identifier(self, node: ast.Node):
        return node.value

    def _visit_group(self, node: ast.Node):
        return f"({self._visit(node.children[0])})"
