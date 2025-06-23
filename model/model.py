import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self.best_sol = []
        self.album = None

    def buildGraph(self,l):
        self._graph.clear()
        allNodes = DAO.getAllAlbums(l)
        for node in allNodes:
            self._idMap[node.AlbumId] = node

        self._graph.add_nodes_from(allNodes)

        allEdges = DAO.getAllEdges(self._idMap)
        for edge in allEdges:
            self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]])

        return

    def getConnComp(self, album):
        self.album = album
        components = nx.connected_components(self._graph)
        for component in components:
            if album in component:
                self.conn_comp = component
                sum = 0
                for alb in component:
                    sum += alb.Lenght
                return len(component), sum

    def getSet(self, max_min):
        self.max_minutes = max_min
        self.best_sol = []
        parziale = [self.album]
        self.recursion(parziale)

    def recursion(self, parziale):
        if self.getSum(parziale) > self.max_minutes:
            return

        if len(parziale) > len(self.best_sol):
            self.best_sol = copy.deepcopy(parziale)

        for album in self.conn_comp:
            if album not in parziale:
                parziale.append(album)
                self.recursion(parziale)
                parziale.pop()

    def getSum(self, parziale):
        sum = 0
        for album in parziale:
            sum += album.Lenght
        return sum