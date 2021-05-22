class {{ast.__class__.__name__}};


    {%- for var in ast.content_as_list %}
    {{var.sv_var_declr}};
    {%- endfor %}


    function new();
        {%- for var in ast.content_as_list %}
        {{var.name}} = {{var.sv_default_value}};
        {%- endfor %}
    endfunction

    function void report();
        {%- for content in ast.sv_report_string() %}
        {{content}}
        {%- endfor %}
    endfunction

    static function SpyBytes SerializeToOstream(bit[23:0] spy_field = 24'h0, input {{ast.__class__.__name__}} value);
        SpyBytes   value_stream;

        value_stream = {
                            {%- for field, var in ast.content_as_dict[0:-1] %}
                            {{var.sv_spy_type}}::SerializeToOstream({{field}}, value.{{var.name}}),
                            {%- endfor %}
                            {{ast.content_as_dict[-1][1].sv_spy_type}}::SerializeToOstream({{ast.content_as_dict[-1][0]}}, value.{{ast.content_as_dict[-1][1].name}})
                        };
        return SpyMessage::SerializeToOstream(spy_field, value_stream);
    endfunction

    static function void ParseFromIstream(ref {{ast.__class__.__name__}} value, input SpyBytes stream, input SpyTag tag='{8'h0,24'h0,32'h0});
        SpyQofBytes stream_list;
        SpyBytes    substream;
        SpyTag      substream_tag;

        stream_list = SpyBase::SplitIstream(stream);
        foreach(stream_list[i]) begin
            substream = stream_list[i];
            substream_tag = SpyBase::ParseHeadFromIstream(substream);
            case(substream_tag.spy_field)
                {%- for field, var in ast.content_as_dict %}
                24'h{{field}}:    {{var.sv_spy_type}}::ParseFromIstream(value.{{var.name}}, substream, substream_tag);
                {%- endfor %}
            endcase
        end
    endfunction

    function string SerializeToString();
        string      Ostring;
        SpyBytes    Ostream;
        string      str_bytes;

        Ostream = this.SerializeToOstream(0, this);
        foreach (Ostream[i]) begin
            str_bytes.hextoa(Ostream[i]);
            if (Ostream[i] < 8'h10) begin
                Ostring = {Ostring, "0", str_bytes};
            end else begin
                Ostring = {Ostring, str_bytes};
            end
        end
        return Ostring;
    endfunction
endclass