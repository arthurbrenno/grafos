"""
Implemente uma classe em Python para representar um grafo n ˜ ao-direcionado utilizando uma lista de ad-
jac ˆ encias. A classe deve permitir:
• Calcular tamanho do grafo.
• Determinar o grau de cada v ´ ertice.
"""

"""
A: B
B: A
C: B

"""


class Grafo:
    def __init__(self):
        self.grafo = {}

    def add_aresta(self, v1, v2):
        vertices_do_grafo = self.grafo.keys()
        
        if v1 not in vertices_do_grafo:
            self.grafo[v1] = []

        if v2 not in vertices_do_grafo:
            self.grafo[v2] = []

        self.grafo[v1].add(v2)
        self.grafo[v2].add(v1)

    def calcular_ordem(self):
        vertices_do_grafo = self.grafo.keys()
        return len(vertices_do_grafo)

    def calcular_tamanho(self):
        return len(self.grafo.items())


g = Grafo()

g.add_aresta("a", "b")
g.add_aresta("b", "c")
g.add_aresta("c", "a")
g.add_aresta("a", "d")

print(g.calcular_tamanho())
