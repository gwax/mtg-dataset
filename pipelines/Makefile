include ../config.mk

# Sub-make projects
subtargets = \
	src_mtg

# Dependencies
# ...

# Targets
$(subtargets):
	$(MAKE) -C $@
.PHONY: $(subtargets)

# Readable named targets
clean:
	-rm -r $(warehouse_dir)
	-rmdir $(build_dir
.PHONY: clean

all: $(subtargets)
.PHONY: all
.DEFAULT_GOAL = all
