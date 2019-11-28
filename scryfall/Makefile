ifeq (0, $(MAKELEVEL))
export root_dir := $(CURDIR)/..
endif
include $(root_dir)/paths.mk

# Output paths
sf_build_dir = $(build_dir)/scryfall
json_dir = $(sf_build_dir)/json
jsonl_dir = $(sf_build_dir)/jsonl

$(json_dir) $(jsonl_dir):
	mkdir -p $@

# Fetch Scryfall JSON
sets_json = $(json_dir)/sets.json
$(sets_json): | $(json_dir)
	curl https://api.scryfall.com/sets > $@

bulk_json = $(json_dir)/bulk-data.json
$(bulk_json): | $(json_dir)
	curl https://api.scryfall.com/bulk-data > $@

bulk_cards_type = default_cards
cards_url_jq = '.data[] | select(.type == "$(bulk_cards_type)") | .permalink_uri'
cards_json = $(json_dir)/cards.json
$(cards_json): $(bulk_json)
	curl $(shell jq $(cards_url_jq) $(bulk_json)) > $@

# Convert JSON to JSON Lines
sets_jsonl = $(jsonl_dir)/sets.jsonlines
$(sets_jsonl): $(sets_json) | $(jsonl_dir)
	jq '.data[]' -c $< > $@

cards_jsonl = $(jsonl_dir)/cards.jsonlines
$(cards_jsonl): $(cards_json) | $(jsonl_dir)
	jq '.[]' -c $< > $@

# Readable named targets
sets: $(sets_jsonl)
.PHONY: sets

cards: $(cards_jsonl)
.PHONY: cards

clean:
	-rm -r $(sf_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: sets cards
.PHONY: all
.DEFAULT_GOAL = all
