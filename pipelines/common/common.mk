# Pipeline common transforms

# Paths
common_dir := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
schema_dir = $(build_dir)/schemas

# Database table management
create_db_sql = $(common_dir)/create_db.sql
drop_db_sql = $(common_dir)/drop_db.sql
# Database location
dbpath = $(warehouse_dir)/$(1)
# Template for create and drop functions
define MANAGEDB_template
dbpath_$(1) = $$(call dbpath,$(1))
$$(dbpath_$(1)): $$(create_db_sql)
	$$(spark_sql) \
		--define dbname="$$(basename $$(notdir $$@))" \
		--define location="$$@" \
		-f $$<

create_$(1): $$(dbpath_$(1))
.PHONY: create_$(1)

drop_$(1): $$(drop_db_sql)
	$$(spark_sql) \
		--define dbname="$(1)" \
		-f $$<
.PHONY: drop_$(1)
endef

# Table as select helper program
table_as_select = $(spark_submit) $(common_dir)/table_as_select.py
