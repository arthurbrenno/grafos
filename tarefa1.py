"""
Módulo Grafo
============

Este módulo fornece classes e métodos para criar e manipular grafos não dirigidos com arestas ponderadas.

Classes Principais
------------------

- `Vertice`: Representa um vértice no grafo.
- `Arco`: Representa uma aresta (arco) ponderada entre dois vértices.
- `ListaDeVertices`: Uma coleção de vértices, armazenados em um conjunto para garantir unicidade.
- `MapaDeArcos`: Um mapa de arcos entre pares de vértices, armazenados em um dicionário.
- `Grafo`: Representa o grafo completo, contendo vértices e arcos.

Uso Básico
----------

Para criar um grafo, instancie a classe `Grafo` e use o método `g` para adicionar vértices e arcos. Você pode visualizar a matriz de adjacência do grafo chamando o método `mostrar_matriz_adjacencia`.

Exemplo:

.. code-block:: python

    grafo = Grafo()
    v1 = Vertice("A")
    v2 = Vertice("B")
    arco = Arco(peso=1.5)
    grafo.g((v1, v2, arco))
    grafo.mostrar_matriz_adjacencia()

Detalhes das Classes
--------------------

- `Vertice`: Imutável e ordenável pelo nome. Pode ser formatado de várias maneiras usando o método `__format__`.
- `Arco`: Imutável, contém o peso da aresta.
- `ListaDeVertices`: Permite adicionar vértices e iterar sobre eles.
- `MapaDeArcos`: Permite adicionar arcos entre vértices e acessar os arcos existentes.
- `Grafo`: Gerencia a coleção de vértices e o mapa de arcos, permitindo a construção do grafo e a visualização da matriz de adjacência.

Para mais detalhes sobre cada classe e seus métodos, consulte as docstrings individuais.

"""

from __future__ import annotations

import os
from collections.abc import Iterator, ValuesView
from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Vertice:
    """
    Representa um vértice em um grafo.

    Esta classe é imutável (frozen) e pode ser ordenada com base no atributo 'nome'.

    Atributos:
        nome (str): O nome único do vértice.
    """

    nome: str

    def __format__(self, format_spec: str) -> str:
        """
        Formata o vértice de acordo com a especificação de formato fornecida.

        Especificações de formato suportadas:
            - 'n' ou '' (vazio): Retorna apenas o nome do vértice.
            - 'f': Retorna uma representação completa (nome e id).
            - 'i': Retorna apenas o id do vértice (neste caso, igual ao nome).
            - Um número (ex: '3'): Retorna o nome do vértice com padding para a largura especificada.

        Parâmetros:
            format_spec (str): A especificação de formato a ser usada.

        Retorna:
            str: A representação formatada do vértice.

        Levanta:
            ValueError: Se a especificação de formato for desconhecida.

        Exemplos:
            >>> v = Vertice("A")
            >>> f"{v:n}"  # ou f"{v}"
            'A'
            >>> f"{v:f}"
            'A (id=A)'
            >>> f"{v:i}"
            'A'
            >>> f"{v:3}"
            'A  '  # padded to width 3
        """
        try:
            width = int(format_spec)
            return f"{self.nome:{width}}"
        except ValueError:
            if not format_spec or format_spec == "n":
                return self.nome
            elif format_spec == "f":
                return f"{self.nome} (id={self.nome})"
            elif format_spec == "i":
                return self.nome
            else:
                raise ValueError(f"Unknown format code '{format_spec}' for Vertice")


@dataclass(frozen=True)
class Arco:
    """
    Representa uma aresta (arco) entre dois vértices em um grafo.

    Esta classe é imutável (frozen).

    Atributos:
        peso (float): O peso da aresta. Valor padrão é 1.0.
    """

    peso: float = field(default=1.0)

    def __add__(self) -> Arco:
        """Overload para representar a soma de dois arcos.

        Returns:
            Arco: O novo arco com os pesos somados
        """


@dataclass
class ListaDeVertices:
    """
    Representa uma coleção de vértices em um grafo.

    Utiliza um conjunto para armazenar os vértices, garantindo unicidade.

    Atributos:
        vertices (set[Vertice]): Conjunto de vértices.
    """

    vertices: set[Vertice] = field(default_factory=set)

    def criar(self, _v: Vertice, /) -> None:
        """
        Adiciona um vértice à coleção.

        Parâmetros:
            _v (Vertice): O vértice a ser adicionado (parâmetro apenas posicional).

        Retorna:
            None

        Exemplo:
            >>> lista = ListaDeVertices()
            >>> v = Vertice("A")
            >>> lista.criar(v)
            >>> len(lista.vertices)
            1
        """
        self.vertices.add(_v)

    def __iter__(self) -> Iterator:
        """
        Retorna um iterador sobre os vértices na coleção.

        Retorna:
            Iterator: Um iterador sobre os vértices.

        Exemplo:
            >>> lista = ListaDeVertices()
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("B")
            >>> lista.criar(v1)
            >>> lista.criar(v2)
            >>> for v in lista:
            ...     print(v.nome)
            A
            B
        """
        for el in self.vertices:
            yield el

    def __contains__(self, item: Vertice) -> bool:
        return item in self.vertices

    def __len__(self) -> int:
        """Retorna o tamanho da lista de vertices

        Returns:
            int: O tamanho da lista de vertices
        """
        return len(self.vertices)


@dataclass
class MapaDeArcos:
    """
    Representa um mapa de arestas (arcos) entre pares de vértices em um grafo.

    Utiliza um dicionário para armazenar os arcos, com chaves sendo tuplas de vértices.

    Atributos:
        arcos (dict[tuple[Vertice, Vertice], Arco]): Dicionário de arcos.
    """

    arcos: dict[tuple[Vertice, Vertice], Arco] = field(default_factory=dict)

    def criar(self, v1: Vertice, v2: Vertice, arco: Arco) -> None:
        """
        Adiciona um arco entre dois vértices.

        Parâmetros:
            v1 (Vertice): O primeiro vértice.
            v2 (Vertice): O segundo vértice.
            arco (Arco): O arco a ser associado aos vértices.

        Retorna:
            None

        Exemplo:
            >>> mapa = MapaDeArcos()
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("B")
            >>> arco = Arco(peso=2.5)
            >>> mapa.criar(v1, v2, arco)
            >>> mapa.arcos[(v1, v2)].peso
            2.5
        """
        self.arcos[(v1, v2)] = arco

    def values(self) -> ValuesView[Arco]:
        """
        Retorna uma visão dos valores (arcos) no dicionário.

        Retorna:
            ValuesView[Arco]: Uma visão dos arcos armazenados.

        Exemplo:
            >>> mapa = MapaDeArcos()
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("B")
            >>> arco = Arco(peso=2.5)
            >>> mapa.criar(v1, v2, arco)
            >>> for a in mapa.values():
            ...     print(a.peso)
            2.5
        """
        return self.arcos.values()

    def __get_item__(self, item: tuple[Vertice, Vertice]) -> Arco:
        return self.arcos[item]

    def __set_item__(self, key: tuple[Vertice, Vertice], new_val: Arco) -> None:
        """
        Define um novo valor para um arco específico.

        Parâmetros:
            key (tuple[Vertice, Vertice]): A chave representando o par de vértices.
            new_val (Arco): O novo arco a ser associado.

        Retorna:
            None

        Exemplo:
            >>> mapa = MapaDeArcos()
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("B")
            >>> arco1 = Arco(peso=1.0)
            >>> arco2 = Arco(peso=2.0)
            >>> mapa.criar(v1, v2, arco1)
            >>> mapa.__set_item__((v1, v2), arco2)
            >>> mapa.arcos[(v1, v2)].peso
            2.0
        """
        self.arcos[key] = new_val

    def __contains__(self, item: tuple[Vertice, Vertice]) -> bool:
        return item in self.arcos


def g(grafo: Grafo, *_to: tuple[Vertice, Vertice, Arco]) -> None:
    """
    Adiciona vértices e arcos ao grafo a partir de uma lista de tuplas.

    Cada tupla deve conter dois vértices e um arco. O método adiciona os vértices
    à coleção de vértices e cria arcos bidirecionais entre eles.

    Parâmetros:
        *_to (tuple[Vertice, Vertice, Arco]): Tuplas contendo v1, v2 e arco.

    Retorna:
        None

    Exemplo:
        >>> grafo = Grafo()
        >>> v1 = Vertice("A")
        >>> v2 = Vertice("B")
        >>> arco = Arco(peso=1.5)
        >>> grafo.g((v1, v2, arco))
        >>> len(grafo.vertices)
        2
        >>> grafo.arcos.arcos[(v1, v2)].peso
        1.5
    """
    for v1, v2, arco in _to:
        grafo.vertices.criar(v1)
        grafo.vertices.criar(v2)
        grafo.arcos.criar(v1, v2, arco)
        grafo.arcos.criar(v2, v1, arco)


@dataclass(frozen=True)
class Grafo:
    """
    Uma tripla ordenada (N, A, g) em que:
    N: Um conjunto não vazio de nós
    A: Um conjunto de arcos (arestas)
    g: Uma função que associa cada arco `a` a um par ordenado x-y de nós,
    chamados de extremidades de `a`.

    Atributos:
        vertices (ListaDeVertices): A coleção de vértices do grafo.
        arcos (MapaDeArcos): O mapa de arcos do grafo.

    Exemplo:
            >>> grafo = Grafo()
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("B")
            >>> arco = Arco(peso=1.5)
            >>> grafo.g((v1, v2, arco))
            >>> grafo.calcular_comprimento(v1, v2)
            1.5
    """

    vertices: ListaDeVertices = field(default_factory=ListaDeVertices)
    arcos: MapaDeArcos = field(default_factory=MapaDeArcos)

    def mostrar_matriz_adjacencia(self, clear_screen: bool = False) -> None:
        """
        Mostra a matriz de adjacência do grafo de forma legível e bem formatada.

        A matriz é exibida com rótulos das linhas e colunas, onde:
        - Os vértices são mostrados em ordem alfabética
        - Os pesos das arestas são mostrados com 1 casa decimal
        - 'null' indica ausência de aresta
        - O layout inclui linhas divisórias para melhor legibilidade

        Retorna:
            None

        Exemplo:
            >>> grafo = Grafo()
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("B")
            >>> arco = Arco(peso=1.0)
            >>> grafo.g((v1, v2, arco))
            >>> grafo.mostrar_matriz_adjacencia()
            === Matriz de Adjacência ===
                A    B
            A  │null 1.0
            ----+---------
            B  │1.0  null
            ====+=
        """
        if clear_screen:
            os.system("cls" if os.name == "nt" else "clear")

        vertices_ordenados = sorted(list(self.vertices.vertices))
        n = len(vertices_ordenados)

        if n == 0:
            print("\n=== Matriz de Adjacência ===")
            print("Grafo vazio")
            return

        largura_rotulo = max(len(v.nome) for v in vertices_ordenados)
        largura_valor = max(4, len("null"))

        print("\n=== Matriz de Adjacência ===")
        print(" " * (largura_rotulo + 1), end="")
        for v in vertices_ordenados:
            print(f"{v.nome:^{largura_valor}}", end=" ")
        print()

        print("=" * (largura_rotulo + 1) + "+" + "=" * ((largura_valor + 1) * n - 1))

        for v1 in vertices_ordenados:
            print(f"{v1.nome:<{largura_rotulo}}", end=" │")
            for v2 in vertices_ordenados:
                arco = self.arcos.arcos.get((v1, v2))
                valor = f"{arco.peso:.1f}" if arco else "null"
                print(f"{valor:^{largura_valor}}", end=" ")
            print()

            if v1 != vertices_ordenados[-1]:
                print(
                    "-" * (largura_rotulo + 1)
                    + "+"
                    + "-" * ((largura_valor + 1) * n - 1)
                )

        print("=" * (largura_rotulo + 1) + "+" + "=" * ((largura_valor + 1) * n - 1))


@dataclass(frozen=True)
class CalculadoraDeGrafos:
    grafo: Grafo

    def calcular_soma_pesos(self, v1: Vertice, v2: Vertice) -> tuple[int, ...]:
        """Calcula a soma de todos os pesos possiveis entre dois vertices do grafo

        Args:
            v1 (Vertice): Ponto de partida
            v2 (Vertice): Ponto de chegada

        Returns:
            tuple[int, ...]: retorna uma tupla com todos a soma de cada peso possivel.
        """

    def calcular_soma_comprimentos(self, v1: Vertice, v2: Vertice) -> tuple[int, ...]:
        """Calcula todos os comprimentos possiveis entre dois vertices do grafo

        Args:
            v1 (Vertice): Ponto de partida
            v2 (Vertice): Ponto de chegada

        Returns:
            tuple[int, ...]: retorna uma tupla com todos os comprimentos possiveis.
        """


# Exemplo de uso
grafo = Grafo()

v1 = Vertice("A")
v2 = Vertice("B")
v3 = Vertice("C")

grafo.vertices.criar(v3)
g(grafo, (v1, v2, Arco()))

grafo.mostrar_matriz_adjacencia(clear_screen=True)

calculadora = CalculadoraDeGrafos(grafo)
print(calculadora.calcular_soma_comprimentos(v1, v2))
