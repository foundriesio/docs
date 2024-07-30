# You can set these variables from the command line.
OUTDIR        ?= build
SPHINXBUILD   ?= sphinx-build
SPHINXOPTS    ?=

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# ' (this line works around an Emacs makefile-mode bug)

ALLSPHINXOPTS   = -W -d $(OUTDIR)/doctrees $(SPHINXOPTS) source
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(SPHINXOPTS) source

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  lint-all   to lint markup files under source"
	@echo "  lint-diff  to lint files changed since last commit"

.PHONY: clean
clean:
	rm -rf $(OUTDIR)/*

.PHONY: html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(OUTDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(OUTDIR)/html."

.PHONY: simplepdf
simplepdf:
	$(SPHINXBUILD) -M simplepdf source $(OUTDIR)/pdf
	@echo
	@echo "Build finished. The PDF is in $(OUTDIR)/pdf."

.PHONY: dirhtml
dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(OUTDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(OUTDIR)/dirhtml."

.PHONY: singlehtml
singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(OUTDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(OUTDIR)/singlehtml."

.PHONY: linkcheck
linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(OUTDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(OUTDIR)/linkcheck/output.txt."

.PHONY: lint-all
lint-all:
	vale sync && vale source

.PHONY: lint-diff
lint-diff:
	vale sync && vale $(shell git diff --name-only | tr '\n' ' ')
