import SpyLib::*;
class SubDemo;
    int                 a;
    real                b;


    function new();
        a = 'h0;
        b = 0;
    endfunction

    function void report();
        $display("a: %h", a);
        $display("b: %f", b);
    endfunction

    static function SpyBytes SerializeToOstream(bit[23:0] spy_field = 24'h0, input SubDemo value);
        SpyBytes   value_stream;

        value_stream = {
                            SpyInt::SerializeToOstream(1, value.a),
                            SpyFloat::SerializeToOstream(2, value.b)
                        };
        return SpyMessage::SerializeToOstream(spy_field, value_stream);
    endfunction

    static function void ParseFromIstream(ref SubDemo value, input SpyBytes stream, input SpyTag tag='{8'h0,24'h0,32'h0});
        SpyQofBytes stream_list;
        SpyBytes    substream;
        SpyTag      substream_tag;

        stream_list = SpyBase::SplitIstream(stream);
        foreach(stream_list[i]) begin
            substream = stream_list[i];
            substream_tag = SpyBase::ParseHeadFromIstream(substream);
            case(substream_tag.spy_field)
                24'h1:    SpyInt::ParseFromIstream(value.a, substream, substream_tag);
                24'h2:    SpyFloat::ParseFromIstream(value.b, substream, substream_tag);
            endcase
        end
    endfunction
endclass


class Demo;
    int                 a;
    real                b;
    string              c;
    bit [16:0]          d;
    SubDemo             e;
    real                f[];


    function new();
        a = 'h0;
        b = 0;
        c = "asdf";
        d = 17'h0;
        e = new();
        f = {2.4};
    endfunction

    function void report();
        $display("a: %h", a);
        $display("b: %f", b);
        $display("c: \"%s\"", c);
        $display("d: 17'h%h", d);
        e.report();
        foreach(f[i]) $display("f[%0d]: %f", i, f[i]);
    endfunction

    static function SpyBytes SerializeToOstream(bit[23:0] spy_field = 24'h0, input Demo value);
        SpyBytes   value_stream;

        value_stream = {
                            SpyInt::SerializeToOstream(1, value.a),
                            SpyFloat::SerializeToOstream(2, value.b),
                            SpyString::SerializeToOstream(3, value.c),
                            SpyBit#(17)::SerializeToOstream(4, value.d),
                            SubDemo::SerializeToOstream(5, value.e),
                            SpyList#(real, SpyFloat)::SerializeToOstream(6, value.f)
                        };
        return SpyMessage::SerializeToOstream(spy_field, value_stream);
    endfunction

    static function void ParseFromIstream(ref Demo value, input SpyBytes stream, input SpyTag tag='{8'h0,24'h0,32'h0});
        SpyQofBytes stream_list;
        SpyBytes    substream;
        SpyTag      substream_tag;

        stream_list = SpyBase::SplitIstream(stream);
        foreach(stream_list[i]) begin
            substream = stream_list[i];
            substream_tag = SpyBase::ParseHeadFromIstream(substream);
            case(substream_tag.spy_field)
                24'h1:    SpyInt::ParseFromIstream(value.a, substream, substream_tag);
                24'h2:    SpyFloat::ParseFromIstream(value.b, substream, substream_tag);
                24'h3:    SpyString::ParseFromIstream(value.c, substream, substream_tag);
                24'h4:    SpyBit#(17)::ParseFromIstream(value.d, substream, substream_tag);
                24'h5:    SubDemo::ParseFromIstream(value.e, substream, substream_tag);
                24'h6:    SpyList#(real, SpyFloat)::ParseFromIstream(value.f, substream, substream_tag);
            endcase
        end
    endfunction
endclass