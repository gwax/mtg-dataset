include ../config.mk

cards_table_dir = $(warehouse_dir)/stg_mtg/cards
sets_table_dir = $(warehouse_dir)/stg_mtg/sets

# Canonical json
canonical_json_dir = $(root_dir)/canonical_json
$(canonical_json_dir): json_split.py $(sets_table_dir) $(cards_table_dir)
	-rm -r $@
	$(spark_submit) $< $@

# Readable named targets
canonical_json: $(canonical_json_dir)
.PHONY: canonical_json

all: canonical_json
.PHONY: all
.DEFAULT_GOAL = all
