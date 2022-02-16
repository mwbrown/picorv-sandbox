
all:
	$(MAKE) -C ../fw
	PYTHONPATH=.. python3 -m picosb.cli --output ../rtl/am_gen.v
	$(MAKE) -f ./Makefile.sim
