import egglog.bindings as eggbnd


def tuple_fun(name):
    def res(*args):
        return (name, *args)

    return res


def tuple2sexp(tup):
    return "(" + " ".join(tup) + ")"


def sexp_fun(name):
    def res(*args):
        return f"({name} {' '.join(args)})"

    return res


@dataclass
class Sort:
    name: str


IntSort = lambda: Sort("i64")
BoolSort = lambda: Sort("bool")
StringSort = lambda: Sort("string")
FloatSort = lambda: Sort("f64")
UnitSort = lambda: Sort("unit")


@dataclass
class Expr:
    expr: str


def Int(x):
    assert isinstance(x, int)
    return Expr(str(x))


class Solver:
    def __init__(self):
        self.egraph = eggbnd.EGraph()

    def parse_run(self, expr):
        cmds = self.egraph.parse(tuple2sexp(expr))
        return self.egraph.run_program(cmds)

    def Sort(self, name):
        self.parse_run(f"(Sort {name})")
        return Sort(name)

    def Relation(self, name, *args):
        self.parse_run(f"(relation {name} {' '.join(args)})")
        return sexp_fun(name)

    def Function(self, name, *args):
        output = args[-1]
        input = args[:-1]
        schema = eggbnd.Schema(input, output)
        self.run_command(self.self, name, args)
        return sexp_fun(name)

    def extract(self, expr):
        return self.run_program(eggbnd.Extract(expr))

    def add_rw(self, lhs, rhs):
        return self.parse_run(f"(rw {lhs} {rhs})")

    def add_rule(self, head, body):
        pass


# Hmm. Maybe Saul is on point.

# possibly a bad idea
__global_solver = Solver()
Function = __global_solver.Function
Relation = __global_solver.Relation
Sort = __global_solver.Sort
