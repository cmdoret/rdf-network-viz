import pickle

import networkx as nx
from prefect import flow, task
from rdflib import Graph
from rdflib.namespace import RDF, Namespace, split_uri

from config import Location

SDO = Namespace("http://schema.org/")
GHA = Namespace("https://api.github.com/")


@task
def load_triples(path: str) -> Graph:
    g = Graph().parse(path)  # type: ignore
    g.bind("schema", SDO)
    g.bind("github", GHA)

    return g


@task
def filter_triples(triples: Graph) -> Graph:
    return triples


@task
def rdf_to_networkx(triples: Graph) -> nx.MultiDiGraph:
    uris = set(triples.subjects())
    graph = nx.MultiDiGraph()
    # Iteratively add nodes and associated edges
    for uri in uris:
        # Find all outgoing edges from node
        props = triples.predicate_objects(uri)

        # linking 2 instances (object prop.) -> edges
        o_props = {split_uri(p)[1]: o for p, o in props if o in uris}
        for p, o in o_props.items():
            graph.add_edge(uri, o, pred=p)

        # Other properties: node attributes
        d_props = {split_uri(p)[1]: o for p, o in props if o not in uris}
        graph.add_node(str(uri), **d_props)
    return graph


@task
def adjust_weights(network: nx.MultiDiGraph) -> nx.MultiDiGraph:
    return network


@task
def save_network(network: nx.MultiDiGraph, path: str):
    with open(path, "wb") as f:
        pickle.dump(network, f, pickle.HIGHEST_PROTOCOL)


@flow
def process_graph(location: Location = Location()):
    triples = load_triples(location.triples)
    triples = filter_triples(triples)
    network = rdf_to_networkx(triples)
    network = adjust_weights(network)
    save_network(network, location.network)


if __name__ == "__main__":
    process_graph()
