import sys
import heapq
import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class Grafo:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.matAdj = [[sys.maxsize for _ in range(self.numVertices)] for _ in range(self.numVertices)]

    @property
    def numVertices(self):
        return self._numVertices

    @numVertices.setter
    def numVertices(self, numVertices):
        self._numVertices = numVertices

    @property
    def matAdj(self):
        return self._matAdj

    @matAdj.setter
    def matAdj(self, matAdj):
        self._matAdj = matAdj

    def adicionarAresta(self, verticeA, verticeB, peso):
        self._matAdj[verticeA][verticeB] = peso
        self._matAdj[verticeB][verticeA] = peso
    
    def removerAresta(self, verticeA, verticeB):
        self._matAdj[verticeA][verticeB] = sys.maxsize

    def dijkstra(self, origem):
        distancias = [sys.maxsize for _ in range(self.numVertices)]
        antecessores = [sys.maxsize for _ in range(self.numVertices)]
        visitados = [False for _ in range(self.numVertices)]

        distancias[origem] = 0
        antecessores[origem] = origem

        heap = [(0, origem)]

        while heap:
            _, verticeAtual = heapq.heappop(heap)
            if visitados[verticeAtual]:
                continue
            visitados[verticeAtual] = True
            for j in range(self.numVertices):
                if self._matAdj[verticeAtual][j] != sys.maxsize:
                    novaDistancia = distancias[verticeAtual] + self._matAdj[verticeAtual][j]
                    if novaDistancia < distancias[j]:
                        antecessores[j] = verticeAtual
                        distancias[j] = novaDistancia
                        heapq.heappush(heap, (novaDistancia, j))
        return distancias, antecessores

    def encontraCaminhoMinimo(self, origem, destino):
        distancias, antecessores = self.dijkstra(origem)
        caminho = []
        if distancias[destino] == sys.maxsize:
            return caminho
        atual = destino
        while atual != origem:
            caminho.append(atual)
            atual = antecessores[atual]
        caminho.reverse()
        return caminho
    
    def betweeness(self):
        betweeness = [0.0 for _ in range(self.numVertices)]
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                cam = self.encontraCaminhoMinimo(i, j)
                if len(cam) != 0:
                    
                    for v in range(len(cam) - 1):
                        betweeness[cam[v]] += 1
        cont = (self.numVertices * self.numVertices - 1) / 2
        for i in range(self.numVertices):
            betweeness[i] /= cont
            print(f"{i}: ", betweeness[i])
        return betweeness

    def mostraGrafo(self):
        print("    ", end="")
        ##for i in range(self.numVertices):
        ##    print(f" {i}: ", end="")
        ##print("")
        for i in range(self.numVertices):
            print( end="")
            for j in range(self.numVertices):
                if (self.matAdj[i][j] == sys.maxsize):
                    print(f"{0:>3}", end=",")
                else:
                    print(f"{self.matAdj[i][j]:>3}", end=",")
            print("")

    def plotarGrafo(self, valores):
        G = nx.Graph()
        numVertices = self.numVertices
        G.add_nodes_from(range(numVertices))

        for i in range(numVertices):
            for j in range(i + 1, numVertices):
                weight = self.matAdj[i][j]
                if weight != sys.maxsize:
                    G.add_edge(i, j)

        # Calcula o grau de cada vértice
        graus = G.degree()

        # Obtém os valores de grau para normalização
        valores_grau = [graus[i] for i in range(numVertices)]
        max_betweeness = max(valores)
        min_betweeness = min(valores)

        # Definindo uma lista de cores personalizada para a paleta linear
        my_colors = [
        '#C8102E',  # Vermelho
        '#FF4500',  # laranja
        '#FFFF00',  # Amarelo claro
        '#90EE90',  # Verde claro
        '#00FFFF',  # Verde água
        '#ADD8E6',  # Azul claro
        '#0000FF',  # Azul
        ]

        # Criando uma paleta de cores linear personalizada
        cmap = colors.ListedColormap(my_colors)

        # Normaliza os valores de grau entre 0 e 1
        norm = colors.Normalize(vmin=min_betweeness, vmax=max_betweeness)

        # Mapeia os valores de grau normalizados para cores
        cores = [cmap(norm(valores[i])) for i in range(numVertices)]

        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, node_color=cores, node_size=800)
        plt.axis('off')
        plt.show()


def ler_arquivo_grafo(nome_arquivo, numero_vertices):
    grafo = Grafo(numero_vertices)
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(',')
            vertice1 = int(dados[0])
            vertice2 = int(dados[1])
            peso = int(dados[2])
            grafo.adicionarAresta(vertice1, vertice2, peso)
    return grafo

# altere o numero de vertices para o codigo não quebrar
grafo = ler_arquivo_grafo('estrela.txt', 40 )

# teste para ver se caminho minimo funciona
origem = 1
destino = 4
caminhoMinimo = grafo.encontraCaminhoMinimo(origem, destino)
print(f"\nCaminho minimo PARTINDO de ({origem}) PARA ({destino}): {caminhoMinimo}\n")

# betweeness com todos os caminhos minimos
valores = grafo.betweeness()

grafo.mostraGrafo()

#Plotando o grafo
grafo.plotarGrafo(valores)
