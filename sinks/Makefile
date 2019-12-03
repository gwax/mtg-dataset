include ../config.mk

# Output paths
$(dataset_dir):
	mkdir -p $@

$(dataset_dir)/json: jsonfiles.py | $(dataset_dir)
	-rm -r $@
	$(spark_submit) $< $@
.PHONY: $(dataset_dir)/json

# Readable named targets
jsonfiles: $(dataset_dir)/json
.PHONY: jsonfiles

clean:
	-rm -r $(dataset_dir)
.PHONY: clean

all: jsonfiles
.PHONY: all
.DEFAULT_GOAL = all
