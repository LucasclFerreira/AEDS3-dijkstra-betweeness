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
        # vetor contendo a distancia da origem para cada vertice (indice). Inicialmente infinito
        distancias = [sys.maxsize for _ in range(self.numVertices)]

        # vetor que para cada vertice (indice) indica qual veio antes dele no caminho minimo. poderia ser inicializado com qualquer valor desde que não fosse o valor de algum vertice que existe no grafo
        antecessores = [sys.maxsize for _ in range(self.numVertices)]

        # a distancia da origem pra ela mesmo é zero claramente
        distancias[origem] = 0

        # quem veio antes dela mesma é a própria origem claramente
        antecessores[origem] = origem

        # a heap é uma lista de tuplas do formato (distancia, vertice)
        # essa heap é minima, ou seja, a tupla com o menor valor de distancia fica na cabeça da fila
        # lembrando que as operações de fila retiram nós da cabeça e inserem na cauda
        heap = [(0, origem)]

        # esse while executa enquanto a heap não for vazia
        while heap:
            # casamento de padrão retirando da fila o valor com a menor distancia e depois armazenando o valor do vertice atual na variavel
            _, verticeAtual = heapq.heappop(heap)

            # esse FOR atravessa todos os vertices para testarmos se ele tem aresta com o verticeAtual (lembre-se que estamos em uma matriz)
            for j in range(self.numVertices):
                # como usamos matriz de adjacencia devemos checar se o peso não é infinito (pois nesse caso o peso infinito indica que não há aresta entre dois vertices)
                if self._matAdj[verticeAtual][j] != sys.maxsize:
                    # calculamos a nova distancia olhando o vetor de distancias e somando com o peso da aresta que liga o verticeAtual ao vertice j
                    novaDistancia = distancias[verticeAtual] + self._matAdj[verticeAtual][j]
                    # se essa nova distancia for menor do que a que tinhamos armazenado no vetor distancia anteriormente, entramos no IF
                    if novaDistancia < distancias[j]:
                        # aqui dentro dizemos qual vertice veio antes do vertice j que adicionamos com a nova distancia
                        antecessores[j] = verticeAtual
                        # atualizamos a nova distance da origem até o vertice j
                        distancias[j] = novaDistancia
                        # e finalmente inserimos uma nova tupla contendo a novaDistancia e o j (que será o próximo vertice atual) na heap
                        heapq.heappush(heap, (novaDistancia, j))
        return distancias, antecessores

    def encontraCaminhoMinimo(self, origem, destino):
        # rodamos o dijkstra para a origem passada por paramentro para reconstruirmos o caminho minimo
        distancias, antecessores = self.dijkstra(origem)

        # o caminho começa vazio e valos preenche-lo
        caminho = []

        # aqui apenas testamos se é possível chegar até o vertice de destino ou não (se a distancia dele for infinita, então esse vertice é desconexo do restante do grafo)
        if distancias[destino] == sys.maxsize:
            return caminho
        
        # agora sim, devemos começar do final do caminho para chegarmos no começo
        atual = destino

        # enquanto não estivermos no vertice de origem exetamos o while
        while atual != origem:
            # devemos adicionar o vertice em que estamos no caminho
            caminho.append(atual)
            # e depois disso procuramos no vetor de antecessores qual vertice veio antes dele no caminho minimo
            atual = antecessores[atual]

        # depois de tudo ter sido realizado com sucesso teremos o caminho em ordem invertida, por isso usamos o reverse() para que fique na ordem normal
        caminho.reverse()

        # e por fim retornamos o caminho
        return caminho
    
    def betweeness(self):
        # o betweeness começa como um vetor de zeros (do tipo float)
        betweeness = [0.0 for _ in range(self.numVertices)]

        # usamos dois loops para atravessarmos todos os caminhos possiveis na nossa matriz
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                # para cada i e j chamamos o metodo encontraCaminhoMinimo que dentro dele chama o dijkstra ;)
                cam = self.encontraCaminhoMinimo(i, j)

                # checamos se o caminho não é vazio
                if len(cam) != 0:
                    # e agora devemos desconsiderar o ultimo vertice do caminho pois ele não entra no betweeness
                    # lembrando que o cam retornado pelo encontraCaminhoMinimo NÃO INCLUI o primeiro vertice do caminho
                    for v in range(len(cam) - 1):
                        # então para cada vertice que estiver nesse cam, usamos ele como inddice para somar +1 na sua posição no vetor betweeness
                        # exemplo: se cam fosse [3, 4] nós iriamos no betweenes[3] e somariamos +1 e também fariamos o mesmo na posição 4
                        # e lembrando que a posição no vetor representa o vertice em questão, ou seja, se a posição 1 do betweenes (bet[1]) for 0.66 então o vertice 1 tem o seu velor de centralidade betweenes igual a 0.66!
                        betweeness[cam[v]] += 1

        # por fim contamos todos os caminhos possíveis usando a formula (n * (n - 1)) / 2
        cont = (self.numVertices * self.numVertices - 1) / 2

        # e aqui estamos apenas divindo cada valor do betweenes pelo total de caminhos minimos
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
                if (self.matAdj[i][j] == sys.maxsize):
                    print(f"{0:>3}", end=" ")
                else:
                    print(f"{self.matAdj[i][j]:>3}", end=" ")
            print("")

    def plotarGrafo(self, betweeness):
        G = nx.Graph()
        numVertices = self.numVertices
        G.add_nodes_from(range(numVertices))

        for i in range(numVertices):
            for j in range(i + 1, numVertices):
                weight = self.matAdj[i][j]
                if weight != sys.maxsize:
                    G.add_edge(i, j)

        valores_centralidade = betweeness
        max_centralidade = max(valores_centralidade)
        min_centralidade = min(valores_centralidade)
        cmap = cm.get_cmap('coolwarm')
        cor_vertices = []

        for i in range(numVertices):
            cor_proporcional = 1.0 - (betweeness[i] - min_centralidade) / (max_centralidade - min_centralidade)
            r, g, b, _ = cmap(cor_proporcional)
            cor_vertices.append((r, g, b))

        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, node_color=cor_vertices, node_size=800)
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
grafo = ler_arquivo_grafo('grafo4.txt', 5)

# teste para ver se caminho minimo funciona
origem = 2
destino = 4
caminhoMinimo = grafo.encontraCaminhoMinimo(origem, destino)
print(f"\nCaminho minimo PARTINDO de ({origem}) PARA ({destino}): {caminhoMinimo}\n")

# betweeness com todos os caminhos minimos
betweeness = grafo.betweeness()
print("Betweeness implementado =", betweeness)

grafo.mostraGrafo()

#Plotando o grafo
grafo.plotarGrafo(betweeness)
