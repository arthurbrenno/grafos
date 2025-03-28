"""
Implementação de um grafo não-direcionado com leitura de arquivo e menu interativo.
- Autores: Arthur Brenno e Yannes Fidalgo
"""

import os
from typing import Literal


class Grafo:
    """
    Classe que implementa um grafo não-direcionado utilizando lista de adjacência.

    Permite operações básicas como adicionar arestas e verificar propriedades do grafo
    como conexidade, ciclicidade e planaridade.
    """

    def __init__(self) -> None:
        """
        Inicializa um grafo vazio.
        """
        self.grafo: dict[str, list[str]] = {}

    def add_aresta(self, v1: str, v2: str) -> None:
        """
        Adiciona uma aresta não-direcionada entre dois vértices no grafo.

        Args:
            v1: Primeiro vértice da aresta
            v2: Segundo vértice da aresta
        """
        if v1 not in self.grafo:
            self.grafo[v1] = []

        if v2 not in self.grafo:
            self.grafo[v2] = []

        self.grafo[v1].append(v2)
        self.grafo[v2].append(v1)

    def carregar_de_arquivo(self, nome_arquivo: str = "input.txt") -> bool:
        """
        Carrega um grafo a partir do arquivo input.txt.

        O formato esperado do arquivo é:
        - Uma aresta por linha
        - Cada linha contém dois vértices separados por espaço ou vírgula

        Args:
            nome_arquivo: Nome do arquivo contendo a definição do grafo

        Returns:
            bool: True se o arquivo foi carregado com sucesso, False caso contrário
        """
        try:
            with open(nome_arquivo, "r") as arquivo:
                # Limpa o grafo atual
                self.grafo = {}

                for linha in arquivo:
                    # Remove espaços em branco extras e quebra de linha
                    linha = linha.strip()

                    if not linha or linha.startswith("#"):
                        continue  # Ignora linhas vazias e comentários

                    # Tenta separar por espaço ou vírgula
                    if "," in linha:
                        v1, v2 = linha.split(",", 1)
                    else:
                        v1, v2 = linha.split(None, 1)

                    v1 = v1.strip()
                    v2 = v2.strip()

                    self.add_aresta(v1, v2)

                return True
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return False

    def eh_conexo(self) -> bool:
        """
        Verifica se o grafo é conexo, ou seja, se existe um caminho entre
        quaisquer dois vértices do grafo.

        Returns:
            bool: True se o grafo for conexo, False caso contrário
        """
        if not self.grafo:
            return True  # Grafo vazio é considerado conexo

        # Implementação usando busca em profundidade recursiva
        visitados: set[str] = set()

        def dfs(vertice: str) -> None:
            visitados.add(vertice)
            for vizinho in self.grafo[vertice]:
                if vizinho not in visitados:
                    dfs(vizinho)

        # Comece a DFS a partir do primeiro vértice
        primeiro_vertice = next(iter(self.grafo))
        dfs(primeiro_vertice)

        # Se todos os vértices foram visitados, o grafo é conexo
        return len(visitados) == len(self.grafo)

    def eh_ciclico(self) -> bool:
        """
        Verifica se o grafo contém pelo menos um ciclo.

        Returns:
            bool: True se o grafo for cíclico, False caso contrário
        """
        visitados: set[str] = set()

        def tem_ciclo(vertice: str, pai: str | None) -> bool:
            visitados.add(vertice)

            for vizinho in self.grafo[vertice]:
                # Se o vizinho já foi visitado e não é o pai, encontramos um ciclo
                if vizinho in visitados and vizinho != pai:
                    return True

                # Se o vizinho não foi visitado, continue a busca
                if vizinho not in visitados:
                    if tem_ciclo(vizinho, vertice):
                        return True

            return False

        # Verifique cada componente não visitado
        for vertice in self.grafo:
            if vertice not in visitados:
                if tem_ciclo(vertice, None):
                    return True

        return False

    def eh_plano(self) -> bool:
        """
        Verifica se o grafo é planar, ou seja, se pode ser desenhado em um plano
        sem que suas arestas se cruzem.

        Esta implementação usa a fórmula de Euler para grafos planares: V - E + F = 2,
        onde V é o número de vértices, E é o número de arestas e F é o número de faces.

        Returns:
            bool: True se o grafo for planar, False caso contrário
        """
        # Verifica se o grafo está vazio
        if not self.grafo:
            return True

        # Número de vértices
        v: int = len(self.grafo)

        # Número de arestas (contando cada aresta uma única vez)
        e: int = sum(len(vizinhos) for vizinhos in self.grafo.values()) // 2

        # Para um grafo planar, o número máximo de arestas é 3v - 6 para v ≥ 3
        if v >= 3:
            return e <= 3 * v - 6

        # Para v < 3, qualquer grafo é planar
        return True

    def mostrar_grafo(self) -> None:
        """
        Exibe uma representação do grafo na tela.
        """
        if not self.grafo:
            print("Grafo vazio.")
            return

        print("\nRepresentação do Grafo (Lista de Adjacência):")
        print("-" * 50)

        for vertice, vizinhos in sorted(self.grafo.items()):
            print(f"{vertice} -> {', '.join(sorted(vizinhos))}")

        print("-" * 50)
        print(f"Total de vértices: {len(self.grafo)}")

        # Calcula o número de arestas (cada aresta é contada duas vezes na lista de adjacência)
        total_arestas = sum(len(vizinhos) for vizinhos in self.grafo.values()) // 2
        print(f"Total de arestas: {total_arestas}")
        print("-" * 50)


def limpar_tela() -> None:
    """
    Limpa a tela do console.
    """
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para MacOS e Linux
    else:
        os.system("clear")


def mostrar_menu() -> None:
    """
    Exibe o menu principal do programa.
    """
    print("\n==== MENU DO GRAFO ====")
    print("1. Mostrar grafo")
    print("2. Verificar se o grafo é conexo")
    print("3. Verificar se o grafo é cíclico")
    print("4. Verificar se o grafo é planar")
    print("5. Adicionar aresta")
    print("0. Sair")
    print("=======================")


def menu_principal() -> None:
    """
    Função principal que implementa o menu interativo para o grafo.
    """
    grafo = Grafo()

    limpar_tela()

    # Carrega o grafo do arquivo input.txt automaticamente na inicialização
    print("Carregando grafo do arquivo input.txt...")
    if grafo.carregar_de_arquivo():
        print("Grafo carregado com sucesso!")
    else:
        print(
            "Não foi possível carregar o grafo. Verifique se o arquivo input.txt existe."
        )

    while True:
        limpar_tela()
        mostrar_menu()

        try:
            opcao = input("Escolha uma opção: ")

            limpar_tela()

            match opcao:
                case "1":
                    grafo.mostrar_grafo()

                case "2":
                    if grafo.eh_conexo():
                        print("\nO grafo É conexo.")
                    else:
                        print("\nO grafo NÃO é conexo.")

                case "3":
                    if grafo.eh_ciclico():
                        print("\nO grafo É cíclico.")
                    else:
                        print("\nO grafo NÃO é cíclico.")

                case "4":
                    if grafo.eh_plano():
                        print("\nO grafo É planar.")
                    else:
                        print("\nO grafo NÃO é planar.")

                case "5":
                    v1 = input("Digite o primeiro vértice: ")
                    v2 = input("Digite o segundo vértice: ")
                    grafo.add_aresta(v1, v2)
                    print(f"\nAresta adicionada: {v1} -- {v2}")

                case "0":
                    print("\nEncerrando o programa...")
                    break

                case _:
                    print("\nOpção inválida. Tente novamente.")

            input("\nPressione Enter para continuar...")

        except Exception as e:
            print(f"\nErro: {e}")
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    print("===== SISTEMA DE GRAFO =====")
    print("Autores: Arthur Brenno e Yannes Fidalgo")
    menu_principal()
