
#include <iostream>
#include <memory>
#include <string>
#include <pthread.h>
#include <unistd.h>

#include <grpcpp/grpcpp.h>
//#include "remote_storage.grpc.pb.h"
#include "SpyPipeGRPC.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using grpc::ClientWriter;
using spy_pipe_pkg::Data;
using spy_pipe_pkg::ReceivedCount;
using spy_pipe_pkg::SpyPipeGRPC;



class RemoteStorageClient {

public:
    RemoteStorageClient(std::shared_ptr<Channel> channel)
        :stub_(SpyPipeGRPC::NewStub(channel)) {}

    void SendData(const std::string& message) {
        ClientContext context;
        Data          data;
        ReceivedCount received_count;
        std::unique_ptr<ClientWriter<Data> > writer(stub_->SendData(&context, &received_count));

        data.set_payload(message);
        writer->Write(data);
        writer->WritesDone();
        Status status = writer->Finish();
    }

    void SendEnd(){
        ClientContext context;
        Data          data;
        ReceivedCount received_count;
        std::unique_ptr<ClientWriter<Data> > writer(stub_->SendData(&context, &received_count));

        data.set_control("end");
        writer->Write(data);
        writer->WritesDone();
        Status status = writer->Finish();
        if (status.ok()) {
            std::cout << "Response:"<< received_count.control() << "   " << std::endl;
        }
        else {
            std::cout << "something wrong" << std::endl;
            std::cout << "Response:"<< received_count.control() << "   " << std::endl;
        }


    }

private:
    std::unique_ptr<SpyPipeGRPC::Stub> stub_;
};


void* call_python_server(void *args){
    //char* name = (char*)args;
    char command[100];
    system(command);
    //sprintf(command,"python server.py %s",(char*)args);
}

class RemoteStorageSolution{

public:
    RemoteStorageSolution(const char* command,const char* name_in){
        char sock_name[100];
        char full_command[200];
        sprintf(sock_name,"unix:SpyPipe_%s.sock",name_in);
        sprintf(full_command,"%s %s",command,sock_name);
        
        this->name = sock_name;

        // new server
        pthread_create(&server_tid, NULL, call_python_server,(void*)full_command);
        // new client
        sleep(1);
        this->client = new RemoteStorageClient(grpc::CreateChannel(sock_name,grpc::InsecureChannelCredentials()));
    }
    //    :client(grpc::CreateChannel(sock_name,grpc::InsecureChannelCredentials())){}
    //RemoteStorageClient(std::shared_ptr<Channel> channel)
    //    :stub_(SpyPipeGRPC::NewStub(channel)) {}
    //void start(const char* name){
    //
    //}

    void send_data(const char* message){
        this->client->SendData(message);
    }

    void finish(){
        this->client->SendEnd();
        pthread_join(server_tid, &server_thread_status);
    }

private:
    RemoteStorageClient* client;
    const char* name;
    pthread_t server_tid;
    void *server_thread_status;

};

extern "C" void*    spy_pipe_start(const char* command,const char* name);
extern "C" void     spy_pipe_send_data(RemoteStorageSolution* ptr,const char* message);
extern "C" void     spy_pipe_stop(RemoteStorageSolution* ptr);
extern "C" void     spy_pipe_debug_print(const char* message);

void spy_pipe_debug_print(const char* message) {
    std::cout << "spy_pipe_debug_print:"<< message << std::endl;
}

void* spy_pipe_start(const char* command,const char* name) {
    void *ptr = (void*)new char[sizeof(RemoteStorageSolution)];
    RemoteStorageSolution *remote_storage = new(ptr) RemoteStorageSolution(command,name);
    std::cout << "-------------- Start --------------" << std::endl;
    return remote_storage;
}

void spy_pipe_send_data(RemoteStorageSolution* ptr,const char* message) {
    ptr->send_data(message);
}

void spy_pipe_stop(RemoteStorageSolution* ptr) {
    ptr->finish();
    free(ptr);
    std::cout << "-------------- release mem --------------" << std::endl;
}
 











//-------------------------------------------------golden-----------------------------------------------------------------------------------
// void* rs_start(const char* name) {
//     //static int count = 0;
//     char sock_name[100];
//     sprintf(sock_name,"unix:rmsock_%s",name);
//     void *ptr = (void*)new char[sizeof(RemoteStorageClient)];
//     RemoteStorageClient *remote_storage = new(ptr) RemoteStorageClient(grpc::CreateChannel(sock_name,
//                                                                                            grpc::InsecureChannelCredentials()));
//     std::cout << "-------------- Start --------------" << std::endl;
//     //RemoteStorageClient* remote_storage=(RemoteStorageClient*)malloc(sizeof(RemoteStorageClient));
//     //remote_storage = new()
//     return remote_storage;
// }
// 
// void rs_send_data(RemoteStorageClient* ptr,const char* message) {
//     ptr->SendData(message);
// }
// 
// void rs_end(RemoteStorageClient* ptr) {
//     ptr->SendEnd();
//     free(ptr);
//     std::cout << "-------------- release mem --------------" << std::endl;
// }
 

// int main(int argc, char** argv) {
//     RemoteStorageClient remote_storage(
//         grpc::CreateChannel("localhost:50051",
//                             grpc::InsecureChannelCredentials())
//     );
//     std::cout << "-------------- Start --------------" << std::endl;
//     remote_storage.SendData("test");
//     return 0;
// }

int main(int argc, char** argv) {
    void* ptr;

    ptr = spy_pipe_start("python SpyPipeServer.py","port0");
    spy_pipe_send_data((RemoteStorageSolution*)ptr,"test222");
    spy_pipe_stop((RemoteStorageSolution*)ptr);

    return 0;
}
