from graph import Graph
from utils import Utils
from ioutils import IOUtils

PHEROMONE_INCREMENT = 3

class ACO:
    '''An ant colony system representation'''
    def __init__(self, graph, iterations, num_ants, evaporation_rate, seed, log):
        self.__graph = graph
        self.__num_ants = num_ants
        self.__iterations = iterations
        self.__evaporation_rate = evaporation_rate
        Utils().set_seed(seed)
        IOUtils().open_log(log)

    def optimize(self):
        '''
        Main method for optimizing a graph problem (in this case, the longest path problem)
        '''
        count = 0
        max_fitness = 0
        avg_fitness = 0
        best_path   = [] # Best solution
        ioutils = IOUtils()
        
        # Iterate N times: build and evaluate solutions and update the graph pheromones
        while count < self.__iterations:
            result = self.build_solution()
            curr_fitness = self.__graph.calculate_fitness(result)
            avg_fitness  += curr_fitness
            if curr_fitness > max_fitness:
                best_path = result
                max_fitness = curr_fitness
            self.__graph.evaporate_pheromones(self.__evaporation_rate)
            count += 1
            ioutils.save_data(str(count) + ',' + str(max_fitness) + ',' + str(avg_fitness/count))

        avg_fitness /= count

        return {'path': best_path, 'avg_fitness': avg_fitness}

    def build_solution(self):
        '''
        Build up N solutions -- one for each ant in the colony. All the solutions are valid
        simple paths in the given graph.

        Returns:
            [list] -- the best path found amongst the N ones created.
        '''
        source = 1
        dest   = self.__graph.get_num_vertices()
        paths  = []
        utils  = Utils()

        # Generate N valid simple paths
        for i in range(self.__num_ants):
            curr_path = self.__graph.generate_path(source, dest)
            if curr_path is not None:
                paths.append(curr_path)

        # Evaluate each path, get the best one and update the graph pheromones
        max_fitness = 0
        for path in paths:
            path_fitness = self.__graph.calculate_fitness(path)
            if path_fitness > max_fitness:
                best_path = [vertex for vertex in path]
                max_fitness = path_fitness

            source = path.pop(0)
            for dest in path:
                pheromone = self.__graph.get_pheromone(source, dest)
                pheromone += PHEROMONE_INCREMENT
                self.__graph.set_pheromone(source, dest, pheromone)
                source = dest

        # Update the best path pheromone in the graph
        tmp_path = [vertex for vertex in best_path]
        source = tmp_path.pop(0)
        for dest in tmp_path:
            pheromone = self.__graph.get_pheromone(source, dest)
            pheromone += PHEROMONE_INCREMENT
            self.__graph.set_pheromone(source, dest, pheromone)
            source = dest

        return best_path

