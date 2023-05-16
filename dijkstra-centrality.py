import sys
from queue import PriorityQueue

class Grafo:
    def __init__(self, numVertices):
        self._numVertices = numVertices
        self.matAdj = [[sys.maxsize if i != j else 0 for j in range(numVertices)] for i in range(numVertices)]

    @property
    def numVertices(self):
        return self._numVertices

    @numVertices.setter
    def numVertices(self, numVertices):
        self._numVertices = numVertices

    def adicionarAresta(self, verticeA, verticeB, peso):
        self.matAdj[verticeA][verticeB] = peso
    
    def removerAresta(self, verticeA, verticeB):
        self.matAdj[verticeA][verticeB] = sys.maxsize

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
                if self.matAdj[verticeAtual][j] != 0:
                    novaDistancia = distancias[verticeAtual] + self.matAdj[verticeAtual][j]
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
                if (self.matAdj[i][j] == sys.maxsize):
                    print(f"{0:>3}", end=" ")
                else:
                    print(f"{self.matAdj[i][j]:>3}", end=" ")
            print("")

grafo = Grafo(5)
grafo.adicionarAresta(0, 1, 4)
grafo.adicionarAresta(0, 2, 1)
grafo.adicionarAresta(1, 3, 1)
grafo.adicionarAresta(2, 1, 2)
grafo.adicionarAresta(2, 3, 5)
grafo.adicionarAresta(3, 4, 3)

caminhoMinimo = grafo.dijkstra(0)  # partindo do vértice 0, encontre o caminho mínimo

grafo.mostraGrafo()

print(f"\nCaminho Mínimo partindo do vértice 0 e len(caminhoMinimo) = {len(caminhoMinimo)}: ")
for i in range(len(caminhoMinimo)):
    print(f"{caminhoMinimo[i]}", end=" ")
