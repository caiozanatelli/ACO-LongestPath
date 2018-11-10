import random

class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class Utils(object):
    __metaclass__ = Singleton

    def __init__(self, seed=None):
        if seed is not None:
            self.set_seed(seed)

    def set_seed(self, seed):
        '''
        Set the seed for random number generation.

        Arguments:
            [int] -- the seed to be used
        '''
        random.seed(seed)
    
    def get_random_vertex(self, probabilities):
        '''
        Get a random vertex according to given probabilities.

        Arguments:
            [list] -- probabilities to consider.

        Returns:
            [int] -- the vertice chosen
        '''
        r = random.uniform(0, sum(iter(probabilities.values())))
        s = 0.0
        for k, w in iter(probabilities.items()):
            s += w
            if r < s: return k
        return k

    def calculate_probabilities(self, graph, vertex):
        '''
        Calculate probabilities for choosing the next vertex.

        Arguments:
            [dict] -- graph representing the problem
            [int] -- vertex for which we should calculate probabilities
        '''
        adjacents = graph.get_neighboors(vertex)
        probabilities = {}
        for dest in adjacents:
            curr_weight = graph.get_weight(vertex, dest)
            curr_pheromone = graph.get_pheromone(vertex, dest)
            probabilities[dest] = curr_weight * curr_pheromone

        total_values = sum(float(probabilities[d]) for d in probabilities.keys())
        for dest in probabilities:
            probabilities[dest] /= total_values

        return probabilities
    