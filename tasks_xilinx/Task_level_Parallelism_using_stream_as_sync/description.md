A common dataflow pattern is where a writer and reader process
exchange data by writing/reading from external memory - in this case
because there are no direct channels of communication, both processes
will start as soon as possible.  This is a problem because the reader
process should not start until the writer has written out at least one
line of memory (or it will read garbage). 

To allow the writer to write out at least one line of memory, a stream
of can be used a synchronization mechanism