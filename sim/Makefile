
all:
	$(MAKE) -C ../fw
	PYTHONPATH=.. python3 -m picosb.cli generate -t v > ../rtl/am_gen.v
	$(MAKE) -f ./Makefile.sim
