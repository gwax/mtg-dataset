include ../config.mk

# Input paths
canonical_json = $(root_dir)/canonical_json
sets_json = $(canonical_json)/sets
cards_json = $(canonical_json)/cards

# Output paths
re_build_dir = $(build_dir)/recycle
jsonl_dir = $(re_build_dir)/jsonl

$(jsonl_dir):
	mkdir -p $@

# Recycle json to jsonlines
sets_jsonl = $(jsonl_dir)/sets.jsonlines
$(sets_jsonl): $(sets_json) | $(jsonl_dir)
	find $< -name '*.json' -type f -print0 | \
		sort -z | \
		xargs -0 jq '.' -c \
		> $@

cards_jsonl = $(jsonl_dir)/cards.jsonlines
$(cards_jsonl): $(cards_json) | $(jsonl_dir)
	find $< -name '*.json' -type f -print0 | \
		sort -z | \
		xargs -0 jq '.' -c \
		> $@

# Readable named targets
sets: $(sets_jsonl)
.PHONY: sets

cards: $(cards_jsonl)
.PHONY: cards

clean:
	-rm -r $(re_build_dir)
	-rmdir $(build_dir)
.PHONY: clean

all: sets cards
.PHONY: all
.DEFAULT_GOAL = all
