include ../config.mk

# Output paths
# dataset_dir = $(root_dir)/dataset

# $(dataset_dir):
# 	mkdir -p $@

terminal: terminal.py
	$(spark_submit) terminal.py
.PHONY: terminal
