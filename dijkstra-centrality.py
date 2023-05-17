import sys
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, numVertices):
        self.__numVertices = numVertices
        self.__matAdj = [[sys.maxsize if i != j else 0 for j in range(numVertices)] for i in range(numVertices)]

    @property
    def numVertices(self):
        return self.__numVertices

    # @numVertices.setter
    # def numVertices(self, numVertices):
    #     self.__numVertices = numVertices

    def adicionarAresta(self, verticeA, verticeB, peso):
        self.__matAdj[verticeA][verticeB] = peso
        self.__matAdj[verticeB][verticeA] = peso
    
    def removerAresta(self, verticeA, verticeB):
        self.__matAdj[verticeA][verticeB] = sys.maxsize

    def dijkstra(self, posicao):
        visitados = [False for _ in range(self.numVertices)]
        distancias = [float('inf') for _ in range(self.numVertices)]
        distancias[posicao] = 0

        for i in range(self.numVertices):
            verticeAtual = -1
            for j in range(self.numVertices):
                if not visitados[j] and (verticeAtual == -1 or distancias[j] < distancias[verticeAtual]):
                    verticeAtual = j
            visitados[verticeAtual] = True
            for j in range(self.numVertices):
                if self.__matAdj[verticeAtual][j] != sys.maxsize:
                    novaDistancia = distancias[verticeAtual] + self.__matAdj[verticeAtual][j]
                    if novaDistancia < distancias[j]:
                        distancias[j] = novaDistancia
        return distancias

    def mostraGrafo(self):
        print("    ", end="")
        for i in range(self.numVertices):
            print(f" {i}: ", end="")
        print("")
        for i in range(self.numVertices):
            print(f" {i}: ", end="")
            for j in range(self.numVertices):
                if (self.__matAdj[i][j] == sys.maxsize):
                    print(f"{0:>3}", end=" ")
                else:
                    print(f"{self.__matAdj[i][j]:>3}", end=" ")
            print("")

    def plotarGrafo(self):
        G = nx.Graph()
        numVertices = len(grafo.__matAdj)
        numvertices = grafo.numVertices
        G.add_nodes_from(range(numvertices))

        for i in range(numvertices):
            for j in range(i + 1, numvertices):
                weight = grafo.__matAdj[i][j]
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

caminhoMinimo = grafo.dijkstra(0)  # partindo do vértice 0, encontre o caminho mínimo

grafo.mostraGrafo()

#Plotando o grafo
grafo.plotarGrafo()

print(f"\nCaminho Mínimo partindo do vértice 0 e len(caminhoMinimo) = {len(caminhoMinimo)}: ")
for i in range(len(caminhoMinimo)):
    print(f"{caminhoMinimo[i]}", end=" ")
