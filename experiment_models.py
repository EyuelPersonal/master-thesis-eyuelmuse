
from models import Network, BipartateNetwork, Hypergraph
from pydantic import BaseModel
from matplotlib import pyplot as plt
import numpy as np
from typing import Union
import networkx as nx

class Experiment(BaseModel):
    """
    This class is used to run experiments on networks. It is a wrapper around the Network class.
    Attributes:
        name (str): The name of the experiment.
        network (Union[Network, BipartateNetwork, Hypergraph]): The network to run the experiment on.
        next_network (nx.Graph): The next network to run the experiment on.
        timestamp (int): The timestamp of the experiment.
        alpha (float): The alpha value of the experiment.
        dt (float): The dt value of the experiment.
        degree_dict (dict): Dictionary to store the degree distribution of the network.
        degree_sequence (list[int]): The degree sequence of the network.
        ordered_degree (dict): The ordered degree of the network.
        connected_components (float): The number of connected components of the network.
        removed_nodes (list[list]): The list of removed nodes.
    """
    name: str
    network: Union[Network, BipartateNetwork, Hypergraph]
    next_network: nx.Graph = None
    timesatmp: int = 0
    alpha: float = 1.0
    dt: float = 0.01
    degree_dict: dict = None
    degree_sequence: list[int] = []
    ordered_degree: dict = None
    connected_components: float = 0.0
    removed_nodes: list[list] = None
    class Config:
        arbitrary_types_allowed = True

    def nodes_to_remove(self, n, random=True):
        if random:
            self.removed_nodes = np.random.choice(list(self.network.G.nodes), n, replace=False)
        else:
            self.removed_nodes = list(self.ordered_degree.keys())[:n]
    
    def initialize(self):
        self.network.pos = nx.spring_layout(self.network)
        theta = 2 * np.pi * np.random.rand()
        omega = 2 * np.pi * np.random.rand()
        nx.set_node_attributes(self.network, theta, 'theta')
        nx.set_node_attributes(self.network, omega, 'omega')
        self.next_network = self.network.copy()

    def visualize(self):
        plt.figure(figsize=(8, 8))
        plt.axis('off')
        ax = 1,
            
        nx.draw(
            self.network,
            #pos=self.network.pos,
            node_color=[
                np.sin(self.network.G.nodes[v]['theta']) 
                for v in self.network.G.nodes
                ],
            cmap=plt.cm.hsv,
            node_size=100,
            alpha=0.8
        )
        plt.show()

    def update(self):
        for i in self.network.G.nodes:
            self.next_network.nodes[i]['theta'] = (
                self.network.G.nodes[i]['theta'] + (
                    self.network.G.nodes[i]['omega'] + self.alpha * (
                        np.sum([
                            np.sin(self.network.G.nodes[j]['theta'] - 
                                   self.network.G.nodes[i]['theta']) 
                                   for j in self.network.G.neighbors(i)
                        ]) / self.network.degree(i) * self.dt
                    )))
        self.network, self.next_network = self.next_network, self.network

        
    def _degree_sequence(self):
        self.degree_sequence =  sorted((
                                        d for n, d in self.network.degree_centrality
                                        ), reverse=True)
    def _ordered_degree(self):
        self.ordered_degree =  dict(sorted(
                                            self.degree_dict.items(), 
                                            key=lambda item: item[1], 
                                            reverse=True
                                            ))
    def _degree_dict(self):
        self.degree_dict = dict(self.network.degree_centrality)

    def _connected_components(self):
        self.connected_components = self.network.connected_components
    
    def compute_metrics(self):
        self.network.compute_metrics()
        self._degree_dict()
        self._degree_sequence()
        self._ordered_degree()
        self._connected_components()

    def remove_nodes(self, nodes: list = None):
        if nodes:
            self.removed_nodes = nodes
            self.network.G.remove_nodes_from(self.removed_nodes)
        else:
            self.network.G.remove_nodes_from(self.removed_nodes)
        self.compute_metrics()

class SpreadingPhenomena(Experiment):
    """
    This class is used to run experiments on networks. It is extends the Experiemnt class.
    Attributes:
        beta (float): Possible infection rate of the network.
        n_infected (int): The number of infected nodes in the network.
        n_susceptible (int): The number of susceptible nodes in the network.
        N (int): The total number of nodes in the network.
        rate_of_spread (float): The rate of spread of the infection in the network.
        timesatmp (int): The timestamp of the experiment.
    """
    beta: float = 0.1
    n_infected: int = 0
    n_susceptible: int = 0
    N: int = 0
    rate_of_spread: float = 0.0
    timesatmp: int = 0

    def initialize(self):
        for i in list(self.network.G.nodes):
            self.network.G.nodes[i]['Infected'] = 0
        infected = np.random.choice(list(self.network.G.nodes))
        self.N = len(self.network.G.nodes)
        self.n_susceptible = len(self.network.G.nodes) - 1
        self.timesatmp = 0
        self.network.G.nodes[infected]['Infected'] = 1
        self.n_infected = 1
        self.next_network = self.network.copy()

    def _rate_of_spread(self):
        return self.n_infected / self.N

    def spreading(self):
        for i in self.network.G.nodes:
            if self.network.G.nodes[i]['Infected'] == 1:
                for j in self.network.G.neighbors(i):
                    if self.network.G.nodes[j]['Infected'] == 0:
                        if np.random.rand() < self.beta:
                            self.network.G.nodes[j]['Infected'] = 1
                            self.n_susceptible -= 1
                            self.n_infected += 1
        self.timesatmp += 1
        self.rate_of_spread = self._rate_of_spread()