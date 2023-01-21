initialize_git:
	@echo "Initializing git..."
	git init 
	
install: 
	@echo "Installing..."
	poetry install
	poetry run pre-commit install

activate:
	@echo "Activating virtual environment"
	poetry shell

download_data:
	@echo "Downloading data..."
	wget https://gist.githubusercontent.com/khuyentran1401/a1abde0a7d27d31c7dd08f34a2c29d8f/raw/da2b0f2c9743e102b9dfa6cd75e94708d01640c9/Iris.csv -O data/raw/iris.csv

setup: initialize_git install download_data

test:
	pytest

docs_view:
	@echo View API documentation... 
	PYTHONPATH=src pdoc src --http localhost:8080

docs_save:
	@echo Save documentation to docs... 
	PYTHONPATH=src pdoc src -o docs

data/processed/graph.ttl: data/raw/sources.yml src/extract.py
	@echo "Getting triples..."
	python src/extract.py

data/processed/network.edgelist: data/processed/graph.ttl src/process.py
	@echo "Processing graph..."
	python src/process.py

data/final/bundled_network.png: data/processed/network.edgelist src/viz.py
	@echo "Visualizing graph..."
	python src/viz.py

pipeline: data/processed/graph.ttl data/processed/network.edgelist data/final/bundled_network.png

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
