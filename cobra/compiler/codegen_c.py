from cobra.compiler import ast


class CodegenCError(Exception):
    pass


RUNTIME_HEADER = """\
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static char* cobra_str_concat(const char* a, const char* b) {
    size_t len = strlen(a) + strlen(b) + 1;
    char* result = (char*)malloc(len);
    if (result) { strcpy(result, a); strcat(result, b); }
    return result;
}

static char* cobra_double_to_str(double x) {
    char buf[64];
    if (x == (int)x) {
        snprintf(buf, sizeof(buf), "%d", (int)x);
    } else {
        snprintf(buf, sizeof(buf), "%g", x);
    }
    return strdup(buf);
}

static char* cobra_bool_to_str(int x) {
    return strdup(x ? "true" : "false");
}
"""

STRING_FUNCS = {"str", "input", "cobra_str_from_double", "cobra_str_concat", "cobra_bool_to_str"}


def _is_number_node(node: ast.Node) -> bool:
    t = node.type
    if t in (ast.NodeType.INT, ast.NodeType.FLOAT):
        return True
    if t == ast.NodeType.BINARY_OP:
        return all(_is_number_node(c) for c in node.children)
    if t == ast.NodeType.UNARY_OP:
        return _is_number_node(node.children[0])
    if t == ast.NodeType.CALL:
        return node.value not in STRING_FUNCS
    if t == ast.NodeType.IDENTIFIER:
        return True
    if t == ast.NodeType.GROUP:
        return _is_number_node(node.children[0])
    return False


class CodegenC:
    def __init__(self):
        self.indent_level = 0
        self.output = []
        self._in_func = False
        self._has_return = False

    def indent(self):
        return "    " * self.indent_level

    def emit(self, line: str = ""):
        self.output.append(self.indent() + line)

    def generate(self, node: ast.Node) -> str:
        self.output = []
        self.emit(RUNTIME_HEADER)
        self._visit(node)
        return "\n".join(self.output)

    def _visit(self, node: ast.Node):
        method = f"_visit_{node.type.name.lower()}"
        visitor = getattr(self, method, None)
        if visitor is None:
            raise CodegenCError(f"No C codegen visitor for {node.type}")
        return visitor(node)

    def _visit_program(self, node: ast.Node):
        func_defs = [c for c in node.children if c.type == ast.NodeType.FUNC]
        main_stmts = [c for c in node.children if c.type != ast.NodeType.FUNC]
        for fd in func_defs:
            self._visit(fd)
        self.emit("int main(int argc, char** argv) {")
        self.indent_level += 1
        self.emit('(void)argc; (void)argv;')
        for stmt in main_stmts:
            result = self._visit(stmt)
            if result is not None:
                self.emit(f"{result};")
        self.emit("return 0;")
        self.indent_level -= 1
        self.emit("}")

    def _visit_print(self, node: ast.Node):
        val = self._visit(node.children[0])
        if _is_number_node(node.children[0]):
            self.emit(f'printf("%s\\n", cobra_double_to_str({val}));')
        else:
            self.emit(f'printf("%s\\n", {val});')

    def _visit_let(self, node: ast.Node):
        var = node.value
        val = self._visit(node.children[0])
        if _is_number_node(node.children[0]):
            self.emit(f"double {var} = {val};")
        else:
            self.emit(f"char* {var} = {val};")

    def _visit_assign(self, node: ast.Node):
        var = node.value
        val = self._visit(node.children[0])
        self.emit(f"{var} = {val};")

    def _visit_if(self, node: ast.Node):
        cond = self._visit(node.children[0])
        self.emit(f"if ({cond}) {{")
        self.indent_level += 1
        self._visit(node.children[1])
        self.indent_level -= 1
        if len(node.children) > 2:
            self.emit("} else {")
            self.indent_level += 1
            self._visit(node.children[2])
            self.indent_level -= 1
        self.emit("}")

    def _visit_while(self, node: ast.Node):
        cond = self._visit(node.children[0])
        self.emit(f"while ({cond}) {{")
        self.indent_level += 1
        self._visit(node.children[1])
        self.indent_level -= 1
        self.emit("}")

    def _visit_for(self, node: ast.Node):
        var = node.value
        start = self._visit(node.children[0])
        end = self._visit(node.children[1])
        self.emit(f"for (double {var} = {start}; {var} < {end}; {var}++) {{")
        self.indent_level += 1
        self._visit(node.children[2])
        self.indent_level -= 1
        self.emit("}")

    def _visit_func(self, node: ast.Node):
        name, params = node.value
        self._in_func = True
        self._has_return = False
        param_str = ", ".join(f"double {p}" for p in params)
        self.emit(f"double {name}({param_str}) {{")
        self.indent_level += 1
        self._visit(node.children[0])
        if not self._has_return:
            self.emit("return 0;")
        self.indent_level -= 1
        self.emit("}")
        self._in_func = False

    def _visit_return(self, node: ast.Node):
        val = self._visit(node.children[0])
        self._has_return = True
        self.emit(f"return {val};")

    def _visit_call(self, node: ast.Node):
        name = node.value
        args = [self._visit(c) for c in node.children]
        if name == "print":
            if args:
                if _is_number_node(node.children[0]):
                    return f'printf("%s\\n", cobra_double_to_str({args[0]}))'
                return f'printf("%s\\n", {args[0]})'
            return 'printf("\\n")'
        if name == "str":
            return f"cobra_double_to_str({args[0]})" if args else 'strdup("")'
        return f"{name}({', '.join(args)})"

    def _visit_member_access(self, node: ast.Node):
        obj = self._visit(node.children[0])
        return f"{obj}.{node.value}"

    def _visit_import(self, node: ast.Node):
        pass

    def _visit_block(self, node: ast.Node):
        for child in node.children:
            result = self._visit(child)
            if result is not None and child.type in (ast.NodeType.CALL,):
                self.emit(f"{result};")

    def _visit_binary_op(self, node: ast.Node):
        left = self._visit(node.children[0])
        right = self._visit(node.children[1])
        is_num = _is_number_node(node.children[0]) and _is_number_node(node.children[1])
        if node.op == "+":
            if is_num:
                return f"({left} + {right})"
            if _is_number_node(node.children[0]):
                left = f"cobra_double_to_str({left})"
            if _is_number_node(node.children[1]):
                right = f"cobra_double_to_str({right})"
            return f"cobra_str_concat({left}, {right})"
        op_map = {
            "-": " - ", "*": " * ", "/": " / ",
            "==": " == ", "!=": " != ", "<": " < ", ">": " > ",
            "<=": " <= ", ">=": " >= ",
            "and": " && ", "or": " || ",
        }
        op = op_map.get(node.op)
        if op is None:
            return f"({left} {node.op} {right})"
        return f"({left}{op}{right})"

    def _visit_unary_op(self, node: ast.Node):
        expr = self._visit(node.children[0])
        if node.op == "-":
            return f"(-{expr})"
        if node.op == "not":
            return f"(!{expr})"
        return f"({node.op}{expr})"

    def _visit_int(self, node: ast.Node):
        return str(node.value)

    def _visit_float(self, node: ast.Node):
        return str(node.value)

    def _visit_string(self, node: ast.Node):
        return f'"{node.value}"'

    def _visit_bool(self, node: ast.Node):
        return "1" if node.value else "0"

    def _visit_identifier(self, node: ast.Node):
        return node.value

    def _visit_group(self, node: ast.Node):
        return f"({self._visit(node.children[0])})"
