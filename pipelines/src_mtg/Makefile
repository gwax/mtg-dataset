include ../../config.mk
include ../common/common.mk

# Options
.SECONDEXPANSION:

# Parameters
dbname := $(notdir $(CURDIR))

# Database management
$(eval $(call MANAGEDB_template,$(dbname)))
db = $(call dbpath,$(dbname))

# Create raw source tables
raw_table_sql = $(CURDIR)/raw_table.sql
# Raw table source data
raw_recycle_sets_JSONL = $(build_dir)/recycle/jsonl/sets.jsonlines
raw_recycle_cards_JSONL = $(build_dir)/recycle/jsonl/cards.jsonlines
raw_scryfall_sets_JSONL = $(build_dir)/scryfall/jsonl/sets.jsonlines
raw_scryfall_cards_JSONL = $(build_dir)/scryfall/jsonl/cards.jsonlines
raw_librarities_cards_JSONL = $(build_dir)/librarities/jsonl/cards.jsonlines
# Raw table target
$(db)/raw_%: $(raw_table_sql) $$($$(notdir $$@)_JSONL) | $(db)
	$(spark_sql) \
		--define dbname="$(dbname)" \
		--define tablename="$(notdir $@)" \
		--define input_file="$(word 2, $^)" \
		-f $<

# Readable named targets
raw_tables = \
	raw_recycle_sets \
	raw_recycle_cards \
	raw_scryfall_sets \
	raw_scryfall_cards \
	raw_librarities_cards
$(raw_tables): $$(db)/$$@
.PHONY: $(raw_tables)

clean: drop_$(dbname)
	-rm -r $(db)
	-rmdir $(warehouse_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: create_$(dbname) $(raw_tables)
.PHONY: all
.DEFAULT_GOAL = all
