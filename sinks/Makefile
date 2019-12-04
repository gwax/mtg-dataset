include ../config.mk

# Output paths
$(dataset_dir):
	mkdir -p $@

canonical_json_dir = $(dataset_dir)/canonical_json
$(canonical_json_dir): json_split.py | $(dataset_dir)
	-rm -r $@
	$(spark_submit) $< $@
.PHONY: $(canonical_json_dir)

# Readable named targets
canonical_json: $(canonical_json_dir)
.PHONY: canonical_json

clean:
	-rm -r $(dataset_dir)
.PHONY: clean

all: canonical_json
.PHONY: all
.DEFAULT_GOAL = all
