from database.DAO import DAO
import networkx as nx
from geopy.distance import distance
import copy
import random

class Model:
    def __init__(self):
        self._bestComp = []
        self._grafo = nx.Graph()
        self._maxVicini = []


    def getProvider(self):
        provider = DAO.getProvider()
        return provider

    def getNodes(self, p):
        nodi = DAO.getLocations(p)
        return nodi

    def buildGraph(self, p, s):
        self._grafo.clear()
        nodi = self.getNodes(p)
        self._grafo.add_nodes_from(nodi)
        position = DAO.getPosition(p)
        for p1 in position:
            for p2 in position:
                if p1.Location != p2.Location:
                    distanza = distance((p1.Latitude, p1.Longitude), (p2.Latitude, p2.Longitude)).km
                    if float(distanza) < float(s):
                        self._grafo.add_edge(p1.Location, p2.Location, weight = distanza)

    def maxVicini(self):
        lista = []
        max = 0
        for n in self._grafo.nodes:
            vicini = self._grafo.neighbors(n)
            num = len(list(vicini))
            if num>max:
                max = num
        for n in self._grafo.nodes:
            vicini = self._grafo.neighbors(n)
            num = len(list(vicini))
            if num==max:
                lista.append(n)
                self._maxVicini.append(n)
        return lista, max

    def getPath(self, target, s):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        nodo = self._maxVicini[random.randint(0, len(self._maxVicini)-1)]
        # inizializzo il parziale con il nodo iniziale
        parziale = [nodo]
        self._ricorsione(parziale, target, s)
        return self._bestComp

    def _ricorsione(self, parziale, target, s):
        # verifico se soluzione è migliore di quella salvata in cache
        if parziale[-1] == target:
            if len(parziale) > len(self._bestComp):
                self._bestComp = copy.deepcopy(parziale)
            return

        # verifico se posso aggiungere un altro elemento
        for a in self._grafo.neighbors(parziale[-1]):
            if a not in parziale and s not in a:
                parziale.append(a)
                self._ricorsione(parziale, target, s)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking