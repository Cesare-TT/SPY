import "DPI-C" function chandle spy_pipe_start(input string command,input string name);
import "DPI-C" function void    spy_pipe_send_data(input chandle inst,input string str);
import "DPI-C" function void    spy_pipe_stop(input chandle inst);
import "DPI-C" function void    spy_pipe_debug_print(input string str);

//function rm_start("input")

class SpyPipe;

    string name;
    chandle cobj;

    function new(string name);
        this.name = name;
    endfunction

    task start(string server_start_command);
        cobj = spy_pipe_start(server_start_command,name);
    endtask

    function send_data(string data);
        spy_pipe_send_data(cobj,data);
    endfunction

    task stop();
        spy_pipe_stop(cobj);
    endtask

endclass