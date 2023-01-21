import pickle
from typing import Any, Dict, List

import holoviews as hv
import matplotlib.pyplot as plt
import networkx as nx
from holoviews.operation.datashader import bundle_graph, datashade
from holoviews.util import save
from prefect import flow, task
from rdflib.namespace import split_uri

from config import Location


@task
def load_network(path: str) -> nx.MultiDiGraph:
    with open(path, "rb") as f:
        graph = pickle.load(f)
    return graph


@task
def save_viz(graph: nx.MultiDiGraph, path: str):
    pos = nx.kamada_kawai_layout(graph)
    plt.figure(figsize=(20, 20))
    nx.draw_networkx_nodes(
        graph, pos, node_size=3, node_color="#210070", alpha=0.9
    )
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos, font_size=14)
    nx.draw_networkx_edge_labels(graph, pos)
    plt.savefig(path)


@flow
def make_plot(location: Location = Location()):
    nx_network = load_network(location.network)
    save_viz(nx_network, location.plot)


if __name__ == "__main__":
    make_plot()
