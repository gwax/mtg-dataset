include ../config.mk

# Input paths
sets_table_dir = $(warehouse_dir)/stg_mtg/sets
cards_table_dir = $(warehouse_dir)/stg_mtg/cards

# Output paths
canonical_json_dir = $(root_dir)/canonical_json
sunk_data_dir = $(root_dir)/sunk_data

# Canonical json
$(canonical_json_dir): json_split.py $(sets_table_dir) $(cards_table_dir)
	-rm -r $@
	$(spark_submit) $< $@

# Sunk data
sets_nested_dir = $(sunk_data_dir)/json_sets
$(sets_nested_dir): json_nested.py $(sets_table_dir) $(cards_table_dir)
	-rm -r $@
	$(spark_submit) $< $@

# Readable named targets
canonical_json: $(canonical_json_dir)
.PHONY: canonical_json

json_nested: $(sets_nested_dir)
.PHONY: json_nested

clean:
	-rm -r $(sunk_data_dir)
.PHONY: clean

all: canonical_json json_nested
.PHONY: all
.DEFAULT_GOAL = all
