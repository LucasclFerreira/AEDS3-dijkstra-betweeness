import sys
import heapq
import networkx as nx
import matplotlib.pyplot as plt

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
        cont = self.numVertices * self.numVertices - 1
        for i in range(self.numVertices):
            betweeness[i] /= cont
        return betweeness

    def mostraGrafo(self):
        print("    ", end="")
        for i in range(self.numVertices):
            print(f" {i}: ", end="")
        print("")
        for i in range(self.numVertices):
            print(f" {i}: ", end="")
            for j in range(self.numVertices):
                if (self._matAdj[i][j] == sys.maxsize):
                    print(f"{0:>3}", end=" ")
                else:
                    print(f"{self._matAdj[i][j]:>3}", end=" ")
            print("")

    def plotarGrafo(self):
        G = nx.Graph()
        numVertices = len(grafo._matAdj)
        numvertices = grafo.numVertices
        G.add_nodes_from(range(numvertices))

        for i in range(numvertices):
            for j in range(i + 1, numvertices):
                weight = grafo._matAdj[i][j]
                if weight != sys.maxsize:
                    G.add_edge(i, j, weight=weight)

        pos = nx.spring_layout(G)  # Layout para posicionar os nós
        edge_labels = nx.get_edge_attributes(G, 'weight')  # Rótulos das arestas
        nx.draw_networkx(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.show()

grafo = Grafo(5)
grafo.adicionarAresta(0, 1, 4)
grafo.adicionarAresta(0, 2, 1)
grafo.adicionarAresta(1, 3, 1)
grafo.adicionarAresta(2, 1, 2)
grafo.adicionarAresta(2, 3, 5)
grafo.adicionarAresta(3, 4, 3)

origem = 1
destino = 4
caminhoMinimo = grafo.encontraCaminhoMinimo(origem, destino)
print(f"\nCaminho minimo PARTINDO de ({origem}) PARA ({destino}): {caminhoMinimo}\n")
print("Betweeness implementado =", grafo.betweeness())

# o código abaixo serve apenas para comparar os resultados do betweeness implementado e o da biblioteca NetworkX
G = nx.DiGraph()
G.add_edge(0, 1, weight=4)
G.add_edge(0, 2, weight=1)
G.add_edge(1, 3, weight=1)
G.add_edge(2, 1, weight=2)
G.add_edge(2, 3, weight=5)
G.add_edge(3, 4, weight=3)
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
print("Betweenness do NetworkX =", betweenness_centrality)


grafo.mostraGrafo()

#Plotando o grafo
grafo.plotarGrafo()
