from dataclasses import dataclass, field
from typing import Sequence

@dataclass
class Grafo:
    grafo: dict[str, set[str]] = field(default_factory=dict)

    def criar_vertice(self, vertice: str) -> None:
        self.grafo[vertice] = set({})

    def adicionar_aresta(self, origem: str, destino: str) -> None:
        self.grafo[origem].add(destino)
        self.grafo[destino].add(origem)

    def listar_vizinhos(self, vertice: str) -> Sequence[str]:
        return self.grafo.get(vertice)

g = Grafo()
g.criar_vertice("A")
g.criar_vertice("B")
g.criar_vertice("C")
g.criar_vertice("D")
g.adicionar_aresta(origem="A", destino="B")
g.adicionar_aresta(origem="A", destino="C")
g.adicionar_aresta(origem="A", destino="D")
g.adicionar_aresta(origem="B", destino="D")

print(g.listar_vizinhos("A"))
