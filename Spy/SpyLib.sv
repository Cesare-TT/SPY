package SpyLib;

    `define debug_display       if ($test$plusargs("VERBOSE")) $display

    typedef byte            SpyBytes[];
    typedef SpyBytes        SpyQofBytes[$];
    typedef bit[31:0]       SpyWords[];
    typedef bit[63:0]       SpyBit64;
    typedef int unsigned    SpyUint;
    typedef struct packed {
        bit [7:0]   spy_type;
        bit [23:0]  spy_field;
        bit [31:0]  spy_len;
    } SpyTag;

    localparam align_width      = 8;

    localparam SPY_TYPE_BIT     = 8'h1;
    localparam SPY_TYPE_INT     = 8'h2;
    // localparam SPY_TYPE_INT32   = 8'h1;
    // localparam SPY_TYPE_INT64   = 8'h2;
    localparam SPY_TYPE_FLOAT   = 8'h3;
    localparam SPY_TYPE_MESSAGE = 8'h4;
    localparam SPY_TYPE_STRING  = 8'h5;
    localparam SPY_TYPE_LIST    = 8'h6;

    class SpyBase#(type T=bit[31:0]);
        function new();
        endfunction

        static function bit HasLength(bit [7:0] spy_type);
            case (spy_type)
                SPY_TYPE_BIT:       return 1'b1;
                SPY_TYPE_INT:       return 1'b0;
                SPY_TYPE_FLOAT:     return 1'b0;
                SPY_TYPE_MESSAGE:   return 1'b1;
                SPY_TYPE_STRING:    return 1'b1;
                SPY_TYPE_LIST:      return 1'b1;
                default:            return 1'b0;
            endcase
        endfunction

        // static function SpyUint GetLength(bit[7:0] spy_type, T value);
        //     SpyUint    len;
        //     case (spy_type)
        //         SPY_TYPE_BIT:       len = SpyUint'($ceil(real'($size(value))/8));
        //         SPY_TYPE_INT:       len = 4;
        //         SPY_TYPE_FLOAT:     len = 8;
        //         // SPY_TYPE_MESSAGE:   len = value.Getstream_length();
        //         SPY_TYPE_STRING:    len = $size(value);
        //         // SPY_TYPE_LIST:      len = value.Getstream_length()
        //         // default: 
        //     endcase
        //     return len;
        // endfunction

        static function SpyBytes SerializeHeadToOstream(input bit[7:0] spy_type, input bit [23:0] spy_field, input SpyBytes value_stream);
            SpyBytes    head_stream;
            int         head_len;
            SpyUint     value_len;

            case (spy_type)
                SPY_TYPE_INT:   head_len = 4;
                SPY_TYPE_FLOAT: head_len = 4;
                default:        head_len = 8;
            endcase

            head_stream = new[head_len];
            head_stream[0] = spy_type;
            for (int ptr=0; ptr<3; ptr++) begin
                head_stream[ptr+1] = spy_field[(ptr+1)*align_width-1 -: align_width];
            end
            if (head_len == 8) begin
                value_len = value_stream.size();
                for (int ptr=0; ptr<4; ptr++) begin
                    head_stream[ptr+4] = value_len[(ptr+1)*align_width-1 -: align_width];
                end
            end
            return {head_stream, value_stream};
        endfunction

        static function SpyTag ParseHeadFromIstream(input SpyBytes stream);
            SpyTag  tag;
            tag.spy_type  = stream[0];
            tag.spy_field = {stream[3], stream[2], stream[1]};

            case(tag.spy_type)
                SPY_TYPE_INT:   tag.spy_len = 4;
                SPY_TYPE_FLOAT: tag.spy_len = 8;
                default         tag.spy_len = SpyUint'({stream[7], stream[6], stream[5], stream[4]});
            endcase
            `debug_display("tag.spy_len: %0d", tag.spy_len);
            return tag;
        endfunction

        static function SpyQofBytes SplitIstream(input SpyBytes stream);
            SpyQofBytes stream_list;
            int         ptr = 8;
            SpyBytes    substream;
            int         stream_len;
            SpyTag      substream_tag;
            int         substream_len;
            
            stream_len = stream.size();
            while(ptr<stream_len) begin
                substream_tag = ParseHeadFromIstream(stream[ptr +:8]);
                substream_len =4+4*(HasLength(substream_tag.spy_type))+substream_tag.spy_len;
                substream = new[substream_len];
                for (int i=ptr; i<ptr+substream_len; i++) begin
                    substream[i-ptr] = stream[i];
                end
                stream_list.push_back(substream);
                ptr = ptr+substream_len;
            end
            return stream_list;
        endfunction
    endclass

    class SpyBit#(BIT_WIDTH) extends SpyBase#(bit[BIT_WIDTH-1:0]);
        function new();
            
        endfunction //new()

        static function SpyBytes SerializeToOstream(bit [23:0] field, bit [BIT_WIDTH-1:0] value);
            byte    stream[$];
            byte    tmp = 8'h0;
            int     ptr;

            ptr = 0;
            while(ptr*align_width<=BIT_WIDTH) begin
                if ((BIT_WIDTH%align_width>0) && (align_width*(ptr+1) > BIT_WIDTH)) begin
                    for (int i=0; i<BIT_WIDTH%align_width; i++) begin
                        tmp[i] = value[ptr*align_width+i];
                    end
                    stream.push_back(tmp);
                end else begin
                    stream.push_back(value[(ptr+1)*align_width-1 -: align_width]);
                end
                ptr++;
            end
            return SpyBase::SerializeHeadToOstream(SPY_TYPE_BIT, field, stream);
        endfunction

        static function void ParseFromIstream(ref bit[BIT_WIDTH-1:0] value, input SpyBytes stream, input SpyTag tag);
            // bit [BIT_WIDTH-1:0] value;

            for (int ptr=0; ptr<tag.spy_len; ptr++) begin
                if ((BIT_WIDTH%align_width==0) || (BIT_WIDTH>=(ptr+1)*align_width)) begin
                    `debug_display("BIT_WIDTH: %0d", BIT_WIDTH);
                    `debug_display("msb: %0d; lsb: %0d", (ptr+1)*align_width-1, ptr*align_width);
                    value[(ptr+1)*align_width-1 -: align_width] = stream[ptr+8];
                end else begin
                    `debug_display("msb: %0d; lsb: %0d", BIT_WIDTH-1, ptr*align_width);
                    for (int i=0; i<BIT_WIDTH%align_width; i++) begin
                        value[ptr*align_width+i] = stream[ptr+8][i];
                        `debug_display("value[%0d]: %0d", ptr*align_width+i, value[ptr*align_width+i]);
                        `debug_display("stream[%0d][%0d]: %0d", ptr+8, i, stream[ptr+8][i]);
                    end
                    // value[BIT_WIDTH-1 - BIT_WIDTH-1-BIT_WIDTH%align_width] = stream[ptr+8];
                    // `debug_display("value[%0d]: %0d", BIT_WIDTH-1 - BIT_WIDTH-1-BIT_WIDTH%align_width, value[BIT_WIDTH-1 - BIT_WIDTH-1-BIT_WIDTH%align_width]);
                    // `debug_display("stream[%0d]: %0d", ptr+8, stream[ptr+8]);
                end
            end
            // return value;
        endfunction
    endclass //SpyBit#(BIT_WIDTH)

    class SpyInt extends SpyBase#(int);
        function new();
            
        endfunction //new()

        static function SpyBytes SerializeToOstream(bit [23:0] field, int value);
            byte    stream[4];
            int     ptr;

            ptr = 0;
            for (int i=0; i<4; i++) stream[i] = value[(i+1)*align_width-1 -:align_width];
            return SpyBase::SerializeHeadToOstream(SPY_TYPE_INT, field, stream);
        endfunction

        static function void ParseFromIstream(ref int value, input SpyBytes stream, input SpyTag tag);
            for (int i=0; i<4; i++) value[(i+1)*align_width-1 -:align_width] = stream[i+4];
        endfunction
    endclass

    class SpyFloat extends SpyBase#(real);
        function new();
            
        endfunction //new()

        static function SpyBytes SerializeToOstream(bit [23:0] field, real value);
            byte        stream[8];
            int         ptr;
            SpyBit64    tmp;
            ptr = 0;
            tmp = $realtobits(value);
            for (int i=0; i<8; i++) stream[i] = tmp[(i+1)*align_width-1 -:align_width];
            return SpyBase::SerializeHeadToOstream(SPY_TYPE_FLOAT, field, stream);
        endfunction

        static function void ParseFromIstream(ref real value, input SpyBytes stream, input SpyTag tag);
            SpyBit64    tmp;
            for (int i=0; i<8; i++) tmp[(i+1)*align_width-1 -:align_width] = stream[i+4];
            value = $bitstoreal(tmp);
        endfunction
    endclass

    class SpyString extends SpyBase#(string);
        function new();
            
        endfunction //new()

        static function SpyBytes SerializeToOstream(bit [23:0] field, string value);
            byte    stream[$];
            int     ptr = 0;

            while(ptr<value.len()) begin
                stream[ptr] = SpyUint'(value[ptr]);
                ptr++;
            end
            return SpyBase::SerializeHeadToOstream(SPY_TYPE_STRING, field, stream);
        endfunction

        static function void ParseFromIstream(ref string value, input SpyBytes stream, input SpyTag tag);
            value = {tag.spy_len{" "}};
            for (int ptr=0; ptr<tag.spy_len; ptr++) begin
                value[ptr] = string'(stream[ptr+8]);
            end
        endfunction
    endclass

    class SpyList#(type ItemType, type ItemSpyType) extends SpyBase;
        function new();
            
        endfunction

        static function SpyBytes SerializeToOstream(bit [23:0] field, ItemType list[]);
            SpyBytes    value_stream;
            SpyBytes    item_stream;
            byte        stream[$];

            foreach(list[i]) begin
                item_stream = ItemSpyType::SerializeToOstream(i, list[i]);
                foreach(item_stream[i]) stream.push_back(item_stream[i]);
                item_stream.delete();
            end
            value_stream = stream;
            return SpyBase::SerializeHeadToOstream(SPY_TYPE_LIST, field, value_stream);
        endfunction
        
        static function void ParseFromIstream(ref ItemType value[], input SpyBytes stream, input SpyTag tag);
            SpyQofBytes stream_list;
            SpyBytes    substream;
            SpyTag      substream_tag;

            stream_list = SpyBase::SplitIstream(stream);
            value = new[stream_list.size()];
            foreach(stream_list[i]) begin
                substream = stream_list[i];
                foreach (substream[i]) $display("substream[%0d]: %h", i, substream[i]);
                substream_tag = SpyBase::ParseHeadFromIstream(substream);
                if (i == substream_tag.spy_field) ItemSpyType::ParseFromIstream(value[i], substream, substream_tag);
            end
        endfunction

    endclass

    class SpyMessage extends SpyBase;
        function new();
            
        endfunction

        static function SpyBytes SerializeToOstream(bit[23:0] field = 24'h0, input SpyBytes value_stream);
            return SpyBase::SerializeHeadToOstream(SPY_TYPE_MESSAGE, field, value_stream);
        endfunction
    endclass

endpackage