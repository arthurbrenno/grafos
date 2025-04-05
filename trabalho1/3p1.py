import random


def dfs(
    grafo: dict[str, set[str]], origem: str, visitados: list[str], contador: int
) -> int:
    contador = contador + 1
    visitados.append(origem)
    for w in grafo[origem]:
        if w not in visitados:
            contador = dfs(grafo, w, visitados, contador)
    return contador


class Grafo:
    def __init__(self) -> None:
        self.adjacencias: dict[str, set[str]] = {}

    def eh_conexo(self) -> bool:
        if dfs(
            self.adjacencias,
            random.choice(list(self.adjacencias.keys())),
            [],
            0,
        ):
            return True

        return False

    def identificar_pontos_criticos(self) -> set[str]:
        def dfs(
            grafo: dict[str, set[str]],
            origem: str,
            visitados: set[str],
            vertices_criticos: set[str],
        ):
            visitados.add(origem)
            adjacencias = grafo[origem]
            if len(adjacencias) > 1:
                vertices_criticos.add(origem)

            for w in adjacencias:
                if w not in visitados:
                    dfs(
                        grafo,
                        w,
                        visitados=visitados,
                        vertices_criticos=vertices_criticos,
                    )

        vertices_criticos: set[str] = {*()}
        dfs(
            self.adjacencias,
            random.choice(list(self.adjacencias.keys())),
            {*()},
            vertices_criticos=vertices_criticos,
        )

        return vertices_criticos

    def add_aresta(self, v1: str, v2: str) -> None:
        vertices_do_grafo = self.adjacencias.keys()

        if v1 not in vertices_do_grafo:
            self.adjacencias[v1] = {*()}

        if v2 not in vertices_do_grafo:
            self.adjacencias[v2] = {*()}

        self.adjacencias[v1].add(v2)
        self.adjacencias[v2].add(v1)

    def calcular_ordem(self) -> int:
        vertices_do_grafo = self.adjacencias.keys()
        quantidade_vertices = len(vertices_do_grafo)
        return quantidade_vertices

    def calcular_tamanho(self) -> int:
        return sum(len(v) for v in self.adjacencias.values()) // 2


g = Grafo()

g.add_aresta("r", "a")
g.add_aresta("r", "b")
g.add_aresta("r", "c")
g.add_aresta("a", "d")
g.add_aresta("a", "e")
g.add_aresta("c", "f")
g.add_aresta("f", "g")

print("Tamanho: ")
print(g.calcular_tamanho())

print("Conexo: ")
print(g.eh_conexo())

print("Criticos: ")
print(g.identificar_pontos_criticos())

print("DFS que retorna num vertices visitados: ")
print(dfs(g.adjacencias, "r", [], 0))
