
module top();

    SpyPipe rs0,rs1;

    initial begin
        rs0 = new("port0");
        rs1 = new("port1");
        rs0.start("python SpyPipeServer.py");
        rs1.start("python SpyPipeServer.py");
        rs0.send_data("test string from sv.");
        rs1.send_data("test string from sv.");
        rs0.stop();
        rs1.stop();
    end

    //chandle rs_obj;

    //initial begin
    //    rs_obj = rs_start("port0");
    //    rs_send_data(rs_obj,"test string from sv.");
    //    rs_end(rs_obj);
    //end


endmodule