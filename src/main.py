from graph import Graph
from ioutils import IOUtils
from aco import ACO
import argparse

def parser_args():
    '''
    Parse command line arguments.

    Returns: 
        [args] -- a structure containing all the arguments parsed.
    '''
    parser = argparse.ArgumentParser(description='An ACO (Ant Colony Optimization) \
                algorithm for solving the Longest Path Problem in directed and \
                weighted graphs')
    parser.add_argument('-input', '--input', action='store', type=str, required=True,
                        help='Input file describing the graph')
    parser.add_argument('-output', '--output', action='store', type=str, required=True,
                        help='Output file for storing the results')
    parser.add_argument('-n', '--ants', action='store', type=int, default=10,
                        help='Number of ants in the colony')
    parser.add_argument('-i', '--iterations', action='store', type=int, default=100,
                        help='Number of iterations for the ACO algorithm to perform')
    parser.add_argument('-e', '--evaporation-rate', action='store', type=float, default=0.1,
                        help='Decay rate for the pheromones')
    parser.add_argument('-s', '--seed', action='store', type=int, default=1, 
                        help='Seed for controlled random number genaration')
    return parser.parse_args()

def main(args):
    '''
    Controls the program flow. Reads the input, generates the associated graph, calls the
    optimizing process through ACO and print the best solution found.
    '''
    ioutils = IOUtils()
    graph = ioutils.read_input(args.input)
    aco   = ACO(graph, args.iterations, args.ants, args.evaporation_rate, args.seed, args.output)
    solution = aco.optimize()

    best_path = solution['path']
    print(str(graph.calculate_fitness(best_path)) + ',' + str(solution['avg_fitness']))

if __name__ == '__main__':
    args = parser_args()
    main(args)
