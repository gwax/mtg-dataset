ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/build
endif

subtargets = scryfall librarities

all: scryfall librarities
.PHONY: all
.DEFAULT_GOAL = all

clean:
	-rm -r $(build_dir)
.PHONY: clean

# Sub-make targets
$(subtargets):
	$(MAKE) -C $@
.PHONY: $(subtargets)
