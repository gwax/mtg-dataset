# Inherit parent output, if called recursively
ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/../build
endif

# Options
.SECONDEXPANSION:

# Output paths
warehouse_dir = $(build_dir)/warehouse

# Spark configuration
spark_conf_dir = $(CURDIR)/../spark_conf
spark_env = SPARK_CONF_DIR=$(spark_conf_dir)
spark_params = \
	--packages io.delta:delta-core_2.11:0.4.0 \
	--conf "spark.sql.warehouse.dir=$(warehouse_dir)" \
	--conf "spark.driver.extraJavaOptions=-Dderby.system.home=$(warehouse_dir)"
spark_sql_cmd = $(spark_env) spark-sql $(spark_params)

# Create database
create_db_sql = create_db.sql
mtgdata_db = $(warehouse_dir)/mtgdata
$(mtgdata_db): $(create_db_sql)
	$(spark_sql_cmd) $(spark_params) \
		--define name="$(notdir $@)" \
		--define location="$@" \
		-f $<

# Create raw tables
raw_table_sql = raw_table.sql
raw_scryfall_sets_JSONL = $(build_dir)/scryfall/jsonl/sets.jsonlines
raw_scryfall_cards_JSONL = $(build_dir)/scryfall/jsonl/cards.jsonlines
raw_librarities_cards_JSONL = $(build_dir)/librarities/jsonl/cards.jsonlines
$(mtgdata_db)/raw_%: $(raw_table_sql) $(mtgdata_db) $$($$(notdir $$@)_JSONL)
	$(spark_sql_cmd) $(spark_params) \
		--define dbname="$(notdir $(word 2, $^))" \
		--define tablename="$(notdir $@)" \
		--define input_file="$(word 3, $^)" \
		-f $<

# Readable named targets
mtgdata_db: $(mtgdata_db)
.PHONY: mtgdata_db

raw_tables = raw_scryfall_sets raw_scryfall_cards raw_librarities_cards
$(raw_tables): $$(mtgdata_db)/$$@
.PHONY: $(raw_tables)

clean:
	-rm -r $(warehouse_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: $(raw_tables)
.PHONY: all
.DEFAULT_GOAL = all
