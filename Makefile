# Output directory configuration
build_dir = build
json_dir = $(build_dir)/json
jsonl_dir = $(build_dir)/jsonl

sf_json = $(json_dir)/scryfall
sf_jsonl = $(jsonl_dir)/scryfall

lr_jsonl = $(jsonl_dir)/librarities

# Scryfall retrieval configuration
sf_cards_type = default_cards

.PHONY: all
all: scryfall librarities

.PHONY: clean
clean:
	-rm -r $(build_dir)

# Magic md5 target that updates only on input change
%.md5: %
	@$(if $(filter-out $(shell cat $@ 2>/dev/null),$(shell md5sum $*)),md5sum $* > $@)

# Fetch scryfall json data from the web
$(sf_json):
	mkdir -p $@

# We always fetch the bulk data description and then we depend on the md5
# to only fetch if remote has changes
.PHONY: $(sf_json)/bulk-data.json
$(sf_json)/bulk-data.json: | $(sf_json)
	curl https://api.scryfall.com/bulk-data > $@

$(sf_json)/sets.json: $(sf_json)/bulk-data.json.md5
	curl https://api.scryfall.com/sets > $@

$(sf_json)/cards.json: $(sf_json)/bulk-data.json.md5
	curl $(shell jq '.data[] | select(.type == "$(sf_cards_type)") | .permalink_uri' $(sf_json)/bulk-data.json) > $@

# Convert scryfall json data to jsonlines
$(sf_jsonl):
	mkdir -p $@

$(sf_jsonl)/sets.jsonlines: $(sf_json)/sets.json | $(sf_jsonl)
	jq '.data[]' -c $(sf_json)/sets.json > $@

$(sf_jsonl)/cards.jsonlines: $(sf_json)/cards.json | $(sf_jsonl)
	jq '.[]' -c $(sf_json)/cards.json > $@

.PHONY: scryfall
scryfall: $(sf_jsonl)/sets.jsonlines $(sf_jsonl)/cards.jsonlines

# Fetch magic librarities data from the web
$(lr_jsonl):
	mkdir -p $@

$(lr_jsonl)/cards.jsonlines: | $(lr_jsonl)
	scrapy runspider -o $@ scrapers/librarities.py

.PHONY: librarities
librarities: $(lr_jsonl)/cards.jsonlines
