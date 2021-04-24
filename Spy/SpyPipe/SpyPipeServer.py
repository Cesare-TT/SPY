
import time
from concurrent      import futures
from multiprocessing import Queue,Process
from threading       import Event

import grpc
from . import SpyPipeGRPC_pb2      as proto_pb2
from . import SpyPipeGRPC_pb2_grpc as proto_pb2_grpc


class RemoteStorage(proto_pb2_grpc.SpyPipeGRPCServicer):

    def __init__(self,stop_event):
        self.stop_event = stop_event

    def SendData(self,request_iterator,context):
        req_list = []
        while 1:
            req = next(request_iterator)
            print(req)
            req_list.append(req)
            if req.control =="end":
                #time.sleep(5)
                self.stop_event.set()
                #print(req_list)
                #self.main_Server.stop_process()
                #self.main_Server.stop_event.set()
                return proto_pb2.ReceivedCount(control=req.control)

class SpyPipeServer(Process):

    def __init__(self,name):
        super().__init__()
        self.name = name

    def run(self):
        stop_event = Event()
        #queue_rpc2storage = Queue(100)
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        proto_pb2_grpc.add_SpyPipeGRPCServicer_to_server(RemoteStorage(stop_event), self.grpc_server)
        self.grpc_server.add_insecure_port('unix:SpyPipe_%s.sock' % self.name)
        #self.grpc_server.add_insecure_port('http::./test')

        self.grpc_server.start()
        stop_event.wait()
        self.stop()

    #def stop_process(self):
    #    print('run stop process')

    def stop(self):
        self.grpc_server.stop(grace=None)

if __name__ == '__main__':
    # server = serve()
    # server.stop(grace=None)
    print('python server started.')
    import sys
    server = SpyPipeServer('test')
    server.start()
    #server.stop()



# def serve():
    # queue_rpc2storage = Queue(100)

    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    # proto_pb2_grpc.add_RemoteStorageServicer_to_server(RemoteStorage(queue_rpc2storage), server)
    # server.add_insecure_port('[::]:50051')
    # server.start()
    # # try:
    # #     while True:
    # #         time.sleep(60*60*24) # one day in seconds
    # # except KeyboardInterrupt:
    # #     server.stop(0)
    # return server

