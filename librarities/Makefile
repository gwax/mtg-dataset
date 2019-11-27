# Inherit parent output, if called recursively
ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/../build
endif

# Options
.DELETE_ON_ERROR:

# Output paths
lr_build_dir = $(build_dir)/librarities
jsonl_dir = $(lr_build_dir)/jsonl

$(jsonl_dir):
	mkdir -p $@

# Scrape Magic Librarities
cards_scraper = scraper.py
cards_jsonl = $(jsonl_dir)/cards.jsonlines
$(cards_jsonl): $(cards_scraper) | $(jsonl_dir)
	scrapy runspider -o $@ $<

# Readable named targets
cards: $(cards_jsonl)
.PHONY: cards

clean:
	-rm -r $(lr_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: cards
.PHONY: all
.DEFAULT_GOAL = all
