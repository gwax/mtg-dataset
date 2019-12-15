include ../../config.mk
include ../common/common.mk

# Options
.SECONDEXPANSION:

# Parameters
dbname := $(notdir $(CURDIR))

# Database target
$(eval $(call MANAGEDB_template,$(dbname)))
db = $(call dbpath,$(dbname))

# Output paths
schema_dir = $(build_dir)/schemas

# Create transform tables
transforms := $(patsubst %.sql,%,$(wildcard *.sql))
$(db)/%: %.sql $(warehouse_dir)/src_mtg | $(db)
	$(table_as_select) \
		--db="$(dbname)" \
		--name="$(notdir $@)" \
		--sqlfile="$<"

# Readable named targets
$(transforms): $$(db)/$$@
.PHONY: $(transforms)

clean: drop_$(dbname)
	-rm -r $(db)
	-rmdir $(warehouse_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: create_$(dbname) $(transforms)
.PHONY: all
.DEFAULT_GOAL = all
