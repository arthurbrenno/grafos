from __future__ import annotations

from collections.abc import Iterator, ValuesView
from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Vertice:
    nome: str

    def __format__(self, format_spec: str) -> str:
        """
        Format vertex according to format_spec:
        - 'n' or '' -> just the name
        - 'f' -> full representation (name and id)
        - 'i' -> just the id
        - number (e.g. '3') -> name padded to specified width

        Examples:
            "{vertex:n}" -> "A"
            "{vertex:f}" -> "A (id=123e4567-...)"
            "{vertex:i}" -> "123e4567-..."
            "{vertex:3}" -> "A  "  # padded to width 3
            "{vertex}" -> "A"
        """
        # Try to interpret as width specification
        try:
            width = int(format_spec)
            return f"{self.nome:{width}}"
        except ValueError:
            # Handle other format codes
            if not format_spec or format_spec == "n":
                return self.nome
            elif format_spec == "f":
                return f"{self.nome}"
            elif format_spec == "i":
                return self.nome
            else:
                raise ValueError(f"Unknown format code '{format_spec}' for Vertice")


@dataclass(frozen=True)
class Arco:
    peso: float = field(default=1.0)


@dataclass(frozen=True)
class ListaDeVertices:
    vertices: set[Vertice] = field(default_factory=set)

    def criar(self, _v: Vertice, /) -> None:
        self.vertices.add(_v)

    def __iter__(self) -> Iterator:
        for el in self.vertices:
            yield el


@dataclass(frozen=True)
class MapaDeArcos:
    arcos: dict[tuple[Vertice, Vertice], Arco] = field(default_factory=dict)

    def criar(self, v1: Vertice, v2: Vertice, arco: Arco) -> None:
        self.arcos[(v1, v2)] = arco

    def values(self) -> ValuesView[Arco]:
        return self.arcos.values()

    def __set_item__(self, key: tuple[Vertice, Vertice], new_val: Arco) -> None:
        self.arcos[key] = new_val


@dataclass(frozen=True)
class Grafo:
    vertices: ListaDeVertices = field(default_factory=ListaDeVertices)
    arcos: MapaDeArcos = field(default_factory=MapaDeArcos)

    def g(self, *_to: tuple[Vertice, Vertice, Arco]) -> None:
        for v1, v2, arco in _to:
            self.vertices.criar(v1)
            self.vertices.criar(v2)
            self.arcos.criar(v1, v2, arco=arco)
            self.arcos.criar(v2, v1, arco=arco)

    def mostrar_matriz_adjacencia(self) -> None:
        """
        Mostra a matriz de adjacência do grafo de forma legível e bem formatada.

        A matriz é exibida com rótulos das linhas e colunas, onde:
        - Os vértices são mostrados em ordem alfabética
        - Os pesos das arestas são mostrados com 1 casa decimal
        - 'null' indica ausência de aresta
        - O layout inclui linhas divisórias para melhor legibilidade
        """
        # Obtém lista ordenada de vértices
        vertices_ordenados = sorted(list(self.vertices))
        n = len(vertices_ordenados)

        if n == 0:
            print("\n=== Matriz de Adjacência ===")
            print("Grafo vazio")
            return

        # Calcula a largura máxima necessária para os rótulos e valores
        largura_rotulo = max(len(v.nome) for v in vertices_ordenados)
        largura_valor = max(4, len("null"))  # Maior entre 4 e len("null")

        # Imprime título
        print("\n=== Matriz de Adjacência ===")

        # Imprime cabeçalho
        print(" " * (largura_rotulo + 1), end="")
        for v in vertices_ordenados:
            print(f"{v.nome:^{largura_valor}}", end=" ")
        print()

        # Imprime linha separadora do cabeçalho
        print("=" * (largura_rotulo + 1) + "+" + "=" * ((largura_valor + 1) * n - 1))

        # Imprime linhas da matriz
        for v1 in vertices_ordenados:
            print(f"{v1.nome:<{largura_rotulo}}", end=" │")
            for v2 in vertices_ordenados:
                arco = self.arcos.arcos.get((v1, v2))
                valor = f"{arco.peso:.1f}" if arco else "null"
                print(f"{valor:^{largura_valor}}", end=" ")
            print()

            # Imprime linha separadora entre linhas da matriz (exceto após a última)
            if v1 != vertices_ordenados[-1]:
                print(
                    "-" * (largura_rotulo + 1)
                    + "+"
                    + "-" * ((largura_valor + 1) * n - 1)
                )

        # Imprime linha final
        print("=" * (largura_rotulo + 1) + "+" + "=" * ((largura_valor + 1) * n - 1))


# Exemplo de uso
grafo = Grafo()

v1 = Vertice("A")
v2 = Vertice("B")
v3 = Vertice("C")

grafo.vertices.criar(v3)
grafo.g((v1, v2, Arco(peso=1)))

grafo.mostrar_matriz_adjacencia()
