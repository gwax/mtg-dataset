include ../config.mk

# Options
.SECONDEXPANSION:

# Input paths
canonical_data = $(root_dir)/canonical_data

# Output paths
re_build_dir = $(build_dir)/recycle
jsonl_dir = $(re_build_dir)/jsonl

$(re_build_dir) $(jsonl_dir):
	mkdir -p $@

# Hash input data every time and only run downstream if changed to avoid downstream cycles
canonical_md5 = $(re_build_dir)/canonical_data.md5
$(canonical_md5): FORCE | $(re_build_dir)
	find $(canonical_data) -type f -print0 | \
		sort -z | \
		xargs -0 md5sum | \
		md5sum \
		> $@.new
	if [ "$$(cat $@ 2>/dev/null)" != "$$(cat $@.new)" ]; then \
		cp $@.new $@; \
	fi
	rm $@.new

# Recycle canonical json to jsonlines
# Queries
cards_jq = '.cards[]'
sets_jq = 'del(.cards)'
# Rules
query_types = cards sets
jsonlines_files := $(foreach type,$(query_types),$(jsonl_dir)/$(type).jsonlines)
$(jsonlines_files): $(canonical_md5) | $(jsonl_dir)
	find $(canonical_data) -name '*.json' -type f -print0 | \
		sort -z | \
		xargs -0 jq $($(patsubst $(jsonl_dir)/%.jsonlines,%,$@)_jq) -c \
		> $@

# Readable named targets
$(query_types): $(jsonl_dir)/$$@.jsonlines
.PHONY: $(query_types)

clean:
	-rm -r $(re_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: $(query_types)
.PHONY: all
.DEFAULT_GOAL = all

# Meta targets
FORCE:
.PHONY: FORCE
