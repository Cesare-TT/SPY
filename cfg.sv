class SubCfg;
    int             int_list[int];
    int             index_int_list_0;
    string          str_list[int];
    int             index_str_list_0;
    string          str_dict[int];
    int             index_str_dict_0;
    int             array_array[int][int];
    int             index_array_array_0;
    int             index_array_array_1;
    string          str_array_array[int][int];
    int             index_str_array_array_0;
    int             index_str_array_array_1;

    function new();
    endfunction: new

    function load_value(string path, string hierarchy = "SubCfg");
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
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.str_list[%%d]=$$%%d$$%%s", hierarchy), index_str_list_0, len, tmp)) begin
                if ($sscanf(content, $sformatf("%s.str_list[%d]=$$%d$$\"%%%0ds\"", hierarchy, index_str_list_0, len, len), str_list[index_str_list_0])) begin
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.str_dict[%%d]=$$%%d$$%%s", hierarchy), index_str_dict_0, len, tmp)) begin
                if ($sscanf(content, $sformatf("%s.str_dict[%d]=$$%d$$\"%%%0ds\"", hierarchy, index_str_dict_0, len, len), str_dict[index_str_dict_0])) begin
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.str_array_array[%%d][%%d]=$$%%d$$%%s", hierarchy), index_str_array_array_0, index_str_array_array_1, len, tmp)) begin
                if ($sscanf(content, $sformatf("%s.str_array_array[%d][%d]=$$%d$$\"%%%0ds\"", hierarchy, index_str_array_array_0, index_str_array_array_1, len, len), str_array_array[index_str_array_array_0][index_str_array_array_1])) begin
                    continue;
                end
            end
        end while (fp);
        $fclose(f);
    endfunction: load_value
    
    function print_value(string hierarchy = "SubCfg");
        foreach (int_list[index_int_list_0])
            $display("%s.int_list[%0d] = %0d", hierarchy, index_int_list_0, int_list[index_int_list_0]);
        foreach (str_list[index_str_list_0])
            $display("%s.str_list[%0d] = %0s", hierarchy, index_str_list_0, str_list[index_str_list_0]);
        foreach (str_dict[index_str_dict_0])
            $display("%s.str_dict[%0d] = %0s", hierarchy, index_str_dict_0, str_dict[index_str_dict_0]);
        foreach (array_array[index_array_array_0])
            foreach (array_array[index_array_array_0][index_array_array_1])
                $display("%s.array_array[%0d][%0d] = %0d", hierarchy, index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1]);
        foreach (str_array_array[index_str_array_array_0])
            foreach (str_array_array[index_str_array_array_0][index_str_array_array_1])
                $display("%s.str_array_array[%0d][%0d] = %0s", hierarchy, index_str_array_array_0, index_str_array_array_1, str_array_array[index_str_array_array_0][index_str_array_array_1]);
    endfunction: print_value
    
endclass: SubCfg

class Cfg;
    int             v_int;
    string          v_str;
    real            v_real;
    SubCfg          subcfg;
    SubCfg          subcfg_array[int][int];
    int             index_subcfg_array_0;
    int             index_subcfg_array_1;

    function new();
        subcfg = new();
        subcfg_array[0][0] = new();
        subcfg_array[1][0] = new();
        subcfg_array[2][0] = new();
    endfunction: new

    function load_value(string path, string hierarchy = "Cfg");
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
            if ($sscanf(content, $sformatf("%s.v_int=%%d", hierarchy), v_int)) continue;
            if ($sscanf(content, $sformatf("%s.v_str=$$%%d$$%%s", hierarchy), len, tmp)) begin
                if ($sscanf(content, $sformatf("%s.v_str=$$%d$$\"%%%0ds\"", hierarchy, len, len), v_str)) begin
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.v_real=%%f", hierarchy), v_real)) continue;
            if ($sscanf(content, $sformatf("%s.subcfg%%s", hierarchy), tmp)) subcfg = new();
            if ($sscanf(content, $sformatf("%s.subcfg_array[%%d][%%d]%%s", hierarchy), index_subcfg_array_0, index_subcfg_array_1, tmp)) begin
                if (!subcfg_array[index_subcfg_array_0][index_subcfg_array_1]) begin
                    subcfg_array[index_subcfg_array_0][index_subcfg_array_1] = new();
                end
            end
        end while (fp);
        $fclose(f);
        subcfg.load_value(path, "cfg.subcfg");
        foreach (subcfg_array[index_subcfg_array_0])
            foreach (subcfg_array[index_subcfg_array_0][index_subcfg_array_1])
                subcfg_array[index_subcfg_array_0][index_subcfg_array_1].load_value(path, $sformatf("%s.subcfg_array[%0d][%0d]", hierarchy, index_subcfg_array_0, index_subcfg_array_1));
    endfunction: load_value
    
    function print_value(string hierarchy = "Cfg");
        $display("%s.v_int = %0d", hierarchy, v_int);
        $display("%s.v_str = \"%0s\"", hierarchy, v_str);
        $display("%s.v_real = %0f", hierarchy, v_real);
        subcfg.print_value("cfg.subcfg");
        foreach (subcfg_array[index_subcfg_array_0])
            foreach (subcfg_array[index_subcfg_array_0][index_subcfg_array_1])
                subcfg_array[index_subcfg_array_0][index_subcfg_array_1].print_value($sformatf("%s.subcfg_array[%0d][%0d]", hierarchy, index_subcfg_array_0, index_subcfg_array_1));
    endfunction: print_value
    
endclass: Cfg