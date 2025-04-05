class Grafo:
    def __init__(self):
        self.adjacencias = {}

    def add_aresta(self, v1, v2):
        vertices_do_grafo = self.adjacencias.keys()

        if v1 not in vertices_do_grafo:
            self.adjacencias[v1] = set([])

        if v2 not in vertices_do_grafo:
            self.adjacencias[v2] = set([])

        self.adjacencias[v1].add(v2)
        self.adjacencias[v2].add(v1)

    def calcular_ordem(self):
        vertices_do_grafo = self.adjacencias.keys()
        quantidade_vertices = len(vertices_do_grafo)
        return quantidade_vertices

    def calcular_tamanho(self):
        return sum(len(v) for v in self.adjacencias.values()) // 2


g = Grafo()

g.add_aresta("a", "b")
g.add_aresta("b", "c")
g.add_aresta("c", "a")
g.add_aresta("a", "d")
g.add_aresta("c", "d")

print(g.calcular_tamanho())
