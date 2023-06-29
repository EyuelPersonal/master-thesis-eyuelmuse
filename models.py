from pydantic import BaseModel
from utils import build_network, build_bipartate_network, build_hypergraph
from plots import degree_plots, log_log_plot 
import networkx as nx
import xgi
import numpy as np
import scipy

class Network(BaseModel):
    """
    This class is used to store the network data and its compute its attributes.
    Attributes:
        name (str): The name of the network.
        description (str): The description of the network.
        node_attributes (list[dict]): The node attributes of the network.
        data (list[dict]): The data of the network.
        timestamp (int): The timestamp of the network.
        G (nx.Graph): The networkx graph of the network.
        degree_centrality (dict): The degree centrality of the network.
        degree_sequence (list): The degree sequence of the network.
        eigenvector_centrality (dict): The eigenvector centrality of the network.
        pagerank (dict): The pagerank of the network.
        betweenness_centrality (dict): The betweenness centrality of the network.
        closeness_centrality (dict): The closeness centrality of the network.
        clustering (dict): The clustering of the network.
        average_clustering (float): The average clustering of the network.
        average_shortest_path_length (list): The average shortest path length of the network.
        connected_components (int): The number of connected components of the network.
        initial_connected_components (int): The number of connected components of the initial network.
        init (bool): Whether the network is initialized or not.
        largest_component (float): The largest component of the network.
    """
    name: str
    description: str
    node_attributes: list[dict]
    data: list[dict]
    timestamp: int = 0
    G: nx.Graph = None
    degree_centrality: dict = None
    degree_sequence: list = None
    eigenvector_centrality: dict = None
    pagerank: dict = None
    betweenness_centrality: dict = None
    closeness_centrality: dict = None
    clustering: dict = None
    average_clustering: float = None
    average_shortest_path_length: list = None
    connected_components: int = None
    initial_connected_components: int = None
    init: bool = True
    largest_component: float = 0.0
    initial_largest_component: float = 0.0

    class Config:
        arbitrary_types_allowed = True

    def _network(self):
        self.G = build_network(self.data, self.node_attributes, True)

    def _degree_centrality(self):
        self.degree_centrality = self.G.degree(weight='weight')
        self.degree_sequence = sorted([d for n, d in self.G.degree()], reverse=True)
        if self.init:
            degree_plots(self.degree_sequence)
            log_log_plot(self.degree_sequence)

    def _eigenvector_centrality(self):
        self.eigenvector_centrality = nx.eigenvector_centrality(
            self.G, max_iter=1000, 
            tol=1e-06,
            weight='weight'
            )

    def _pagerank(self):
        self.pagerank = nx.pagerank(self.G, alpha=0.85, weight='weight')

    def _betweenness_centrality(self):
        self.betweenness_centrality = nx.betweenness_centrality(self.G, weight='weight')

    def _closeness_centrality(self):
        self.closeness_centrality = nx.closeness_centrality(self.G)

    def _clustering(self):
        self.clustering = nx.clustering(self.G, weight='weight')

    def _average_clustering(self):
        self.average_clustering = nx.average_clustering(self.G, weight='weight')

    def _average_shortest_path_length(self):
        self.average_shortest_path_length = []
        subgraphs = nx.connected_components(self.G)
        for i in subgraphs:
            sub = self.G.subgraph(i)
            self.average_shortest_path_length.append(
                (
                    nx.average_shortest_path_length(sub), 
                    len(i)
                )
            )

    def _connected_components(self):
        if self.init == False:
            self.connected_components =  len([
                                                i for i in 
                                                nx.connected_components(
                                                    nx.Graph(self.G)
                                            )])
            self.largest_component = len(sorted([
                                i for i in 
                                nx.connected_components(
                                nx.Graph(self.G)
                            )])[0])/len(self.G.nodes)
        else:
            self.initial_connected_components =  len([
                                                        i for i in 
                                                        nx.connected_components(
                                                            nx.Graph(self.G)
                                                    )])
            self.initial_largest_component = len(sorted([
                                i for i in 
                                nx.connected_components(
                                nx.Graph(self.G)
                            )])[0])/len(self.G.nodes)

    def compute_metrics(self):
        self._degree_centrality()
        self._eigenvector_centrality()
        self._pagerank()
        self._betweenness_centrality()
        self._closeness_centrality()
        self._clustering()
        self._average_clustering()
        self._average_shortest_path_length()
        self._connected_components()
        self.init = False

class BipartateNetwork(BaseModel):
    """
    This class represents a bipartate network. And is used to store the network, its data and its metrics.
    Attributes:
        name (str): The name of the network.
        description (str): The description of the network.
        data (list): The data of the network.
        timestamp (int): The timestamp of the network.
        G (nx.Graph): The networkx graph of the network.
        degree_centrality (dict): The degree centrality of the network.
        degree_sequence (list): The degree sequence of the network.
        eigenvector_centrality (dict): The eigenvector centrality of the network.
        pagerank (dict): The pagerank of the network.
        betweenness_centrality (dict): The betweenness centrality of the network.
        closeness_centrality (dict): The closeness centrality of the network.
        clustering (dict): The clustering of the network.
        average_clustering (float): The average clustering of the network.
        average_shortest_path_length (list): The average shortest path length of the network.
        connected_components (int): The connected components of the network.
        initial_connected_components (int): The initial connected components of the network.
        init (bool): The init of the network.
        largest_component (float): The largest component of the network.
        initial_largest_component (float): The initial largest component of the network.
    """
    name: str
    description: str
    data:list[dict]
    timestamp: int = 0
    G: nx.Graph = None
    degree_centrality: dict = None
    degree_sequence: list = None
    eigenvector_centrality: dict = None
    pagerank: dict = None
    betweenness_centrality: dict = None
    closeness_centrality: dict = None
    clustering: dict = None
    average_clustering: float = None
    average_shortest_path_length: list = None
    connected_components: int = None
    initial_connected_components: int = None
    init: bool = True
    largest_component: float = 0.0
    initial_largest_component: float = 0.0

    class Config:
        arbitrary_types_allowed = True

    def _network(self):
        self.G = build_bipartate_network(self.data)

    def _degree_centrality(self):
        self.degree_centrality = self.G.degree()
        self.degree_sequence = sorted([d for n, d in self.G.degree()], reverse=True)
        if self.init:
            degree_plots(self.degree_sequence)
            log_log_plot(self.degree_sequence)

    def _betweenness_centrality(self):
        self.betweenness_centrality = nx.betweenness_centrality(self.G)

    def _closeness_centrality(self):
        self.closeness_centrality = nx.closeness_centrality(self.G)

    def _clustering(self):
        self.clustering = nx.clustering(self.G)

    def _average_clustering(self):
        self.average_clustering = nx.average_clustering(self.G)

    def _connected_components(self):
        if self.init == False:
            self.connected_components =  len([
                                                i for i in 
                                                nx.connected_components(
                                                    nx.Graph(self.G)
                                            )])
            self.largest_component = len(sorted([
                                i for i in 
                                nx.connected_components(
                                nx.Graph(self.G)
                            )])[0])/len(self.G.nodes)
        else:
            self.initial_connected_components =  len([
                                                        i for i in 
                                                        nx.connected_components(
                                                            nx.Graph(self.G)
                                                    )])
            self.initial_largest_component = len(sorted([
                                i for i in 
                                nx.connected_components(
                                nx.Graph(self.G)
                            )])[0])/len(self.G.nodes)

    def compute_metrics(self):
        self._degree_centrality()
        self._betweenness_centrality()
        self._closeness_centrality()
        self._clustering()
        self._average_clustering()
        self._connected_components()
        self.init = False

class Hypergraph(BaseModel):
    """
    This class represents a hypergraph. And is used to store the network, its data and its metrics.
    Attributes:
        name (str): The name of the network.
        description (str): The description of the network.
        node_attributes (list): The node attributes of the network.
        data (list): The data of the network.
        timestamp (int): The timestamp of the network.
        G (xgi.Hypergraph): The xgraph graph of the network.
        degree_centrality (dict): The degree centrality of the network.
        degree_sequence (list): The degree sequence of the network.
    """
    name: str
    description: str
    node_attributes: list[dict]
    data: list[dict]
    timestamp: int = 0
    G: xgi.Hypergraph = None
    degree_centrality: dict = None
    degree_sequence: list = None

    class Config:
        arbitrary_types_allowed = True

    def _network(self):
        self.G = build_hypergraph(
            self.data,
            self.node_attributes)
    def _degree_centrality(self):
        self.degree_centrality = self.G.degree()
        self.degree_sequence = sorted([d for n, d in self.G.degree()], reverse=True)
        if self.init:
            degree_plots(self.degree_sequence)
            log_log_plot(self.degree_sequence)

class EigenValueCentrality(Hypergraph):
    """
    This class extends the Hypergraph class and is used to compute the eigenvalue centrality of the network.
    Attributes:
        eigen_centrality (dict): The eigenvalue centrality of the network.
        eig_vals (np.ndarray): The eigenvalues of the network.
        eig_vecs (np.ndarray): The eigenvectors of the network.
        click_matrix (np.ndarray): The click matrix of the network.
        nodes (np.ndarray): The nodes of the network.
        cpms (list): The cpms in the network.
        eigen_centrality_cpms (dict): The eigenvalue centrality cpms in the network.
    """
    eigen_centrality:dict = None
    eig_vals:np.ndarray = None
    eig_vecs:np.ndarray = None
    click_matrix:np.ndarray = None
    nodes:np.ndarray = None
    cpms:list = None
    eigen_centrality_cpms:dict = None

    def largest_component(self):
        largest_component = [i for i in xgi.connected_components(self.G)][0]
        self.G = xgi.subhypergraph(self.G, largest_component)
    def get_click_matrix(self):
        self.click_matrix = xgi.clique_motif_matrix(self.G).todense()
    def compute_eigen_vs(self):
        self.eig_vals, self.eig_vecs = scipy.linalg.eig(self.click_matrix)
    def compute_eigen_centrality(self):
        largest_eigval = np.argmax(self.eig_vals)
        self.eigen_centrality = abs(self.eig_vecs[:,largest_eigval])
    def compute(self):
        self.nodes = np.array(list(self.G.nodes))
        self.cpms = list(self.G.nodes.filterby_attr('position', 'PROJECTMANAGER'))
        self.largest_component()
        self.get_click_matrix()
        self.compute_eigen_vs()
        self.compute_eigen_centrality()
        self.eigen_centrality = dict(zip(self.nodes, self.eigen_centrality))
        self.eigen_centrality_cpms = {k:v for k,v in self.eigen_centrality.items() if k in self.cpms}