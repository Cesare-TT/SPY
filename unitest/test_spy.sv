`include "SpyTest.sv"

class SpyTest #(BIT_WIDTH);
    Demo        Demo_T, Demo_R;

    function new();
        Demo_T = new();
        Demo_R = new();
    endfunction

    function SpyBytes load_stream(input string path);
        int         f, code;
        bit [7:0]   mem[int];
        SpyBytes    stream;

        $readmemh(path, mem);
        stream = new[mem.size()];
        foreach(mem[i]) stream[i] = mem[i];
        return stream;
    endfunction

    function void save_stream(input string path, input SpyBytes stream);
        $writememh(path, stream);
    endfunction

    function void ParseFromIstream(input string path);
        SpyBytes    stream;

        stream  = load_stream(path);
        Demo::ParseFromIstream(Demo_R, stream);
    endfunction

    function void SerializeToOstream(input string path);
        SpyBytes    stream;

        stream = Demo::SerializeToOstream(0, Demo_T);
        save_stream(path, stream);
    endfunction

    task int_test(input string ipath, input string opath);
        SpyBytes    stream;
        int         INT_T, INT_R;
        SpyTag      tag;

        tag.spy_type = SPY_TYPE_INT;
        stream = load_stream(ipath);
        SpyInt::ParseFromIstream(INT_R, stream, tag);
        `debug_display("INT_R: %0d", INT_R);
        INT_T = INT_R;
        stream.delete();
        stream = SpyInt::SerializeToOstream(tag.spy_field, INT_R);
        foreach(stream[i])  `debug_display("stream[%0d]: %h", i, stream[i]);
        save_stream(opath, stream);
    endtask

    task bit_test(input string ipath, input string opath);
        SpyBytes            stream;
        bit [BIT_WIDTH-1:0] BIT_T, BIT_R;
        SpyTag              tag;

        tag.spy_type = SPY_TYPE_BIT;
        tag.spy_len  = SpyUint'($ceil(real'(BIT_WIDTH)/8));
        stream = load_stream(ipath);
        foreach(stream[i])  `debug_display("stream[%0d]: %h", i, stream[i]);
        SpyBit#(BIT_WIDTH)::ParseFromIstream(BIT_R, stream, tag);
        `debug_display("BIT_R: %0d", BIT_R);
        BIT_T = BIT_R;
        stream.delete();
        stream = SpyBit#(BIT_WIDTH)::SerializeToOstream(tag.spy_field, BIT_R);
        foreach(stream[i])  `debug_display("stream[%0d]: %h", i, stream[i]);
        save_stream(opath, stream);
    endtask

    task float_test(input string ipath, input string opath);
        SpyBytes            stream;
        real                FLOAT_T, FLOAT_R;
        SpyTag              tag;

        tag.spy_type = SPY_TYPE_FLOAT;
        stream = load_stream(ipath);
        SpyFloat::ParseFromIstream(FLOAT_R, stream, tag);
        `debug_display("FLOAT_R: %0f", FLOAT_R);
        FLOAT_T = FLOAT_R;
        stream.delete();
        stream = SpyFloat::SerializeToOstream(tag.spy_field, FLOAT_R);
        foreach(stream[i])  `debug_display("stream[%0d]: %0h", i, stream[i]);
        save_stream(opath, stream);
    endtask

    task string_test(input string ipath, input string opath);
        SpyBytes            stream;
        string              STRING_T, STRING_R;
        SpyTag              tag;

        tag.spy_type = SPY_TYPE_STRING;
        stream = load_stream(ipath);
        tag.spy_len = SpyUint'({stream[7], stream[6], stream[5], stream[4]});
        SpyString::ParseFromIstream(STRING_R, stream, tag);
        `debug_display("STRING_R: %s", STRING_R);
        STRING_T = STRING_R;
        stream.delete();
        stream = SpyString::SerializeToOstream(tag.spy_field, STRING_R);
        foreach(stream[i])  `debug_display("stream[%0d]: %0h", i, stream[i]);
        save_stream(opath, stream);
    endtask

    task list_test(input string ipath, input string opath);
        SpyBytes            stream;
        string              LIST_T[], LIST_R[];
        SpyTag              tag;

        tag.spy_type = SPY_TYPE_LIST;
        stream = load_stream(ipath);
        tag.spy_len = SpyUint'({stream[7], stream[6], stream[5], stream[4]});
        foreach(stream[i])  `debug_display("stream[%0d]: %0h", i, stream[i]);
        SpyList#(string, SpyString)::ParseFromIstream(LIST_R, stream, tag);
        foreach (LIST_R[i]) begin
            `debug_display("LIST_R[%0d]: %s", i, LIST_R[i]);
        end
        LIST_T = LIST_R;
        stream.delete();
        stream = SpyList#(string, SpyString)::SerializeToOstream(tag.spy_field, LIST_R);
        foreach(stream[i])  `debug_display("stream[%0d]: %0h", i, stream[i]);
        save_stream(opath, stream);
    endtask

    task class_test(input string ipath, input string opath);
        ParseFromIstream(ipath);
        Demo_R.report();
        Demo_T = Demo_R;
        SerializeToOstream(opath);
    endtask

endclass

module tb;
    SpyTest#(`BIT_WIDTH) Test;

    initial begin
        // if ($value$plusargs("BIT_WIDTH=%0d", BIT_WIDTH)) begin
        //     $display("BIT_WIDTH = %0d", BIT_WIDTH);
        // end else begin
        //     BIT_WIDTH = 32;
        //     $display("BIT_WIDTH = %0d", BIT_WIDTH);
        // end
        Test = new();
        if ($test$plusargs("SPY_INT_TEST"))     Test.int_test("SpyStreamPy2Sv", "SpyStreamSv2Py");
        if ($test$plusargs("SPY_FLOAT_TEST"))   Test.float_test("SpyStreamPy2Sv", "SpyStreamSv2Py");
        if ($test$plusargs("SPY_STRING_TEST"))  Test.string_test("SpyStreamPy2Sv", "SpyStreamSv2Py");
        if ($test$plusargs("SPY_BIT_TEST"))     Test.bit_test("SpyStreamPy2Sv", "SpyStreamSv2Py");
        if ($test$plusargs("SPY_LIST_TEST"))    Test.list_test("SpyStreamPy2Sv", "SpyStreamSv2Py");
        if ($test$plusargs("SPY_CLASS_TEST"))   Test.class_test("SpyStreamPy2Sv", "SpyStreamSv2Py");
    end
endmodule