include ../config.mk

# Options
.SECONDEXPANSION:

# Input paths
input_tables = $(warehouse_dir)/stg_mtg
sets_table_dir = $(warehouse_dir)/stg_mtg/sets
cards_table_dir = $(warehouse_dir)/stg_mtg/cards

# Output paths
canonical_data_dir = $(root_dir)/canonical_json
sunk_data_dir = $(build_dir)/sunk_data

$(sunk_data_dir):
	mkdir -p $@

# Sinks
sinks := $(patsubst sink_%.py,%,$(wildcard sink_*.py))
$(sunk_data_dir)/%: sink_%.py $(input_tables) | $(sunk_data_dir)
	-rm -r $@
	$(spark_submit) $< $@

# Canonical json
canonical_sink = json_split
$(sunk_data_dir)/canonical.txt: FORCE | $(sunk_data_dir)
	if [ "$$(cat $@ 2>/dev/null)" != "$(canonical_sink)" ]; then \
		echo "$(canonical_sink)" > $@; \
	fi

$(canonical_data_dir): $(sunk_data_dir)/$(canonical_sink) $(sunk_data_dir)/canonical.txt
	-rm -r $@
	cp -r $< $@

# Readable named targets
$(sinks): $$(sunk_data_dir)/$$@
.PHONY: $(sinks)

canonical_data: $(canonical_data_dir)
.PHONY: canonical_data

clean:
	-rm -r $(sunk_data_dir)
.PHONY: clean

all: $(sinks) canonical_data
.PHONY: all
.DEFAULT_GOAL = all

# Meta targets
FORCE:
.PHONY: FORCE
