class Grafo:
    def __init__(self):
        self.grafo = {}

    def add_aresta(self, v1, v2):
        if v1 not in self.grafo:
            self.grafo[v1] = []

        if v2 not in self.grafo:
            self.grafo[v2] = []

        self.grafo[v1].append(v2)
        self.grafo[v2].append(v1)

    def eh_conexo(): ...

    def eh_ciclico(): ...

    def eh_plano(): ...


g = Grafo()

g.add_aresta("A", "B")
print(g.grafo)
