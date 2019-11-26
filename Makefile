ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/build
endif

subtargets = scryfall librarities

.PHONY: all
all: scryfall librarities

.PHONY: clean
clean:
	-rm -r $(build_dir)

# Sub-make targets
$(subtargets):
	$(MAKE) -C $@
.PHONY: $(subtargets)
