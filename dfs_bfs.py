from collections.abc import Callable, ItemsView, KeysView


class Graph:
    graph: dict[str, list[tuple[str, float]]]

    def __init__(self) -> None:
        self.graph = {}

    def add_aresta(self, o: str, d: str, p: float) -> None:
        if o not in self.graph.keys():
            self.graph[o] = []

        if d not in self.graph.keys():
            self.graph[d] = []

        self.graph[o].append((d, p))
        self.graph[d].append((o, p))

    def items(self) -> ItemsView[str, list[tuple[str, float]]]:
        return self.graph.items()

    def keys(self) -> KeysView[str]:
        return self.graph.keys()

    def __getitem__(self, key: str) -> list[tuple[str, float]]:
        value = self.graph[key]
        return value

    def __str__(self) -> str:
        return str(self.graph)



def w(g: Graph, v1: str, v2: str) -> float:
    neighbors = g[v1]
    for neighbor in neighbors:
        if neighbor[0] == v2:
            return neighbor[1]

    raise RuntimeError("Nenhum vertice adjacente foi encontrado.")


def EXTRACT_MIN(Q: list[str]) -> str:
    min = Q[0]
    for u in Q:
        if u < min:
            min = u

    
    idx = Q.index(min)
    Q.pop(idx)

    return min


def prim(g: Graph, w: Callable[[Graph, str, str], float], r: str) -> Graph:
    key: dict[str, float] = {}
    pai: dict[str, str | None] = {}

    for u in g.keys():
        key[u] = float("inf")
        pai[u] = None

    key[r] = 0
    Q: list[str] = list(g.keys())
    while len(Q) != 0:
        u = EXTRACT_MIN(Q)
        for v in g[u]:
            if v[0] in Q and w(g, u, v[0]) < key[v[0]]:
                pai[v[0]] = u
                key[v[0]] = w(g, u, v[0])

    new_graph = Graph()
    for vertice, vertice_pai in pai.items():
        if vertice_pai is None:
            continue

        new_graph.add_aresta(vertice, vertice_pai, key[vertice])

    return new_graph


g = Graph()
g.add_aresta("a", "b", 2.0)
g.add_aresta("b", "c", 5.0)
g.add_aresta("c", "a", 3.0)
g.add_aresta("c", "d", 4.0)
g.add_aresta("d", "b", 1.0)

r = "a"

mst = prim(g, w, r)
print(mst)
