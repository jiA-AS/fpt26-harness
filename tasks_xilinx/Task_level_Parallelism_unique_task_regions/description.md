This example shows how to call a dataflow function that contains a task region. 
Recall that a hls:task should not be treated as a function call - instead a hls::task 
needs to be thought of as a persistent instance statically bound to channels. Due to 
this, it will be your responsibility to ensure that multiple invocations to any function 
that contains hls::tasks be uniquified or these calls will use the same hls::tasks and channels.

This examples shows how you can use the function template 