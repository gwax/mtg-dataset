# Inherit parent output, if called recursively
ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/build
endif

# Output paths
scryfall_build_dir = $(build_dir)/scryfall
scryfall_json_dir = $(scryfall_build_dir)/json
scryfall_jsonl_dir = $(scryfall_build_dir)/jsonl

# Named targets
all: sets cards
.PHONY: all
.DEFAULT_GOAL = all

clean:
	-rm -r $(scryfall_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

sets: $(scryfall_jsonl_dir)/sets.jsonlines
.PHONY: sets

cards: $(scryfall_jsonl_dir)/cards.jsonlines
.PHONY: cards

# Create output paths
$(scryfall_json_dir) $(scryfall_jsonl_dir):
	mkdir -p $@

# Fetch scryfall json data from the web
scryfall_cards_type = default_cards

$(scryfall_json_dir)/sets.json: | $(scryfall_json_dir)
	curl https://api.scryfall.com/sets > $@

$(scryfall_json_dir)/bulk-data.json: | $(scryfall_json_dir)
	curl https://api.scryfall.com/bulk-data > $@

$(scryfall_json_dir)/cards.json: $(scryfall_json_dir)/bulk-data.json
	curl $(shell jq '.data[] | select(.type == "$(scryfall_cards_type)") | .permalink_uri' $(scryfall_json_dir)/bulk-data.json) > $@

# Convert scryfal json data to jsonlines format
$(scryfall_jsonl_dir)/sets.jsonlines: $(scryfall_json_dir)/sets.json | $(scryfall_jsonl_dir)
	jq '.data[]' -c $(scryfall_json_dir)/sets.json > $@

$(scryfall_jsonl_dir)/cards.jsonlines: $(scryfall_json_dir)/cards.json | $(scryfall_jsonl_dir)
	jq '.[]' -c $(scryfall_json_dir)/cards.json > $@
