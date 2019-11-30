# Pipeline common transforms

# Paths
common_dir := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

# Create database
create_db_sql = $(common_dir)/create_db.sql
$(warehouse_dir)/%/.db_sentinel: $(create_db_sql)
	$(spark_sql) \
		--define dbname="$(notdir $(abspath $(dir $@)))" \
		--define location="$(abspath $(dir $@))" \
		-f $<
	touch $@

# Utility functions
f_dbpath = $(warehouse_dir)/$1
f_dbtarget = $(warehouse_dir)/$1/.db_sentinel
