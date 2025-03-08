"""
Módulo para manipulação de grafos ponderados direcionados usando matriz de adjacência.

Este módulo implementa uma estrutura de dados para representar grafos direcionados
com pesos nas arestas, utilizando um dicionário de dicionários como matriz de adjacência.
Também inclui funções para calcular e visualizar todos os caminhos possíveis entre dois vértices.

Tipos:
    DestinoEPeso: Tupla representando um vértice destino e o peso da aresta para chegar até ele.
    CaminhoPossivel: Lista de tuplas DestinoEPeso representando um caminho completo no grafo.
"""

type DestinoEPeso = tuple[str, float]
type CaminhoPossivel = list[DestinoEPeso]
type RepresentacaoGrafo = dict[str, dict[str, float | None]]


class Grafo:
    """
    Classe que representa um grafo direcionado e ponderado usando matriz de adjacência.

    A matriz de adjacência é implementada como um dicionário de dicionários, onde:
    - A chave externa representa o vértice de origem
    - A chave interna representa o vértice de destino
    - O valor representa o peso da aresta (ou None se não existir conexão)

    Atributos:
        grafo (RepresentacaoGrafo): Matriz de adjacência do grafo.
    """

    grafo: RepresentacaoGrafo

    def __init__(self, grafo: RepresentacaoGrafo | None = None) -> None:
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

        Este método atualiza a matriz de adjacência adicionando uma nova linha e coluna
        para o novo vértice, inicializando todas as conexões como None.

        Args:
            vertice (str): Nome do vértice a ser adicionado.
        """
        if vertice in self.grafo.keys():
            return

        # Atualizar os outros. Adicionar o novo vertice sendo criado e colocar None
        for _, v in self.grafo.items():
            v.update({vertice: None})

        # Atualizar a atual
        self.grafo[vertice] = {vertice: None}
        self.grafo[vertice].update({k: None for k in self.grafo.keys()})

    def add_aresta(self, origem: str, destino: str, peso: float) -> None:
        """
        Adiciona uma aresta direcionada com peso entre dois vértices.

        O método cria uma conexão de origem para destino com o peso especificado.
        Não cria automaticamente a conexão inversa (de destino para origem).

        Args:
            origem (str): Vértice de origem da aresta.
            destino (str): Vértice de destino da aresta.
            peso (float): Peso associado à aresta.

        Raises:
            RuntimeError: Se qualquer um dos vértices não existir no grafo.
        """
        if origem not in self.grafo.keys():
            raise RuntimeError("O vértice de origem não foi encontrado no grafo.")

        if destino not in self.grafo.keys():
            raise RuntimeError("O vértice de destino não foi encontrado no grafo.")

        self.grafo[origem][destino] = peso

    def obter_peso_vertices_adjacentes(self, origem: str, destino: str) -> float | None:
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
        if origem not in self.grafo.keys():
            raise RuntimeError("A origem não foi cadastrada.")

        if destino not in self.grafo[origem] or self.grafo[origem][destino] is None:
            raise RuntimeError("Os vértices não são adjacentes.")

        return self.grafo[origem][destino]

    def visualizar(self) -> None:
        """
        Exibe uma representação visual do grafo como matriz de adjacência no terminal.

        O método limpa a tela e exibe uma tabela onde:
        - As linhas representam os vértices de origem
        - As colunas representam os vértices de destino
        - As células contêm o peso da aresta ou "-" se não houver conexão

        Limpa a tela antes de exibir o grafo.
        """
        import os

        os.system("cls" if os.name == "nt" else "clear")

        vertices = list(self.grafo.keys())

        # Imprime o cabeçalho com os nomes dos vértices
        print("    ", end="")
        for v in vertices:
            print(f"{v:^5}", end="")
        print()

        # Imprime a linha separadora
        print("    " + "-----" * len(vertices))

        # Imprime cada linha da matriz
        for origem in vertices:
            print(f"{origem} | ", end="")
            for destino in vertices:
                # Verifica se existe uma aresta entre origem e destino
                if (
                    destino in self.grafo[origem]
                    and self.grafo[origem][destino] is not None
                ):
                    # Imprime o peso da aresta
                    print(f"{self.grafo[origem][destino]:^5}", end="")
                else:
                    # Imprime um indicador de que não há aresta
                    print("  -  ", end="")
            print()

    def calcular_caminhos_possiveis(
        self,
        origem: str,
        destino: str,
        caminho_atual: list[DestinoEPeso] | None = None,
        visitados: set[str] | None = None,
    ) -> list[CaminhoPossivel]:
        """
        Calcula todos os caminhos possíveis entre dois vértices usando busca em profundidade.

        O algoritmo utiliza uma abordagem recursiva de busca em profundidade (DFS) para
        encontrar todos os caminhos possíveis sem ciclos entre os vértices de origem e destino.

        Args:
            origem (str): Vértice de origem.
            destino (str): Vértice de destino.
            caminho_atual (list[DestinoEPeso] | None): Lista de vértices e pesos
                                                     no caminho atual. Padrão é None.
            visitados (set[str] | None): Conjunto de vértices já visitados. Padrão é None.

        Returns:
            list[CaminhoPossivel]: Lista de todos os caminhos possíveis entre origem e destino.
                                     Cada caminho é uma lista de tuplas (vértice, peso).
        """
        # Inicializar valores padrão
        if caminho_atual is None:
            caminho_atual = []

        if visitados is None:
            visitados = set()

        # Registrar o vértice atual como visitado
        visitados.add(origem)

        # Se chegamos ao destino, retornamos o caminho atual como um único caminho em uma lista
        if origem == destino:
            return [caminho_atual]

        # Lista para armazenar todos os caminhos encontrados
        caminhos: list[CaminhoPossivel] = []

        # Explorar todos os vértices adjacentes
        for proximo_destino in self.grafo[origem]:
            peso = self.grafo[origem][proximo_destino]
            # Ignorar vértices sem conexão (peso None)
            if peso is None:
                continue

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

    def mostrar_caminhos_possiveis(self, caminhos: list[CaminhoPossivel]) -> None:
        """
        Exibe todos os caminhos possíveis entre dois vértices, com seus respectivos pesos.

        Para cada caminho, exibe a sequência de vértices, o peso de cada aresta,
        e o peso total do caminho.

        Args:
            caminhos (CaminhoPossivel): Lista de caminhos a serem exibidos.
                                       Cada caminho é uma lista de tuplas (vértice, peso).
        """
        import os

        os.system("cls" if os.name == "nt" else "clear")

        if not caminhos:
            print("Não foram encontrados caminhos entre os vértices especificados.")
            return

        print(f"\nCaminhos possíveis encontrados: {len(caminhos)}")

        for i, caminho in enumerate(caminhos, 1):
            print(f"Caminho {i}:", end=" ")

            # Verificar se o caminho está vazio (origem = destino)
            if not caminho:
                print("Origem e destino são o mesmo vértice.")
                continue

            # Obter o primeiro vértice do caminho
            peso_total = 0

            # Imprimir o vértice de origem (que não está no caminho)
            if len(caminho) > 0:
                # Encontramos o vértice de origem por exclusão
                for v in self.grafo.keys():
                    if v not in [dest for dest, _ in caminho]:
                        print(f"{v} →", end=" ")
                        break

            # Imprimir o resto do caminho
            for destino, peso in caminho:
                print(f"{destino} ({peso}) →", end=" ")
                peso_total += peso

            print(f"Peso total: {peso_total}")


def ler_grafo_de_arquivo(nome_arquivo: str) -> Grafo:
    """
    Lê um grafo de um arquivo de texto em formato estruturado.

    O arquivo deve seguir um formato específico com seções para vértices e arestas.
    Comentários podem ser incluídos iniciando a linha com #.

    Formato do arquivo:
    # Linhas que começam com # são comentários
    VERTICES:
    v1
    v2
    ...
    ARESTAS:
    v1 v2 peso
    v2 v3 peso
    ...

    Args:
        nome_arquivo (str): Caminho para o arquivo de texto.

    Returns:
        Grafo: Um novo grafo configurado com os vértices e arestas do arquivo.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        ValueError: Se o formato do arquivo for inválido.
    """
    g = Grafo()

    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    # Estado para controlar o que estamos lendo
    estado = None

    for numero_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()

        # Ignorar linhas em branco ou comentários
        if not linha or linha.startswith("#"):
            continue

        # Verificar seções
        if linha == "VERTICES:":
            estado = "vertices"
            continue
        elif linha == "ARESTAS:":
            estado = "arestas"
            continue

        # Processar conteúdo baseado no estado atual
        if estado == "vertices":
            g.add_vertice(linha)
        elif estado == "arestas":
            partes = linha.split()
            if len(partes) != 3:
                raise ValueError(
                    f"Formato inválido na linha {numero_linha}: '{linha}'. Use 'origem destino peso'"
                )

            origem, destino, peso_str = partes
            try:
                peso = float(peso_str)
                g.add_aresta(origem=origem, destino=destino, peso=peso)
            except ValueError:
                raise ValueError(f"Peso inválido na linha {numero_linha}: '{peso_str}'")
            except RuntimeError as e:
                raise ValueError(
                    f"Erro ao adicionar aresta na linha {numero_linha}: {e}"
                )

    # Verificar se o grafo tem pelo menos um vértice
    if not g.grafo:
        raise ValueError("Arquivo não contém vértices válidos")

    return g


def main() -> None:
    """
    Função principal que lê um grafo de um arquivo, calcula e mostra caminhos entre vértices.

    Fluxo de execução:
    1. Tenta carregar um grafo do arquivo 'input.txt'
    2. Exibe a representação visual do grafo
    3. Solicita ao usuário os vértices de origem e destino
    4. Calcula e exibe todos os caminhos possíveis entre os vértices especificados
    5. Trata possíveis erros durante a execução
    """
    try:
        g = ler_grafo_de_arquivo("input.txt")

        print("Grafo carregado com sucesso!")
        g.visualizar()

        origem = input("\nDigite o vértice de origem: ").upper()
        destino = input("Digite o vértice de destino: ").upper()

        caminhos = g.calcular_caminhos_possiveis(origem=origem, destino=destino)

        if not caminhos:
            print(f"Não foram encontrados caminhos de {origem} para {destino}.")
        else:
            g.mostrar_caminhos_possiveis(caminhos)
    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
