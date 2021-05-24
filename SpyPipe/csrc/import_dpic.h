
 extern void* spy_pipe_start(/* INPUT */const char* command, /* INPUT */const char* name);

 extern void spy_pipe_send_data(/* INPUT */void* inst, /* INPUT */const char* str);

 extern void spy_pipe_stop(/* INPUT */void* inst);

 extern void spy_pipe_debug_print(/* INPUT */const char* str);
