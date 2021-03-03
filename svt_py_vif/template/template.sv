class {{sv_class.get_sv_type()}};
    {%- for var in sv_class.var_dict.values() %}
    {%- for content in var.render_declare() %}
    {{content}}
    {%- endfor %}
    {%- endfor %}

    function new();
    {%- for content in sv_class.render_instantiate() %}
        {{content}}
    {%- endfor %}
    endfunction: new

    function load_value(string path, string hierarchy = "{{sv_class.get_sv_type()}}");
        int     f, fp;
        string  content, line, attr_name, value;
        string  tmp;
        int     len;

        f = $fopen(path, "r");
        do begin
            content = "";
            fp = $fgets(line, f);
            for (int i=0; i<line.len(); i++) begin
                if (line.getc(i) == "#") begin
                    break;
                end else if ((line.getc(i) != " ") && (line.getc(i) != "\t") && (line.getc(i) != "\n")) begin
                    content = {content, line.getc(i)};
                end
            end

            {%- for content in sv_class.render_scan_value() %}
            {{content}}
            {%- endfor %}
        end while (fp);
        $fclose(f);
        {%- for content in sv_class.render_load_value() %}
        {{content}}
        {%- endfor %}
    endfunction
endclass: {{sv_class.get_sv_type()}}