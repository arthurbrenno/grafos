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

Para criar um grafo, instancie a classe `Grafo` e use o método `g` para adicionar vértices e arcos.
Você pode visualizar a matriz de adjacência do grafo chamando o método `mostrar_matriz_adjacencia`.
Para uma visualização gráfica interativa, use o método `visualizar_grafo`.

Exemplo:

.. code-block:: python

    grafo = Grafo()
    v1 = Vertice("A")
    v2 = Vertice("B")
    arco = Arco(peso=1.5)
    grafo.g((v1, v2, arco))
    grafo.mostrar_matriz_adjacencia()
    grafo.visualizar_grafo()  # Visualização gráfica (requer pyvis e PyQt5)

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

import importlib
import importlib.util
import logging
import logging.config
import os
import sys
import tempfile
import timeit
from collections.abc import Iterator, MutableSequence, MutableSet, Sequence, ValuesView
from dataclasses import dataclass, field
from typing import Literal

type PesoArco = float

# region logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
# endregion

# region imports condicionais
# Tenta importar pyvis para visualização do grafo
pyvis = importlib.util.find_spec("pyvis")
if pyvis:
    PYVIS_AVAILABLE = True
else:
    logger.debug("AVISO: pyvis não encontrado. Visualização do grafo não disponível.")
    PYVIS_AVAILABLE = False

# Tenta importar PyQt5 para exibição de janelas
try:
    from PyQt5.QtCore import QUrl
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

    PYQT5_AVAILABLE = True
except ImportError:
    logger.debug("AVISO: PyQt5 não encontrado. Visualização em janela não disponível.")
    PYQT5_AVAILABLE = False

# Tenta importar rich para pretty printing
try:
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    logger.debug("AVISO: rich não encontrado. Pretty printing não disponível.")
    RICH_AVAILABLE = False
# endregion


# region funções
def g(
    grafo: Grafo, *_to: tuple[Vertice, Vertice, PesoArco] | tuple[Vertice, Vertice]
) -> None:
    """
    Adiciona vértices e arcos ao grafo a partir de uma lista de tuplas.

    Cada tupla deve conter dois vértices e um arco. O método adiciona os vértices
    à coleção de vértices e cria arcos bidirecionais entre eles.

    Parâmetros:
        *_to (tuple[Vertice, Vertice, Arco] | tuple[Vertice, Vertice]): Tuplas contendo v1, v2 e arco.

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

    for tup in _to:
        if (v1 := tup[0]) not in grafo.vertices:
            raise ValueError(
                "O primeiro vértice não está presente no grafo."
                "Primeiro, você deve criar o vértice."
            )

        if (v2 := tup[1]) not in grafo.vertices:
            raise ValueError(
                "O segundo vértice não está presente no grafo."
                "Primeiro, você deve criar o vértice."
            )

        arco = (
            (Arco(origem=v1, destino=v2, peso=tup[2]))
            if len(tup) == 3
            else Arco(origem=v1, destino=v2, peso=1.0)
        )

        grafo.arcos.criar(v1, v2, arco)
        grafo.arcos.criar(v2, v1, arco)


def mostrar_matriz_adjacencia(grafo: Grafo, clear_screen: bool = False) -> None:
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

    vertices_ordenados = sorted(list(grafo.vertices.vertices))
    n = len(vertices_ordenados)

    if n == 0:
        print("\n=== Matriz de Adjacência ===")
        print("Grafo vazio")
        return

    # Se o rich estiver disponível, usar para exibição mais bonita
    if RICH_AVAILABLE:
        console = Console()
        table = Table(
            title="Matriz de Adjacência", show_header=True, header_style="bold"
        )

        # Adicionar cabeçalhos
        table.add_column("")
        for v in vertices_ordenados:
            table.add_column(v.id, justify="center")

        # Adicionar linhas
        for v1 in vertices_ordenados:
            row = [v1.id]
            for v2 in vertices_ordenados:
                arco = grafo.arcos.arcos.get((v1, v2))
                valor = f"{arco.peso:.1f}" if arco else "null"
                row.append(valor)
            table.add_row(*row)

        console.print(table)
        return

    # Exibição tradicional se rich não estiver disponível
    largura_rotulo = max(len(v.id) for v in vertices_ordenados)
    largura_valor = max(4, len("null"))

    print("\n=== Matriz de Adjacência ===")
    print(" " * (largura_rotulo + 1), end="")
    for v in vertices_ordenados:
        print(f"{v.id:^{largura_valor}}", end=" ")
    print()

    print("=" * (largura_rotulo + 1) + "+" + "=" * ((largura_valor + 1) * n - 1))

    for v1 in vertices_ordenados:
        print(f"{v1.id:<{largura_rotulo}}", end=" │")
        for v2 in vertices_ordenados:
            arco = grafo.arcos.arcos.get((v1, v2))
            valor = f"{arco.peso:.1f}" if arco else "null"
            print(f"{valor:^{largura_valor}}", end=" ")
        print()

        if v1 != vertices_ordenados[-1]:
            print(
                "-" * (largura_rotulo + 1) + "+" + "-" * ((largura_valor + 1) * n - 1)
            )

    print("=" * (largura_rotulo + 1) + "+" + "=" * ((largura_valor + 1) * n - 1))


# endregion


# region vertice
@dataclass(frozen=True, order=True)
class Vertice:
    """
    Representa um vértice em um grafo.

    Esta classe é imutável (frozen) e pode ser ordenada com base no atributo 'nome'.

    Atributos:
        nome (str): O nome único do vértice.
    """

    id: str
    """O identificador do vertice.
    
    Exemplos:
    >>> Vertice("A")
    """

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
            return f"{self.id:{width}}"
        except ValueError:
            if not format_spec or format_spec == "n":
                return self.id
            elif format_spec == "f":
                return f"{self.id} (id={self.id})"
            elif format_spec == "i":
                return self.id
            else:
                raise ValueError(f"Unknown format code '{format_spec}' for Vertice")


# endregion


# region arco
@dataclass(frozen=True, order=True)
class Arco:
    """
    Representa uma aresta (arco) entre dois vértices em um grafo.

    Esta classe é imutável (frozen).

    Atributos:
        peso (float): O peso da aresta. Valor padrão é 1.0.
    """

    origem: Vertice
    destino: Vertice
    peso: float = field(default=1.0)


# endregion


# region lista de vertices
@dataclass(frozen=True)
class ListaDeVertices:
    """
    Representa uma coleção de vértices em um grafo.

    Utiliza um conjunto para armazenar os vértices, garantindo unicidade.

    Atributos:
        vertices (set[Vertice]): Conjunto de vértices.
    """

    vertices: set[Vertice] = field(default_factory=set)

    def verificar_existencia(self, _v: Vertice, /) -> bool:
        """Verifica se um vertice existe dentro da lista.

        Args:
            _v (Vertice): O vertice para ser verificado

        Returns:
            bool: returna True caso exista, False caso contrário.
        """
        return _v in self.vertices

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

    def __iter__(self) -> Iterator[Vertice]:
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


# endregion


# region mapa de arcos
@dataclass(frozen=True)
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


# endregion


# region grafo
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

    def g(
        self, *args: tuple[Vertice, Vertice, PesoArco] | tuple[Vertice, Vertice]
    ) -> None:
        """
        Método wrapper para a função global g.

        Veja a documentação da função g para mais detalhes.
        """
        g(self, *args)

    def mostrar_matriz_adjacencia(self, clear_screen: bool = False) -> None:
        """
        Método wrapper para a função global mostrar_matriz_adjacencia.

        Veja a documentação da função mostrar_matriz_adjacencia para mais detalhes.
        """
        mostrar_matriz_adjacencia(self, clear_screen)

    def visualizar_grafo_navegador(
        self,
        titulo: str = "Visualização do Grafo",
        altura: int = 600,
        largura: int = 800,
    ) -> None:
        """
        Gera uma visualização do grafo e abre-a diretamente no navegador padrão.
        Essa alternativa não requer PyQt5, apenas pyvis.
        """
        # Verificar se pyvis está disponível
        if not PYVIS_AVAILABLE:
            raise ImportError(
                "A biblioteca pyvis não está instalada.\n"
                "Por favor, instale-a usando:\n"
                "pip install pyvis"
            )

        # Importar as bibliotecas necessárias
        from pyvis.network import Network
        import webbrowser
        import os

        # Criar um grafo pyvis
        net = Network(altura, largura, directed=False, notebook=False, heading=titulo)
        net.toggle_physics(True)

        # Adicionar nós ao grafo pyvis
        for vertice in self.vertices:
            net.add_node(vertice.id, label=vertice.id, title=f"Vértice: {vertice.id}")

        # Adicionar arestas únicas (sem duplicatas)
        added_edges = set()
        for (v1, v2), arco in self.arcos.arcos.items():
            edge_id = tuple(sorted([v1.id, v2.id]))
            if edge_id not in added_edges:
                net.add_edge(
                    v1.id,
                    v2.id,
                    value=arco.peso,
                    title=f"Peso: {arco.peso}",
                    label=f"{arco.peso}",
                )
                added_edges.add(edge_id)

        # Criar arquivo HTML temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        temp_file.close()
        html_path = temp_file.name

        print(f"Salvando visualização em: {html_path}")
        net.save_graph(html_path)

        # Verificar se o arquivo foi criado
        if not os.path.exists(html_path):
            print(f"Erro: O arquivo HTML não foi criado em {html_path}")
            return

        # Abrir o arquivo no navegador padrão
        print(f"Abrindo visualização no navegador: {html_path}")
        webbrowser.open("file://" + os.path.abspath(html_path))

    def pretty_print(self, titulo: str | None = None) -> None:
        """
        Exibe informações sobre o grafo de forma bem formatada,
        usando a biblioteca rich se disponível.

        Parâmetros:
            titulo (str): Título da exibição

        Retorna:
            None
        """
        titulo = titulo or "Informações do Grafo"
        if RICH_AVAILABLE:
            console = Console()

            # Seção de resumo
            resumo = Table(show_header=False, box=rich.box.SIMPLE)
            resumo.add_column("Propriedade", style="bold")
            resumo.add_column("Valor")

            vertices_count = len(self.vertices)
            arcos_count = len(
                {tuple(sorted([v1.id, v2.id])) for (v1, v2) in self.arcos.arcos.keys()}
            )

            resumo.add_row("Número de vértices", str(vertices_count))
            resumo.add_row("Número de arcos (único)", str(arcos_count))

            # Calcular peso total e médio
            pesos = [arco.peso for arco in self.arcos.arcos.values()]
            peso_total = (
                sum(pesos) / 2
            )  # Dividir por 2 pois cada aresta é contada duas vezes
            peso_medio = peso_total / arcos_count if arcos_count > 0 else 0

            resumo.add_row("Peso total das arestas", f"{peso_total:.2f}")
            resumo.add_row("Peso médio das arestas", f"{peso_medio:.2f}")

            console.print(Panel(resumo, title=titulo, border_style="green"))

            # Seção de vértices
            if vertices_count > 0:
                vertices_table = Table(
                    title="Vértices", show_header=True, box=rich.box.SIMPLE
                )
                vertices_table.add_column("ID", style="bold")
                vertices_table.add_column("Grau")
                vertices_table.add_column("Conexões")

                for v in sorted(list(self.vertices.vertices), key=lambda x: x.id):
                    # Contar conexões para este vértice
                    conexoes = []
                    grau = 0

                    for (v1, v2), arco in self.arcos.arcos.items():
                        if v1 == v:
                            conexoes.append(f"{v2.id} ({arco.peso:.1f})")
                            grau += 1

                    vertices_table.add_row(v.id, str(grau), ", ".join(conexoes))

                console.print(vertices_table)
        else:
            # Exibição tradicional sem a biblioteca rich
            print(f"\n=== {titulo} ===")
            vertices_count = len(self.vertices)
            arcos_count = len(
                {tuple(sorted([v1.id, v2.id])) for (v1, v2) in self.arcos.arcos.keys()}
            )

            print(f"Número de vértices: {vertices_count}")
            print(f"Número de arcos (único): {arcos_count}")

            # Calcular peso total e médio
            pesos = [arco.peso for arco in self.arcos.arcos.values()]
            peso_total = (
                sum(pesos) / 2
            )  # Dividir por 2 pois cada aresta é contada duas vezes
            peso_medio = peso_total / arcos_count if arcos_count > 0 else 0

            print(f"Peso total das arestas: {peso_total:.2f}")
            print(f"Peso médio das arestas: {peso_medio:.2f}")

            # Listar vértices
            if vertices_count > 0:
                print("\nVértices:")
                for v in sorted(list(self.vertices.vertices), key=lambda x: x.id):
                    # Contar conexões para este vértice
                    conexoes = []
                    grau = 0

                    for (v1, v2), arco in self.arcos.arcos.items():
                        if v1 == v:
                            conexoes.append(f"{v2.id} ({arco.peso:.1f})")
                            grau += 1

                    print(f"  {v.id} - Grau: {grau}, Conexões: {', '.join(conexoes)}")


# endregion


# region calculadora de grafo
@dataclass(frozen=True)
class CalculadoraDeGrafo:
    grafo: Grafo

    def calcular_menor_distancia_com_pesos(
        self,
        origem: Vertice,
        destino: Vertice,
        algoritmo: Literal["dijkstra"] | None = None,
    ) -> Sequence[Arco]:
        """Calcula a menor distancia entre dois vertices, considerando os pesos

        Args:
            origem (Vertice): vertice de origem
            destino (Vertice): vertice de destino
            algoritmo (Literal["dijkstra"] | None, optional): O algoritmo para ser utilizado. O valor padrão é djikstra.

        Returns:
            Sequence[Arco]: retorna a sequencia de arcos que retorna o menor caminho entre os vertices.
        """
        if algoritmo is None:
            algoritmo = "dijkstra"
        # TODO(arthur): implementar o metodo
        return -1.0

    def calcular_possibilidades_caminhos(
        self, v1: Vertice, v2: Vertice, /
    ) -> Sequence[Sequence[Arco]]:
        """
        Calcula todos os caminhos possíveis entre dois vértices no grafo.

        Esta função implementa uma busca em profundidade (DFS) para encontrar todos os caminhos
        possíveis entre o vértice de origem v1 e o vértice de destino v2. A função evita ciclos
        não visitando o mesmo vértice mais de uma vez em um único caminho.

        Args:
            v1 (Vertice): O vértice de origem (parâmetro posicional).
            v2 (Vertice): O vértice de destino (parâmetro posicional).

        Returns:
            Sequence[Sequence[Arco]]: Uma sequência de sequências, onde cada sequência interna
                                    representa um caminho possível como uma lista de arcos.
                                    Retorna uma lista vazia se não houver caminhos entre v1 e v2.

        Exemplo:
            >>> calculadora = CalculadoraDeGrafo(grafo)
            >>> v1 = Vertice("A")
            >>> v2 = Vertice("C")
            >>> caminhos = calculadora.calcular_possibilidades_caminhos(v1, v2)
            >>> len(caminhos)  # Número de caminhos possíveis
            2
        """

        # Lista para armazenar todos os caminhos encontrados
        todos_caminhos: MutableSequence[Sequence[Arco]] = []

        def dfs(
            atual: Vertice,
            destino: Vertice,
            caminho_atual: MutableSequence[Arco],
            vertices_visitados: MutableSet[Vertice],
        ) -> None:
            # Se chegamos ao destino, adicionamos o caminho atual aos resultados
            if atual == destino:
                todos_caminhos.append(list(caminho_atual))
                return

            # Marcar o vértice atual como visitado
            vertices_visitados.add(atual)

            # Explorar todos os vértices adjacentes
            for vertice in self.grafo.vertices:
                # Verificar se há um arco entre o vértice atual e o vértice candidato
                if (
                    atual,
                    vertice,
                ) in self.grafo.arcos.arcos and vertice not in vertices_visitados:
                    # Adicionar o arco ao caminho atual
                    arco = self.grafo.arcos.arcos[(atual, vertice)]
                    caminho_atual.append(arco)

                    # Continuar a busca a partir deste novo vértice
                    dfs(vertice, destino, caminho_atual, vertices_visitados)

                    # Backtracking: remover o último arco adicionado
                    caminho_atual.pop()

            # Remover o vértice atual dos visitados para permitir explorar outros caminhos
            vertices_visitados.remove(atual)

        # Verificar se os vértices existem no grafo
        if v1 not in self.grafo.vertices or v2 not in self.grafo.vertices:
            return todos_caminhos  # Retorna lista vazia se um dos vértices não existir

        # Iniciar a busca em profundidade
        dfs(v1, v2, [], set())

        return todos_caminhos

    def calcular_soma_pesos(self, v1: Vertice, v2: Vertice, /) -> Sequence[float]:
        """Calcula a soma de todos os pesos possiveis entre dois vertices do grafo

        Args:
            v1 (Vertice): Ponto de partida
            v2 (Vertice): Ponto de chegada

        Returns:
            Sequence[int]: retorna uma Sequencia com todas as somas de cada peso possivel.
        """
        possibilidades = self.calcular_possibilidades_caminhos(v1, v2)
        pesos: MutableSequence[float] = []
        for possibilidade in possibilidades:
            soma_pesos: float = 0.0
            for arco in possibilidade:
                soma_pesos += arco.peso
            pesos.append(soma_pesos)
        return pesos

    def calcular_soma_comprimentos(self, v1: Vertice, v2: Vertice, /) -> Sequence[int]:
        """Calcula todos os comprimentos possiveis entre dois vertices do grafo

        Args:
            v1 (Vertice): Ponto de partida
            v2 (Vertice): Ponto de chegada

        Returns:
            Sequence[int]: retorna uma tupla com todos os comprimentos possiveis.
        """
        possibilidades = self.calcular_possibilidades_caminhos(v1, v2)
        comprimentos = [len(p) for p in possibilidades]
        return comprimentos


# endregion


# region main
def main() -> None:
    """Ponto de partida do script"""
    # Instanciar o grafo
    grafo = Grafo()

    # Criar vertices.
    v1 = Vertice("A")
    v2 = Vertice("B")
    v3 = Vertice("C")

    # Adicionar vertices no grafo
    grafo.vertices.criar(v1)
    grafo.vertices.criar(v2)
    grafo.vertices.criar(v3)

    # Associar vertices relacionados com pesos diferentes
    grafo.g(
        (v1, v2, 2.5),
        (v1, v3, 1.0),
        (v2, v3, 3.0),
    )

    calculadora = CalculadoraDeGrafo(grafo)

    # Exibir matriz de adjacência
    grafo.mostrar_matriz_adjacencia(clear_screen=True)

    # Exibir informações do grafo com pretty printing
    print("\n")
    grafo.pretty_print("Grafo de Exemplo")

    # Calcular possibilidades de caminhos
    caminhos = calculadora.calcular_possibilidades_caminhos(v1, v3)
    print(f"\nCaminhos possíveis de A para E: {len(caminhos)}")

    # Tentar visualizar o grafo
    try:
        #grafo.visualizar_grafo_navegador(titulo="Exemplo de Grafo")
        pass
    except ImportError as e:
        print(f"\nNão foi possível visualizar o grafo: {e}")


# endregion

# region script
if __name__ == "__main__":
    import timeit

    beginning = timeit.default_timer()
    main()
    logger.debug(f"Execução finalizada em {(timeit.default_timer() - beginning):.3f}s")
# endregion
