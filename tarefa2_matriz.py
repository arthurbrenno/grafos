type DestinoEPeso = tuple[str, float]


class Grafo:
    grafo: dict[str, dict[str, float | None]]

    def __init__(self, grafo: dict[str, dict[str, float | None]] | None = None) -> None:
        """
        Inicializa um novo grafo, opcionalmente a partir de um dicionário existente.

        Args:
            grafo (dict[str, dict[str, float]] | None, opcional): Dicionário inicial para o grafo.
                                                                  Se None, cria um grafo vazio.
        """
        self.grafo = grafo or {}

    def add_vertice(self, vertice: str) -> None:
        """
        Adiciona um novo vértice ao grafo se ele ainda não existir.

        Args:
            vertice (str): Nome do vértice a ser adicionado.
        """
        if vertice in self.grafo.keys():
            return

        # Pra cada elemento do dicionario, adicionar esse extra
        for _, val in self.grafo.items():
            val[vertice] = {}

        self.grafo[vertice] = {}

    def add_aresta(self, origem: str, destino: str, peso: float) -> None:
        """
        Adiciona uma aresta direcionada com peso entre dois vértices.

        Args:
            origem (str): Vértice de origem da aresta.
            destino (str): Vértice de destino da aresta.
            peso (float): Peso associado à aresta.

        Raises:
            RuntimeError: Se qualquer um dos vértices não existir no grafo.
        """
        ...

    def obter_peso_vertices_adjacentes(self, origem: str, destino: str) -> float:
        """
        Obtém o peso da aresta entre dois vértices adjacentes.

        Args:
            origem (str): Vértice de origem.
            destino (str): Vértice de destino.

        Returns:
            float: Peso da aresta entre os vértices.

        Raises:
            RuntimeError: Se a origem não existir ou os vértices não forem adjacentes.
        """
        ...

    def visualizar(self) -> None:
        """
        Exibe uma representação visual do grafo no terminal.
        Limpa a tela antes de exibir o grafo.
        """
        import os

        os.system("cls" if os.name == "nt" else "clear")
        for origem, destinos in self.grafo.items():
            print(f"{origem}: ", end=" ")
            for _destino, _peso in destinos:
                print(f"{_destino}({_peso}),", end="   ")
            print()

    def calcular_caminhos_possiveis(
        self,
        origem: str,
        destino: str,
        caminho_atual: list[DestinoEPeso] | None = None,
        visitados: set[str] | None = None,
    ) -> list[list[DestinoEPeso]]:
        """
        Calcula todos os caminhos possíveis entre dois vértices usando busca em profundidade.

        Args:
            origem (str): Vértice de origem.
            destino (str): Vértice de destino.
            caminho_atual (list[DestinoEPeso] | None, opcional): Lista de vértices e pesos
                                                                      no caminho atual. Padrão é None.
            visitados (set[str] | None, opcional): Conjunto de vértices já visitados. Padrão é None.

        Returns:
            list[list[DestinoEPeso]]: Lista de todos os caminhos possíveis entre origem e destino.
                                     Cada caminho é uma lista de tuplas (vértice, peso).
        """
        ...

    def mostrar_caminhos_possiveis(self, caminhos: list[list[DestinoEPeso]]) -> None:
        """
        Exibe todos os caminhos possíveis entre dois vértices, com seus respectivos pesos.

        Args:
            caminhos (list[list[DestinoEPeso]]): Lista de caminhos a serem exibidos.
                                                Cada caminho é uma lista de tuplas (vértice, peso).
        """
        import os

        os.system("cls" if os.name == "nt" else "clear")

        for i, caminho in enumerate(caminhos, 1):
            print(f"Caminho {i}:", end=" ")
            peso_total = 0
            for destino, peso in caminho:
                print(f"{destino} ({peso}) →", end=" ")
                peso_total += peso
            print(f"Peso total: {peso_total}")


def main() -> None: ...


if __name__ == "__main__":
    main()
