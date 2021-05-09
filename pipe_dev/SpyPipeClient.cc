
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
using grpc::ClientReaderWriter;
using spy_pipe_pkg::Data;
//using spy_pipe_pkg::ReceivedCount;
using spy_pipe_pkg::SpyPipeGRPC;



class RemoteStorageClient {

public:

    std::shared_ptr<ClientReaderWriter<Data,Data>> stream;
    ClientContext context;

    RemoteStorageClient(std::shared_ptr<Channel> channel)
        :stub_(SpyPipeGRPC::NewStub(channel)){//},
         //stream(stub_->SendData(&context)) {
        stream = std::shared_ptr<ClientReaderWriter<Data,Data>>(stub_->SendData(&context));
        std::cout << "Client::Connected." << std::endl;
    }





    void SendData(const std::string& message) {
        ClientContext context;
        Data          data,data2;
        Data received_count;
        std::cout << "Client::SendData started." << std::endl;
        //std::unique_ptr<ClientWriter<Data> > writer(stub_->SendData(&context, &received_count));
        //std::shared_ptr<ClientReaderWriter<Data,Data>> stream(stub_->SendData(&context));
    //std::shared_ptr<ClientReaderWriter<RouteNote, RouteNote> > stream(
    //    stub_->RouteChat(&context));

        data.set_payload(message);
        stream->Write(data);
        std::cout << "Client::SendData write finished." << std::endl;
        //stream->WritesDone();
        std::cout << "Client::SendData write_done finished." << std::endl;
        //Status status = stream->Finish();
        std::cout << "Client::SendData stream finished." << std::endl;
        //if (!status.ok()) {
        //    std::cout << "Client::SendData failed." << std::endl;
        //}
        //else {
        //    std::cout << "Client send data:"<< data.payload() << "   " << std::endl;
        //}
        //stream->Read(&data2);
        //std::cout << data2.payload() << std::endl;

        std::cout << "Client::SendData end." << std::endl;
    }

    void SendEnd(){
        ClientContext context;
        Data          data;
        Data received_count;
        //std::unique_ptr<ClientWriter<Data> > writer(stub_->SendData(&context, &received_count));
        //std::shared_ptr<ClientReaderWriter<Data,Data>> stream(stub_->SendData(&context));

        data.set_control("end");
        stream->Write(data);
        stream->WritesDone();
        //Status status = stream->Finish();
        // if (status.ok()) {
        //     std::cout << "Response:"<< received_count.control() << "   " << std::endl;
        // }
        // else {
        //     std::cout << "something wrong" << std::endl;
        //     std::cout << "Response:"<< received_count.control() << "   " << std::endl;
        // }
        std::cout << "Client::SendEnd end." << std::endl;

    }

    char* GetData(){
        std::cout << "Client::GetData started." << std::endl;
        ClientContext context;
        Data          data;
        //std::shared_ptr<ClientReaderWriter<Data,Data>> stream(stub_->SendData(&context));
        stream->Read(&data);
        std::cout << "Client::GetData read finished." << std::endl;
        std::cout << "Client::"<< data.payload() << std::endl;
        //stream->Finish();
        //Status status = stream->Finish();
        std::cout << "Client::GetData stream finish finished." << std::endl;
        //if (!status.ok()) {
        //    std::cout << "Client::GetData failed." << std::endl;
        //}
        char *p;
        strcpy(p,data.payload().c_str());
        return p;
    }

private:
    std::unique_ptr<SpyPipeGRPC::Stub> stub_;
};


void* call_python_server(void *args){
    //char* name = (char*)args;
    //char command[100];
    std::cout << "Client::start server:"<< (char*)args << std::endl;
    system((char*)args);
    //sprintf(command,"python server.py %s",(char*)args);
}

class RemoteStorageSolution{

public:
    RemoteStorageSolution(const char* command,const char* name_in){
        char sock_name[100];
        char full_command[200];
        sprintf(sock_name,"unix:SpyPipe_%s.sock",name_in);
        sprintf(full_command,"%s %s",command,name_in);
        
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

    char* get_data(){
        //char *p = 
        //std::cout << "Client::GetData stream finish finished2." << std::endl;
        return this->client->GetData();
    }

    void finish(){
        this->client->SendEnd();
        std::cout << "Client::Start to wait python server shutdown." << std::endl;
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

char* spy_pipe_get_data(RemoteStorageSolution* ptr) {
    return ptr->get_data();
    //std::cout << "Client::GetData stream finish finished3." << std::endl;
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
    //spy_pipe_send_data((RemoteStorageSolution*)ptr,"test223");
    //spy_pipe_send_data((RemoteStorageSolution*)ptr,"test224");
    
    std::cout << spy_pipe_get_data((RemoteStorageSolution*)ptr) << std::endl;
    std::cout << "========================================================" << std::endl;
    //std::cout << spy_pipe_get_data((RemoteStorageSolution*)ptr) << std::endl;
    //std::cout << spy_pipe_get_data((RemoteStorageSolution*)ptr) << std::endl;
    spy_pipe_stop((RemoteStorageSolution*)ptr);
    return 0;
}
