import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._allNodes = []
        self._idMapProdotti = {}
        self._risultato = {}

    def buildGraph(self, categoria, dataI, dataF):
        self._graph.clear()
        self._graph.clear_edges()
        self._idMapProdotti.clear()
        self._risultato.clear()

        self._allNodes = DAO.getAllNodes(categoria.category_id)
        for p in self._allNodes:
            self._idMapProdotti[p.product_id] = p

        self._graph.add_nodes_from(self._allNodes)
        self.addEdges(dataI, dataF)

    def addEdges(self, dataI, dataF):
        listaId, listaIdVendite = DAO.getAllEdges(dataI, dataF)

        for idP in listaId:
            if idP not in self._idMapProdotti.keys():
                listaId.remove(idP)

        listaCoppie = itertools.combinations(listaId, 2)
        for tupla in listaCoppie:
            if tupla[0] in self._idMapProdotti.keys() and tupla[1] in self._idMapProdotti.keys():
                p1 = self._idMapProdotti[tupla[0]]
                p2 = self._idMapProdotti[tupla[1]]
                v1 = self.getVendite(tupla[0], listaIdVendite)
                v2 = self.getVendite(tupla[1], listaIdVendite)
                if v1 > v2:
                    self._graph.add_edge(p1, p2, weight = v1+v2)
                if v2 > v1:
                    self._graph.add_edge(p2, p1, weight = v2+v1)
                if v1 == v2:
                    self._graph.add_edge(p1, p2, weight = v1+v2)
                    self._graph.add_edge(p2, p1, weight= v2+v1)

    def getVendite(self, id, listaIdVendite):
        for tupla in listaIdVendite:
            if tupla[0] == id:
                return tupla[1]
        return None

    def getTop5(self):
        lista = []
        for n in self._graph.nodes:
            sommaU = 0
            sommaE = 0
            uscenti = self._graph.out_edges(n, data=True)
            entranti = self._graph.in_edges(n, data=True)
            for u,v,peso in uscenti:
                sommaU+=peso['weight']
            for u,v,peso in entranti:
                sommaE+=peso['weight']
            lista.append((n,sommaU-sommaE))
        result = sorted(lista, key=lambda x: x[1], reverse=True)
        return result[:5]

    def getAllCategory(self):
        return DAO.getAllCategory()

    def getAllProducts(self):
        return self._allNodes

    def getDateRange(self):
        return DAO.getDateRange()

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)