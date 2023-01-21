"""
Create an iris flow
"""
from prefect import flow
from prefect_dask.task_runners import DaskTaskRunner  # type: ignore

from config import Location
from run_notebook import run_notebook
from src.extract import make_triples
from src.process import process_graph
from src.viz import save_viz


@flow(task_runner=DaskTaskRunner())
def rdf_flow(
    location: Location = Location(),
):
    make_triples(location)
    process_graph(location)
    run_notebook(location)
    save_viz(location)


if __name__ == "__main__":
    rdf_flow()
