`include "cfg.sv"

module tb;
    Cfg  cfg;

    initial begin
        cfg = new();
        cfg.load_value("cfg.cfg", "cfg");
        $display("cfg.attr0 = %0d", cfg.attr0);
        $display("cfg.attr1 = %s", cfg.attr1);
        $display("cfg.attr2 = %0f", cfg.attr2);
        foreach(cfg.subcfg.attr3[i]) $display("cfg.subcfg.attr3[%0d] = %s", i, cfg.subcfg.attr3[i]);
        foreach(cfg.subcfg.attr4[i]) $display("cfg.subcfg.attr4[%0d] = %s", i, cfg.subcfg.attr4[i]);
        foreach(cfg.subcfg.attr5[i]) $display("cfg.subcfg.attr5[%s] = %0d", i, cfg.subcfg.attr5[i]);
        foreach(cfg.subcfg_array[0].attr3[i]) $display("cfg.subcfg_array[0].attr3[%0d] = %s", i, cfg.subcfg_array[0].attr3[i]);
        foreach(cfg.subcfg_array[0].attr4[i]) $display("cfg.subcfg_array[0].attr4[%0d] = %s", i, cfg.subcfg_array[0].attr4[i]);
        foreach(cfg.subcfg_array[0].attr5[i]) $display("cfg.subcfg_array[0].attr5[%s] = %0d", i, cfg.subcfg_array[0].attr5[i]);
        foreach(cfg.subcfg_array[1].attr3[i]) $display("cfg.subcfg_array[1].attr3[%0d] = %s", i, cfg.subcfg_array[1].attr3[i]);
        foreach(cfg.subcfg_array[1].attr4[i]) $display("cfg.subcfg_array[1].attr4[%0d] = %s", i, cfg.subcfg_array[1].attr4[i]);
        foreach(cfg.subcfg_array[1].attr5[i]) $display("cfg.subcfg_array[1].attr5[%s] = %0d", i, cfg.subcfg_array[1].attr5[i]);
    end

endmodule