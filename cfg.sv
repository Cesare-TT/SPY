class SubCfg;
    string      attr3[int];
    string      attr4[int];
    int         attr5[string];

    function new();
    endfunction: new

    function load_value(string path, string hierarchy = "SubCfg");
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
            $sscanf(content, $sformatf("%s.attr3[0]=%%s", hierarchy), attr3[0]);
            $sscanf(content, $sformatf("%s.attr3[1]=%%s", hierarchy), attr3[1]);
            $sscanf(content, $sformatf("%s.attr4[4]=%%s", hierarchy), attr4[4]);
            $sscanf(content, $sformatf("%s.attr4[5]=%%s", hierarchy), attr4[5]);
            $sscanf(content, $sformatf("%s.attr5[\"6\"]=%%d", hierarchy), attr5["6"]);
            $sscanf(content, $sformatf("%s.attr5[\"7\"]=%%d", hierarchy), attr5["7"]);
        end while (fp);
    endfunction
endclass: SubCfg

class Cfg;
    int         attr0;
    string      attr1;
    real        attr2;
    SubCfg      subcfg;
    SubCfg      subcfg_array[int];

    function new();
        subcfg = new();
        subcfg_array[0] = new();
        subcfg_array[1] = new();
    endfunction: new

    function load_value(string path, string hierarchy = "Cfg");
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
            $sscanf(content, $sformatf("%s.attr0=%%d", hierarchy), attr0);
            $sscanf(content, $sformatf("%s.attr1=%%s", hierarchy), attr1);
            $sscanf(content, $sformatf("%s.attr2=%%f", hierarchy), attr2);
            subcfg.load_value(path, "cfg.subcfg");
            subcfg_array[0].load_value(path, "cfg.subcfg_array[0]");
            subcfg_array[1].load_value(path, "cfg.subcfg_array[1]");
        end while (fp);
    endfunction
endclass: Cfg