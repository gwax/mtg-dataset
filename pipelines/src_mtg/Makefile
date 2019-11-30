include ../../config.mk
include ../common/common.mk

# Options
.SECONDEXPANSION:

# Parameters
dbname = $(notdir $(CURDIR))

# Create database
dbpath = $(call f_dbpath,$(dbname))
dbtarget = $(call f_dbtarget,$(dbname))

# Create raw source tables
raw_table_sql = $(CURDIR)/raw_table.sql
# Raw table source data
raw_scryfall_sets_JSONL = $(build_dir)/scryfall/jsonl/sets.jsonlines
raw_scryfall_cards_JSONL = $(build_dir)/scryfall/jsonl/cards.jsonlines
raw_librarities_cards_JSONL = $(build_dir)/librarities/jsonl/cards.jsonlines
# Raw table target
$(dbpath)/raw_%: $(raw_table_sql) $(dbtarget) $$($$(notdir $$@)_JSONL)
	$(spark_sql) \
		--define dbname="$(dbname)" \
		--define tablename="$(notdir $@)" \
		--define input_file="$(word 3, $^)" \
		-f $<

# Readable named targets
create_db: $(dbtarget)
.PHONY: create_db

raw_tables = \
	raw_scryfall_sets \
	raw_scryfall_cards \
	raw_librarities_cards
$(raw_tables): $$(dbpath)/$$@
.PHONY: $(raw_tables)

clean:
	-rm -r $(db_target)
	-rmdir $(warehouse_dir)
	-rmdir $(build_dir)

all: create_db $(raw_tables)
.PHONY: all
.DEFAULT_GOAL = all
