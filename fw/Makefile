
.PHONY: all clean

all: build/Makefile
	@$(MAKE) -C build/

clean:
	@rm -rf build/

build/Makefile:
	@echo Running CMake...
	@mkdir -p build
	@cd build && cmake ..
