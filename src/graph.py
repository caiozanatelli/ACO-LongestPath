from collections import defaultdict
from utils import Utils

WEIGHT         = 'weight'
PHEROMONE      = 'pheromone'
INIT_PHEROMONE = 1

class Graph:
    '''A graph representation based on dictionaries'''

    def __init__(self):
        self.__vertices = {}
        self.__max_weight = 0

    def add_edge(self, source, dest, weight):
        '''
        Insert an edge into the graph.

        Arguments:
            [int] -- source vertex
            [int] -- destination vertex
            [int] -- edge weight
        '''
        if not source in self.__vertices.keys(): self.create_vertex(source)
        self.__vertices[source][dest] = {}
        if not dest in self.__vertices.keys(): self.create_vertex(dest)
        self.set_weight(source, dest, weight)
        self.set_pheromone(source, dest, INIT_PHEROMONE)
        self.__max_weight = max(self.__max_weight, weight)

    def create_vertex(self, source):
        '''Insert a vertex into the graph'''
        self.__vertices[source] = {}

    def set_pheromone(self, source, dest, pheromone):
        '''
        Update an edge pheromone to a new value.
        
        Arguments:
            [int] -- source vertex that identifies the edge
            [int] -- destination vertex that identifies the edge
            [int] -- new pheromone value to the edge
        '''
        self.__vertices[source][dest][PHEROMONE] = pheromone

    def get_pheromone(self, source, dest):
        '''
        Get the pheromone value associated to an edge.

        Arguments:
            [int] -- source vertex
            [int] -- destination vertex

        Returns:
            [int] -- the edge's pheromone value 
        '''
        return self.__vertices[source][dest][PHEROMONE]

    def set_weight(self, source, dest, weight):
        '''
        Update an edge weight to a new value.
        
        Arguments:
            [int] -- source vertex that identifies the edge
            [int] -- destination vertex that identifies the edge
            [int] -- new weight value to the edge
        '''
        self.__vertices[source][dest][WEIGHT] = weight

    def get_weight(self, source, dest):
        '''
        Get the weight value associated to an edge.

        Arguments:
            [int] -- source vertex
            [int] -- destination vertex

        Returns:
            [int] -- the edge's weight value 
        '''
        return self.__vertices[source][dest][WEIGHT]

    def get_edges(self):
        '''
        Get all the graph's edges.

        Returns:
            [dict] -- graph's edges.
        '''
        return self.__vertices

    def get_neighboors(self, vertex):
        '''
        Get an edge's adjacent vertices.

        Arguments:
            [int] -- source vertex

        Returns:
            [list] -- a list containing all the vertices adjacent to 'vertex'
        '''
        return [v for v in self.__vertices[vertex].keys()]

    def get_num_vertices(self):
        '''
        Get the graph's number of vertices.

        Returns:
            [int] -- the number of vertices that the graph contains
        '''
        return len(self.__vertices)

    def generate_path(self, source, dest):
        '''
        Generate a valid simple path from a source vertex to a destination
        vertex.

        Arguments:
            [int] -- source vertex
            [int] -- destination vertex

        Returns:
            [list] -- valid simple path from 'source' to 'destination'
        '''
        num_vertices = self.get_num_vertices()
        path = [source]
        random_vertex = source
        utils = Utils()
        count = 0

        # Generate vertices while we do not find a path to dest
        while random_vertex != dest:
            # Use probabilities for choosing a random vertex
            probs = utils.calculate_probabilities(self, source)
            random_vertex = utils.get_random_vertex(probs)

            # We try to find a path to dest. If there's none we return None
            tries = 0
            while random_vertex in path:
                random_vertex = utils.get_random_vertex(probs)
                tries += 1
                if tries > num_vertices: return None

            path.append(random_vertex)
            source = random_vertex
            count += 1
            if count > num_vertices: return None
        return path

    def is_path_simple(self, path):
        '''
        Check whether a path is simple.

        Arguments:
            [list] -- path for checking
        '''
        tmp_path = sorted(path)
        if len(tmp_path) > self.get_num_vertices():
            print('[+] The path has cycles.')
            return False
        
        previous = tmp_path.pop(0)
        for vertex in tmp_path:
            curr = vertex
            if curr == previous:
                print('[+] The path has cycles.')
                return False
            previous = curr

        return True

    def is_path_valid(self, path):
        '''
        Check whether a path is valid

        Arguments:
            [list] -- path for checking
        '''
        if len(path) == 0: return True
        tmp_path = [vertex for vertex in path]
        if not self.is_path_simple(path) or len(tmp_path) <= 0:
            print('[+] Invalid path.')
            return False
        
        previous = tmp_path.pop(0)
        for v in tmp_path:
            curr = v
            if not curr in self.__vertices[previous].keys():
                print('[+] Invalid path. No path from ' + str(previous) + \
                    'to ' + str(curr) + '.')
                return False
            previous = curr

        return True

    def calculate_fitness(self, path):
        '''
        Calculate the fitness of a path
        '''
        if len(path) == 0: return 0
        if not self.is_path_valid(path): return None
        # The path is valid, so we calculate its fitness and return it
        tmp_path = [vertex for vertex in path]
        sum_weight = 0
        source = tmp_path.pop(0)
        for dest in tmp_path:
            weight = self.get_weight(source, dest)
            sum_weight += weight
            source = dest
        return sum_weight

    def evaporate_pheromones(self, evaporation_rate):
        '''
        Evaporate the pheromone of all edges based on the decay rate set previously.

        Arguments:
            [float] -- decay rate for the pheromone update
        '''
        for source in self.__vertices.keys():
            for dest in self.__vertices[source].keys():
                curr_pheromone = self.get_pheromone(source, dest)
                self.set_pheromone(source, dest, curr_pheromone*(1-evaporation_rate))
        