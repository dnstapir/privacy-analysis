SOURCES=becoming-uniquely-identifiable-in-a-hyperloglog-sketch.tex
PDF_TARGETS=$(SOURCES:.tex=.pdf)

LATEXMK=latexmk
LATEXMK_OPTS=-g -bibtex -pdf -pdflatex="pdflatex -interaction=nonstopmode"

DOCKER=docker
DOCKER_CMD=run --rm -w /data/ --env LATEXMK_OPTS_EXTRA=$(LATEXMK_OPTS_EXTRA)
DOCKER_MOUNT=-v`pwd`:/data
DOCKER_IMG=texlive/texlive

all: render

pdf: $(PDF_TARGETS)

%.pdf: %.tex $(wildcard sections/*) $(wildcard bibtex-references/*) $(wildcard figures/*)
	$(LATEXMK) $(LATEXMK_OPTS_EXTRA) $(LATEXMK_OPTS) $<

clean:
	-$(DOCKER) $(DOCKER_CMD) -u $$(id -u):$$(id -g) $(DOCKER_MOUNT) $(DOCKER_IMG) $(LATEXMK) -bibtex -C becoming-uniquely-identifiable-in-a-hyperloglog-sketch

render:
	$(DOCKER) $(DOCKER_CMD) -u $$(id -u):$$(id -g) $(DOCKER_MOUNT) $(DOCKER_IMG) make pdf
