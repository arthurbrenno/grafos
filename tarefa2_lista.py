"""
Implementação de uma estrutura de dados Grafo com funcionalidades de gerenciamento de vértices,
arestas e cálculo de caminhos entre vértices.

A implementação utiliza um dicionário para representar o grafo, onde as chaves são os vértices
e os valores são conjuntos de tuplas (destino, peso) representando as arestas direcionadas.
"""

# Define um tipo personalizado para representar o destino e o peso de uma aresta
type DestinoEPeso = tuple[str, float]


class Grafo:
    """
    Classe que implementa um grafo direcionado com pesos nas arestas.

    Atributos:
        grafo (dict[str, set[DestinoEPeso]]): Dicionário que mapeia vértices para seus destinos e pesos.
    """

    grafo: dict[str, set[DestinoEPeso]]

    def __init__(self, grafo: dict[str, set[DestinoEPeso]] | None = None) -> None:
        """
        Inicializa um novo grafo, opcionalmente a partir de um dicionário existente.

        Args:
            grafo (dict[str, set[DestinoEPeso]] | None, opcional): Dicionário inicial para o grafo.
                                                                  Se None, cria um grafo vazio.
        """
        self.grafo = grafo or {}

    def add_vertice(self, vertice: str) -> None:
        """
        Adiciona um novo vértice ao grafo se ele ainda não existir.

        Args:
            vertice (str): Nome do vértice a ser adicionado.
        """
        vertice_ja_criado = vertice in self.grafo.keys()
        if vertice_ja_criado:
            return

        self.grafo[vertice.upper()] = set([])

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
        origem_nao_criada = origem.upper() not in self.grafo.keys()
        if origem_nao_criada:
            raise RuntimeError("O primeiro vertice não foi encontrado no grafo.")

        destino_nao_criado = destino.upper() not in self.grafo.keys()
        if destino_nao_criado:
            raise RuntimeError("O segundo vertice não foi encontrado no grafo.")

        self.grafo[origem.upper()].add((destino.upper(), peso))

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
        if origem not in self.grafo.keys():
            raise RuntimeError("A origem não foi cadastrada.")

        destinos = self.grafo[origem]
        peso: float | None = None
        for _dest, _peso in destinos:
            if destino == _dest:
                peso = _peso

        if peso is None:
            raise RuntimeError("Os vertices não são adjacentes.")

        return peso

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
        É uma função recursiva.

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
        # Inicializar valores padrão
        caminho_atual = caminho_atual or []
        visitados = visitados or set()

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
            if proximo_destino in visitados:
                continue

            # Chamada recursiva para continuar a partir do próximo destino
            caminhos_encontrados = self.calcular_caminhos_possiveis(
                origem=proximo_destino.upper(),
                destino=destino.upper(),
                caminho_atual=caminho_atual + [(proximo_destino, peso)],
                visitados=visitados.copy(),
            )

            # Adicionar os caminhos encontrados à lista de caminhos
            caminhos.extend(caminhos_encontrados)

        return caminhos

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


def ler_grafo_de_arquivo(nome_arquivo: str) -> Grafo:
    """
    Lê um grafo de um arquivo de texto em formato estruturado.

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

    Se o arquivo 'input.txt' não existir, cria automaticamente um arquivo de exemplo.
    """
    try:
        nome_arquivo = "input.txt"

        try:
            g = ler_grafo_de_arquivo(nome_arquivo)
        except FileNotFoundError:
            print(
                f"Arquivo '{nome_arquivo}' não encontrado. Criando arquivo de exemplo..."
            )
            with open(nome_arquivo, "w") as f:
                f.write("""# Grafo de exemplo
VERTICES:
A
B
C
D
E

ARESTAS:
A B 5.2
A C 3.1
B D 2.0
C D 1.7
B E 4.3
D E 2.5""")

            # Tenta ler o arquivo recém-criado
            g = ler_grafo_de_arquivo(nome_arquivo)
            print(f"Arquivo de exemplo '{nome_arquivo}' criado com sucesso!")

        print("Grafo carregado com sucesso!")
        g.visualizar()

        origem = input("\nDigite o vértice de origem: ").upper()
        destino = input("Digite o vértice de destino: ").upper()

        caminhos = g.calcular_caminhos_possiveis(
            origem=origem.upper(), destino=destino.upper()
        )

        soma = 0
        for caminho in caminhos:
            for _, peso in caminho:
                soma += peso

        print(soma)

        if not caminhos:
            print(f"Não foram encontrados caminhos de {origem} para {destino}.")
        else:
            g.mostrar_caminhos_possiveis(caminhos)

    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
