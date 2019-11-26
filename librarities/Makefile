ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/build
endif

# Options
.DELETE_ON_ERROR: # TODO: Add stop/resume support

# Output paths
librarities_build_dir = $(build_dir)/librarities
librarities_jsonl_dir = $(librarities_build_dir)/jsonl

# Named targets
all: cards
.PHONY: all
.DEFAULT_GOAL = all

clean:
	-rm -r $(librarities_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

cards: $(librarities_jsonl_dir)/cards.jsonlines
.PHONY: cards

# Create output paths
$(librarities_jsonl_dir):
	mkdir -p $@

# Fetch magic librarities data from the web
$(librarities_jsonl_dir)/cards.jsonlines: scraper.py | $(librarities_jsonl_dir)
	scrapy runspider -o $@ scraper.py
