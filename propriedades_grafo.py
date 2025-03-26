"""Dessa vez fiz um codigo mais simples sem tipagem"""
# Arthur Brenno e Yannes Fidalgo


class Grafo:
    def __init__(self):
        self.grafo = {}

    def add_aresta(self, v1, v2):
        if v1 not in self.grafo:
            self.grafo[v1] = []

        if v2 not in self.grafo:
            self.grafo[v2] = []

        self.grafo[v1].append(v2)
        self.grafo[v2].append(v1)

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

        # vou otimizar isso ainda
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


g = Grafo()

g.add_aresta("A", "B")
print(g.grafo)
