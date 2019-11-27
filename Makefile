ifeq (0, $(MAKELEVEL))
export build_dir := $(CURDIR)/build
endif

get_scryfall    := scryfall
get_librarities := librarities
run_transforms  := transforms
subtargets      := $(get_scryfall) $(get_librarities) $(run_transforms)

# Sub-make targets
$(subtargets):
	$(MAKE) -C $@
.PHONY: $(subtargets)

$(run_transforms): $(get_scryfall) $(get_librarities)

# Readable named targets
clean:
	-rm -r $(build_dir)
.PHONY: clean


all: $(subtargets)
.PHONY: all
.DEFAULT_GOAL = all
