"""Python script to process the data"""

from functools import reduce
from typing import Iterator

import yaml
from gimie.project import Project
from prefect import flow, task  # type: ignore
from rdflib import Graph

from config import Location


@task
def read_sources(src_cfg: str) -> Iterator[str]:
    with open(src_cfg, "r") as inp:
        data = yaml.safe_load(inp)
    sources = []
    for prov in data.keys():
        for org, repos in data[prov].items():
            for repo in repos:
                sources.append(f"{prov}/{org}/{repo}")
    return sources


@task
def generate_triples(url: str) -> Graph:
    return Project(url, sources="github").to_graph()


@task
def combine_triples(graph1: Graph, graph2: Graph):
    return graph1 | graph2


@task
def save_triples(triples: Graph, out: str):
    triples.serialize(out, format="ttl")  # type: ignore


@flow
def make_triples(location: Location = Location()):
    sources = read_sources(location.sources)
    graphs = map(generate_triples, sources)
    merged = reduce(combine_triples, graphs)
    save_triples(merged, location.triples)


if __name__ == "__main__":
    make_triples()
