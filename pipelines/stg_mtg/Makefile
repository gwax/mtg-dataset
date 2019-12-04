include ../../config.mk
include ../common/common.mk

# Options
.SECONDEXPANSION:

# Parameters
dbname := $(notdir $(CURDIR))

# Database target
$(eval $(call MANAGEDB_template,$(dbname)))
db = $(call dbpath,$(dbname))

# Create transform tables
transforms := $(patsubst %.sql,%,$(wildcard *.sql))
$(db)/%: %.sql | $(db)
	$(spark_sql) \
		--define dbname="$(dbname)" \
		--define tablename="$(notdir $@)" \
		-f $<

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
