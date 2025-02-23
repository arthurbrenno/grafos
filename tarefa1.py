from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True)
class Vertice:
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())
    nome: str


@dataclass(frozen=True)
class Arco:
    peso: float = field(default=1.0)


@dataclass(frozen=True)
class Grafo:
    """
    Grafo:
    Uma tripla ordenada (N, a g), em que

    N = um conjunto nao vazio de nós (vertices)
    A = um conjunto de arcos (arestas)
    """

    grafo: dict[Vertice, dict[Vertice, tuple[Vertice, Arco]]] = field(
        default_factory=dict
    )

    def g(self, *_ns: tuple[Vertice, Vertice, float]) -> None:
        """Uma função que associa cada arco a um
        par nao ordenado (x-y) de nós."""
        for v1, v2, peso in _ns:
            self.grafo.update({v1: {v2: (v2, Arco(peso=peso))}})
            if v2 not in self.grafo.keys():
                self.grafo.update({v2: {}})

    # TODO(arthur): implementar matriz adjacencia.
    # Vou usar algo de combinatoria, a matriz adjacencia
    # e uma matriz quadrada nxn. Vai repetir muita coisa
    def obter_arco(self, v1: Vertice, v2: Vertice, /) -> Arco:
        arco = self.grafo[v1][v2][1]
        return arco

    def existe_arco_entre(self, v1: Vertice, v2: Vertice, /) -> bool: ...

    def mostrar_matriz_adjacencia(self) -> None:
        vertices_unicos = self.grafo.keys()
        for vertice in vertices_unicos:
            print(f"{vertice.nome}  ", end="")


A = Vertice(nome="A")
B = Vertice(nome="B")

grafo = Grafo()
grafo.g((A, B, 1))
grafo.mostrar_matriz_adjacencia()
print(grafo.obter_arco(A, B))
