class {{sv_class.get_sv_type()}};
    {%- for var in sv_class.var_dict.values() %}
    {{var.render_declare()}}
    {%- endfor %}

    function new();
    {%- for content in sv_class.render_instantiate() %}
        {{content}}
    {%- endfor %}
    endfunction: new

    function load_value(string path, string hierarchy = "{{sv_class.get_sv_type()}}");
        int     f, fp;
        string  content, line, attr_name, value;

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

            {%- for content in sv_class.render_load_value() %}
            {{content}};
            {%- endfor %}
        end while (fp);
    endfunction
endclass: {{sv_class.get_sv_type()}}