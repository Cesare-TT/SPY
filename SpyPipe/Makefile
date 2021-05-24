HOST_SYSTEM = $(shell uname | cut -f 1 -d_)
SYSTEM ?= $(HOST_SYSTEM)
CXX = g++
CPPFLAGS += `pkg-config --cflags protobuf grpc`
CXXFLAGS += -std=c++11
CXXFLAGS += -fPIC


ifeq ($(SYSTEM),Darwin)
LDFLAGS += -L/usr/local/lib `pkg-config --libs protobuf grpc++`\
					 -pthread\
           -lgrpc++_reflection\
           -ldl
else
LDFLAGS += -L/usr/local/lib `pkg-config --libs protobuf grpc++`\
           -pthread\
           -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed\
           -ldl
endif
PROTOC = protoc
GRPC_CPP_PLUGIN = grpc_cpp_plugin
GRPC_CPP_PLUGIN_PATH ?= `which $(GRPC_CPP_PLUGIN)`
GRPC_PYTHON_PLUGIN = grpc_python_plugin
GRPC_PYTHON_PLUGIN_PATH ?= `which $(GRPC_PYTHON_PLUGIN)`
#python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. remote_storage.proto
#python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. remote_storage.proto

PROTOS_PATH = .

#LDFLAGS += -L/usr/local/lib `pkg-config --libs protobuf grpc++`\
					 #-pthread\
           #-lgrpc++_reflection\
           #-ldl



vpath %.proto $(PROTOS_PATH)

all:SpyPipeClient systemverilog

c_only:SpyPipeClient

systemverilog: top.sv
	vcs -full64 -sverilog SpyPipe.sv top.sv

SpyPipeClient: SpyPipeGRPC.pb.o SpyPipeGRPC.grpc.pb.o SpyPipeClient.o
	$(CXX) $^ $(LDFLAGS) -o $@.so -shared
	$(CXX) $^ $(LDFLAGS) -o $@

%.grpc.pb.cc: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) $<

%.pb.cc: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --cpp_out=. --python_out=. $< 
#	$(PROTOC) -I $(PROTOS_PATH) --cpp_out=. --python_out. $< 

sim:
	./simv -sv_root . -sv_lib SpyPipeClient
clean:
	rm -f *.o *.pb.cc *.pb.h client

release:
	if [ -d ../pipe_py ]; then rm -r ../pipe_py; fi
	mkdir ../pipe_py
	cp SpyPipeServer.py 		../pipe_py/SpyPipeServer.py
	cp SpyPipeGRPC_pb2.py		../pipe_py/SpyPipeGRPC_pb2.py
	cp SpyPipeGRPC_pb2_grpc.py	../pipe_py/SpyPipeGRPC_pb2_grpc.py
	if [ -d ../pipe_so ]; then rm -r ../pipe_so; fi
	mkdir ../pipe_so
	cp SpyPipeClient.so			../pipe_so/SpyPipeClient.so


dbg_gen_code:
	$(PROTOC) -I $(PROTOS_PATH) --cpp_out=. --python_out=. SpyPipeGRPC.proto
	$(PROTOC) -I $(PROTOS_PATH) --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) SpyPipeGRPC.proto
	$(PROTOC) -I $(PROTOS_PATH) --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_PYTHON_PLUGIN_PATH) --plugin=protoc-gen-grpc=$(GRPC_PYTHON_PLUGIN_PATH) SpyPipeGRPC.proto

update_python:
	