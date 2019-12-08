include ../config.mk

# Options
.SECONDEXPANSION:

# Input paths
canonical_json = $(root_dir)/canonical_json

# Output paths
re_build_dir = $(build_dir)/recycle
jsonl_dir = $(re_build_dir)/jsonl

$(re_build_dir) $(jsonl_dir):
	mkdir -p $@

# Hash input data every time and only run downstream if changed to avoid downstream cycles
FORCE:
$(re_build_dir)/%.md5: $(canonical_json)/% FORCE | $(re_build_dir)
	find $< -type f -print0 | \
		sort -z | \
		xargs -0 md5sum | \
		md5sum \
		> $@.new
	if [ "$$(cat $@ 2>/dev/null)" != "$$(cat $@.new)" ]; then \
		cp $@.new $@; \
	fi
	rm $@.new

# Recycle json to jsonlines
$(jsonl_dir)/%.jsonlines: $(re_build_dir)/%.md5 | $(jsonl_dir)
	find $(patsubst $(jsonl_dir)/%.jsonlines,$(canonical_json)/%,$@) \
		-name '*.json' -type f -print0 | \
		sort -z | \
		xargs -0 jq '.' -c \
		> $@

# Readable named targets
sets cards: $(re_build_dir)/$$@.md5 $(jsonl_dir)/$$@.jsonlines
.PHONY: sets cards

clean:
	-rm -r $(re_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: sets cards
.PHONY: all
.DEFAULT_GOAL = all
