BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCS_DIR=./docs/

init:
	pip install --upgrade -r requirements.txt

render: render-pages copy-img
	
render-pages::
	mkdir -p docs
	python3 render.py

	
clean::
	rm -rf $(DOCS_DIR)
	mkdir -p $(DOCS_DIR)
	
commit-docs::
	git add docs
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt docs $(shell date +%F)"; git push origin $(BRANCH))

copy-img::
	mkdir -p docs/images
	rsync -r src/images docs/
