
import time
import sys
from concurrent      import futures
from multiprocessing import Queue,Process
from threading       import Event

import grpc
import SpyPipeGRPC_pb2      as proto_pb2
import SpyPipeGRPC_pb2_grpc as proto_pb2_grpc


class ServerCore(object):

    def process(self,req):
        pass


class RemoteStorage(proto_pb2_grpc.SpyPipeGRPCServicer):

    def __init__(self,stop_event,server_core,debug=False):
        self.stop_event = stop_event
        self.debug = debug
        self.server_core = server_core

    def SendData(self,request_iterator,context):
        for req in request_iterator:
            if req.control =='end':
                print("Server::get end.")
                self.stop_event.set()
                yield proto_pb2.Data(payload=req.payload,control=req.control)
                return
            else:
                res = self.server_core.process(req)
                if res != None:
                    yield res

    def dbg_print(self,string):
        if self.debug != False:
            print(string)

class SpyPipeServer(Process):

    def __init__(self,name,debug=False):
        super().__init__()
        self.name  = name
        self.debug = debug

    def run(self):
        stop_event = Event()
        sock_name  = 'unix:SpyPipe_%s.sock' % self.name

        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        proto_pb2_grpc.add_SpyPipeGRPCServicer_to_server(RemoteStorage(stop_event,self.debug), self.grpc_server)
        self.grpc_server.add_insecure_port(sock_name)
        
        self.dbg_print('Server::start with sock %s' % sock_name)
        self.grpc_server.start()

        self.dbg_print('Server::wait stop event.')
        stop_event.wait()
        self.grpc_server.stop(grace=None)

    def dbg_print(self,string):
        if self.debug != False:
            print(string)



if __name__ == '__main__':
    name = sys.argv[1]
    core = ServerCore()
    print('SpyPipe::Python server %s started.' % name)
    server = SpyPipeServer(name,core)
    server.start()
    print('SpyPipe::Python server %s end.' % name)