`include "cfg.sv"

module tb;
    Cfg  cfg;

    initial begin
        int i, j, k, l;
        cfg = new();
        cfg.load_value("cfg.cfg", "cfg");
        cfg.print_value();
    end
endmodule

// virtual class print #(parameter type T = int);
//     function T print_value (T item, string name);
//         case (type(T))
//             type(int):      $display("%s = %0d", name, item);
//             type(real):     $display("%s = %0f", name, item);
//             type(string):   $display("%s = %s", name, item);
//             default:        begin
//                 int i;
//                 string str_i;
//                 foreach (item[i]) print_value#(type(item[i])) (item[i], {name, "[", str_i.itoa(i), "]"});
//             end
//         endcase
//     endfunction
// endclass