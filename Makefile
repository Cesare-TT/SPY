OPT = 

all: compile run

compile:
	vcs -full64 -sverilog -kdb -l compile.log unitest/test_spy.sv +define+BIT_WIDTH=31 +incdir+"./Spy" $(OPT)

run:
	./simv -l simv.log $(OPT) +VERBOSE