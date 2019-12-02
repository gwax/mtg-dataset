include config.mk

# Sub-make projects
subtargets = \
	scryfall \
	librarities \
	pipelines \
	sinks

# Dependencies
pipelines: scryfall librarities
sinks: pipelines

# Targets
$(subtargets):
	$(MAKE) -C $@
.PHONY: $(subtargets)

# Readable named targets
clean:
	-rm -r $(build_dir)
.PHONY: clean

all: $(subtargets)
.PHONY: all
.DEFAULT_GOAL = all
