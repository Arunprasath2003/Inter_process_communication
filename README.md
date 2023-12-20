Created a session for each client. If there is no server actively available to server the client, then gave a waiting period for the client. If no server is available for the waiting period then the session ends and client is requested to start new session later.This client is called lost client.
Task of creating chat server using different approaches:
Iterative Serving:
•	Serves client requests sequentially in a loop within same process
•	Simple to implement, no parallelism
•	Blocking I/O, only one request handled at a time
Threading Techniques:
•	Creates multiple threads within one process
•	Achieves parallel execution across threads
•	Shared memory so need synchronization
•	Lower overhead than processes
Forking Techniques:
•	Creates separate child processes using fork()
•	New processes fully replicate parent
•	Separate memory so no explicit synchronization
•	Parallel execution across processes
•	Higher creation overhead than threads
In summary:
•	Iterative serving has no concurrency
•	Threading provides concurrency via parallel threads in same process
•	Forking provides concurrency via new processes with separate memory

