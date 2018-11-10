from graph import Graph
import sys

class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class IOUtils(object):
    '''
    A generic class for input and output manipulation.
    '''
    __metaclass__ = Singleton
    __logfile = None

    def __init__(self, logpath=None):
        if not logpath is None:
            self.open_log(logpath)

    def read_input(self, filepath):
        '''
        Read a text input in the format: u v p
        where u is the source vertex, v is the destination vertex, and p
        is the weight associated to the edge (u, v).

        Arguments:
            [str] -- path of the input file.

        Returns:
            [dict] -- a dictionary representing the graph.
        '''
        graph = Graph()
        with open(filepath) as fp:
            for row in fp:
                edge = [int(x) for x in row.split('\t')]
                graph.add_edge(edge[0], edge[1], edge[2])
        return graph 
    
    def save_data(self, data):
        '''
        Save a string data to the log file

        Arguments:
            [str] -- the string to be stored
        '''
        if self.__logfile is None:
            print('Log file not opened.')
        else:
            self.__logfile.write(data + '\n')

    def open_log(self, filepath):
        '''
        Open the log file for storing partial results
        
        Arguments:
            [str] -- path of a file for logging purposes
        '''
        self.__logfile = open(filepath, 'w')
