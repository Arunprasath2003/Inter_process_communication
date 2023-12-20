**CHAT SERVER**
<br>
Created a session for each client. If there is no server actively available to server the client, then gave a waiting period for the client. If no server is available for the waiting period then the session ends and client is requested to start new session later.This client is called lost client.
<br>
Task of creating chat server using different approaches:
<br>
**Iterative Serving:**
1.	Serves client requests sequentially in a loop within same process
2.	Simple to implement, no parallelism
3.	Blocking I/O, only one request handled at a time
<br>
**Threading Techniques:**
1.	Creates multiple threads within one process
2.	Achieves parallel execution across threads
3.	Shared memory so need synchronization
4.  Lower overhead than processes
<br>
**Forking Techniques:**
1.	Creates separate child processes using fork()
2.	New processes fully replicate parent
3.	Separate memory so no explicit synchronization
4.	Parallel execution across processes
5.	Higher creation overhead than threads
<br>
**In summary:**
1.	Iterative serving has no concurrency
2.	Threading provides concurrency via parallel threads in same process
3.	Forking provides concurrency via new processes with separate memory

