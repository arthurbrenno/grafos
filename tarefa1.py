from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence

@dataclass(frozen=True)
class Vertice:
    nome: str
    relations: Sequence[Vertice]
    

@dataclass(frozen=True)
class Aresta:
    peso: float


@dataclass(frozen=True)
class Grafo:
    grafo: dict[Vertice, set[str]] = field(default_factory=dict)

    def criar_vertice(self, vertice: Vertice) -> None:
        self.grafo[vertice] = set({})

    def adicionar_aresta(self, origem: Vertice, destino: Vertice) -> None:
        self.grafo[origem].add(destino)
        self.grafo[destino].add(origem)

    def listar_vizinhos(self, vertice: str) -> Sequence[str]:
        return self.grafo.get(vertice)
