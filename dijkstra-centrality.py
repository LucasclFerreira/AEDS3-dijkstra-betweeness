import sys

class Grafo:
    def __init__(self, numVertices):
        self._numVertices = numVertices
        self.matAdj = [[sys.maxsize for _ in range(numVertices)] for _ in range(numVertices)]

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

    def mostraGrafo(self):
        print("  ", end="")
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
    

            

grafo = Grafo(4)
grafo.adicionarAresta(0, 1, 10)
grafo.adicionarAresta(1, 2, 40)
grafo.adicionarAresta(3, 2, 29)
grafo.adicionarAresta(0, 3, 33)
grafo.removerAresta(0, 3)

grafo.mostraGrafo()