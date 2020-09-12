import networkx as nx
import numpy as np
from utils.WDPair import WDPair

__all__ = ['wd']


def wd(graph: nx.DiGraph) -> (np.array, np.array):
    copy_graph = nx.DiGraph()
    delay = nx.get_node_attributes(graph, 'delay')
    n = graph.number_of_nodes()

    W = np.empty([n, n], dtype=np.int)
    D = np.empty([n, n])

    copy_graph.add_weighted_edges_from(
        [(u, v, WDPair(graph.edges[u, v]['weight'], -delay[u])) for (u, v) in graph.edges]
    )

    shortest_path_len = dict(floyd_warshall_predecessor_and_distance(copy_graph)[1])

    for u in copy_graph.nodes:
        for v in copy_graph.nodes:
            cw = shortest_path_len[u][v]
            W[int(u), int(v)] = cw.x
            D[int(u), int(v)] = delay[v] - cw.y

    return W, D


def floyd_warshall_predecessor_and_distance(G, weight='weight'):
    """
    Find all-pairs shortest path lengths using Floyd's algorithm.
    """
    from collections import defaultdict
    dist = defaultdict(lambda: defaultdict(lambda: WDPair(float('inf'), float('inf'))))
    for u in G:
        dist[u][u] = WDPair(0, 0)
    pred = defaultdict(dict)
    # initialize path distance dictionary to be the adjacency matrix
    # also set the distance to self to 0 (zero diagonal)
    undirected = not G.is_directed()
    for u, v, d in G.edges(data=True):
        e_weight = d.get(weight, 1.0)
        dist[u][v] = min(e_weight, dist[u][v])
        pred[u][v] = u
        if undirected:
            dist[v][u] = min(e_weight, dist[v][u])
            pred[v][u] = v
    for w in G:
        dist_w = dist[w]
        for u in G:
            dist_u = dist[u]
            for v in G:
                d = dist_u[w] + dist_w[v]
                if dist_u[v] > d:
                    dist_u[v] = d
                    pred[u][v] = pred[w][v]

    return dict(pred), dict(dist)