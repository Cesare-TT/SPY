`include "cfg.sv"

module tb;
    Cfg  cfg;

    initial begin
        int i, j, k, l;
        cfg = new();
        cfg.load_value("cfg.cfg", "cfg");
        $display("cfg.v_int = %0d", cfg.v_int);
        $display("cfg.v_str = %s", cfg.v_str);
        $display("cfg.v_real = %0f", cfg.v_real);
        foreach(cfg.subcfg.str_list[i]) $display("cfg.subcfg.str_list[%0d] = %s", i, cfg.subcfg.str_list[i]);
        foreach(cfg.subcfg.str_dict[i]) $display("cfg.subcfg.str_dict[%0d] = %s", i, cfg.subcfg.str_dict[i]);
        foreach(cfg.subcfg.int_list[i]) $display("cfg.subcfg.int_list[%0d] = %0d", i, cfg.subcfg.int_list[i]);
        foreach(cfg.subcfg.array_array[i])
            foreach (cfg.subcfg.array_array[i][j]) $display("cfg.subcfg.array_array[%0d][%0d] = %0d", i, j, cfg.subcfg.array_array[i][j]);
        foreach(cfg.subcfg.str_array_array[i])
            foreach (cfg.subcfg.str_array_array[i][j]) $display("cfg.subcfg.str_array_array[%0d][%0d] = %s", i, j, cfg.subcfg.str_array_array[i][j]);
        // i=0;
        // j=0;
        // k=0;
        // l=0;
        foreach(cfg.subcfg_array[i]) begin
            foreach (cfg.subcfg_array[i][j]) begin
                foreach(cfg.subcfg_array[i][j].str_list[k]) $display("cfg.subcfg_array[%0d][%0d].str_list[%0d] = %s", i, j, k, cfg.subcfg_array[i][j].str_list[k]);
                foreach(cfg.subcfg_array[i][j].str_dict[k]) $display("cfg.subcfg_array[%0d][%0d].str_dict[%0d] = %s", i, j, k, cfg.subcfg_array[i][j].str_dict[k]);
                foreach(cfg.subcfg_array[i][j].int_list[k]) $display("cfg.subcfg_array[%0d][%0d].int_list[%0d] = %0d", i, j, k, cfg.subcfg_array[i][j].int_list[k]);
                foreach(cfg.subcfg_array[i][j].array_array[k])
                    foreach (cfg.subcfg_array[i][j].array_array[k][l]) $display("cfg.subcfg_array[%0d][%0d].array_array[%0d][%0d] = %0d", i, j, k, l, cfg.subcfg_array[i][j].array_array[k][l]);
                foreach(cfg.subcfg_array[i][j].str_array_array[k])
                    foreach (cfg.subcfg_array[i][j].str_array_array[k][l]) $display("cfg.subcfg_array[%0d][%0d].str_array_array[%0d][%0d] = %s", i, j, k, l, cfg.subcfg_array[i][j].str_array_array[k][l]);
            end
        end
        if (cfg.subcfg_array[0][0]) begin
            $display("exist");
            $display("cfg.subcfg_array[%0d][%0d].str_list[%0d] = %s", i, j, k, cfg.subcfg_array[0][0].str_list[0]);
                // foreach(cfg.subcfg_array[0][0].str_dict[k]) $display("cfg.subcfg_array[%0d][%0d].str_dict[%0d] = %s", 0, 0, 0, cfg.subcfg_array[0][0].str_dict[k]);
                // foreach(cfg.subcfg_array[0][0].int_list[k]) $display("cfg.subcfg_array[%0d][%0d].int_list[%0d] = %0d", i, j, k, cfg.subcfg_array[0][0].int_list[k]);
                // foreach(cfg.subcfg_array[0][0].array_array[k])
                //     foreach (cfg.subcfg_array[0][0].array_array[k][l]) $display("cfg.subcfg_array[%0d][%0d].array_array[%0d][%0d] = %0d", i, j, k, l, cfg.subcfg_array[0][0].array_array[k][l]);
                // foreach(cfg.subcfg_array[0][0].str_array_array[k])
                //     foreach (cfg.subcfg_array[0][0].str_array_array[k][l]) $display("cfg.subcfg_array[%0d][%0d].str_array_array[%0d][%0d] = %s", i, j, k, l, cfg.subcfg_array[0][0].str_array_array[k][l]);
        end else begin
            $display("not exist");
        end
    end

endmodule