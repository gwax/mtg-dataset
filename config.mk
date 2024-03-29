# Common configuration options

# Common paths
root_dir := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
build_dir = $(root_dir)/build
warehouse_dir = $(build_dir)/warehouse
spark_conf_dir = $(root_dir)/spark_conf

# Spark configuration
spark_app_name = mtg-dataset

spark_env = SPARK_CONF_DIR=$(spark_conf_dir)
spark_params = \
	--name $(spark_app_name) \
	--driver-memory 4G \
	--conf "spark.sql.warehouse.dir=$(warehouse_dir)" \
	--conf "spark.driver.extraJavaOptions=-Dderby.system.home=$(warehouse_dir)"

spark_sql = $(spark_env) spark-sql $(spark_params)
pyspark = $(spark_env) pyspark $(spark_params)
spark_submit = $(spark_env) spark-submit $(spark_params)

# CLI targets
spark_sql_cli:
	$(spark_sql)
.PHONY: spark_sql_cli

pyspark_cli:
	$(pyspark)
.PHONY: pyspark_cli
