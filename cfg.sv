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
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [0]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [1]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [4]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [5]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
        end while (fp);
    endfunction
endclass: SubCfg

class Cfg;
    int             v_int;
    string          v_str;
    real            v_real;
    SubCfg          subcfg;
    int             index_subcfg_array_0;

    function new();
        subcfg = new();
        subcfg_array[0] = new();
        subcfg_array[1] = new();
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
            if ($sscanf(content, $sformatf("%s.cfg.v_str=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.cfg.v_str=$$%%d$$\"%%%0ds\"", hierarchy, len, len), v_str) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.cfg.v_real=%%f", hierarchy), v_real)) continue;
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [0]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [1]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [4]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [5]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [0]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [1]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [4]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [5]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.int_list[%%d]=%%d", hierarchy), index_int_list_0, int_list[index_int_list_0])) continue;
            if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[0]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [0]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[1]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [1]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[4]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [4]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$%%s", hierarchy), len, tmp)); begin
                if ($sscanf(content, $sformatf("%s.[5]=$$%%d$$\"%%%0ds\"", hierarchy, len, len), [5]) begin;
                    continue;
                end
            end
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
            if ($sscanf(content, $sformatf("%s.array_array[%%d][%%d]=%%d", hierarchy), index_array_array_0, index_array_array_1, array_array[index_array_array_0][index_array_array_1])) continue;
        end while (fp);
    endfunction
endclass: Cfg