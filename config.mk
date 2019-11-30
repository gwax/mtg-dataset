# Common configuration options

# Common paths
root_dir := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
build_dir = $(root_dir)/build
warehouse_dir = $(build_dir)/warehouse
spark_conf_dir = $(root_dir)/spark_conf

# Spark configuration
packages = io.delta:delta-core_2.11:0.4.0

spark_env = SPARK_CONF_DIR=$(spark_conf_dir)
spark_params = \
    --packages $(packages) \
	--conf "spark.sql.warehouse.dir=$(warehouse_dir)" \
	--conf "spark.driver.extraJavaOptions=-Dderby.system.home=$(warehouse_dir)"

spark_sql = $(spark_env) spark-sql $(spark_params)
spark_submit = $(spark_env) spark-submit $(spark_params)
