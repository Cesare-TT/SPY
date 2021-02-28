

all: compile run

compile:
	vcs -full64 -sverilog -kdb -l log/compile.log tb.sv

run:
	./simv -l log/simv.log