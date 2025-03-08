type DestinoEPeso = tuple[str, float]


class Grafo:
    grafo: dict[str, set[DestinoEPeso]]

    def __init__(self, grafo: dict[str, set[DestinoEPeso]] | None = None) -> None:
        self.grafo = grafo or {}

    def add_vertice(self, vertice: str) -> None:
        vertice_ja_criado = vertice in self.grafo.keys()
        if vertice_ja_criado:
            return

        self.grafo[vertice.upper()] = set([])

    def add_aresta(self, origem: str, destino: str, peso: float) -> None:
        origem_nao_criada = origem.upper() not in self.grafo.keys()
        if origem_nao_criada:
            raise RuntimeError("O primeiro vertice não foi encontrado no grafo.")

        destino_nao_criado = destino.upper() not in self.grafo.keys()
        if destino_nao_criado:
            raise RuntimeError("O segundo vertice não foi encontrado no grafo.")

        self.grafo[origem.upper()].add((destino.upper(), peso))

    def obter_peso_vertices_adjacentes(self, origem: str, destino: str) -> float:
        if origem not in self.grafo.keys():
            raise RuntimeError("A origem não foi cadastrada.")

        destinos = self.grafo[origem]
        peso: float | None = None
        for _dest in destinos:
            if destino == _dest[0]:
                peso = _dest[1]

        if peso is None:
            raise RuntimeError("Os vertices não são adjacentes.")

        return peso

    def visualizar(self) -> None:
        import os

        os.system("cls" if os.name == "nt" else "clear")
        for origem, destinos in self.grafo.items():
            print(f"{origem}: ", end=" ")
            for destino in destinos:
                _destino = destino[0]
                _peso = destino[1]
                print(f"{_destino}({_peso}),", end="   ")
            print()

    def calcular_caminhos_possiveis(
        self,
        origem: str,
        destino: str,
        caminho_atual: list[tuple[str, float]] | None = None,
        visitados: set[str] | None = None,
    ) -> list[list[DestinoEPeso]]:
        # Inicializar valores padrão
        if caminho_atual is None:
            caminho_atual = []
        if visitados is None:
            visitados = set()

        # Converter para maiúsculo para manter o padrão
        origem = origem.upper()
        destino = destino.upper()

        # Registrar o vértice atual como visitado
        visitados.add(origem)

        # Se chegamos ao destino, retornamos o caminho atual como um único caminho em uma lista
        if origem == destino:
            return [caminho_atual]

        # Lista para armazenar todos os caminhos encontrados
        caminhos: list[list[DestinoEPeso]] = []

        # Explorar todos os vértices adjacentes
        for proximo_destino, peso in self.grafo[origem]:
            # Verificar se o vértice já foi visitado para evitar ciclos
            if proximo_destino not in visitados:
                # Adicionar o próximo destino ao caminho atual
                novo_caminho = caminho_atual + [(proximo_destino, peso)]

                # Criar uma cópia do conjunto de visitados para a recursão
                novo_visitados = visitados.copy()

                # Chamada recursiva para continuar a partir do próximo destino
                caminhos_encontrados = self.calcular_caminhos_possiveis(
                    proximo_destino, destino, novo_caminho, novo_visitados
                )

                # Adicionar os caminhos encontrados à lista de caminhos
                caminhos.extend(caminhos_encontrados)

        return caminhos

    def mostrar_caminhos_possiveis(self, caminhos: list[list[DestinoEPeso]]) -> None:
        print("\nCaminhos possíveis de A para D:")

        for i, caminho in enumerate(caminhos, 1):
            print(f"Caminho {i}:", end=" ")
            # O primeiro vértice não está no caminho, então precisamos adicioná-lo
            print("A →", end=" ")
            peso_total = 0
            for destino, peso in caminho:
                print(f"{destino} ({peso}) →", end=" ")
                peso_total += peso
            print(f"Peso total: {peso_total}")


def main() -> None:
    g = Grafo()
    g.add_vertice("a")
    g.add_vertice("b")
    g.add_vertice("c")
    g.add_vertice("d")

    g.add_aresta(origem="a", destino="b", peso=1)
    g.add_aresta(origem="b", destino="c", peso=1)
    g.add_aresta(origem="a", destino="c", peso=1)

    g.visualizar()

    # Teste da função de calcular caminhos
    caminhos = g.calcular_caminhos_possiveis(origem="a", destino="c")
    g.mostrar_caminhos_possiveis(caminhos)


if __name__ == "__main__":
    main()
