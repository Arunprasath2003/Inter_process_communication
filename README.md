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
<img width="379" alt="final output iterative serving" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/187fc53b-1a8a-47cc-8b55-b62bf5a21477">
<br>

**Threading Techniques:**
1.	Creates multiple threads within one process
2.	Achieves parallel execution across threads
3.	Shared memory so need synchronization
4.  Lower overhead than processes
<br>
<img width="393" alt="output2" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/3cba2d97-ef57-4230-8d40-038aa5c2cdc5">
<img width="379" alt="output 1" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/726d61d4-cc7e-4e33-b779-0107535bd545">
<br>

**Forking Techniques:**
1.	Creates separate child processes using fork()
2.	New processes fully replicate parent
3.	Separate memory so no explicit synchronization
4.	Parallel execution across processes
5.	Higher creation overhead than threads
<br>
<img width="286" alt="forking output" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/76447d80-640f-4b9b-a295-3535499951a3">
<br>

**Performance improvement over different number of clients**
<br>

The graph shows how the elapsed time varies with the number of clients, providing insights into the performance of the server under different loads. The elapsed time increases as the number of clients increases.
<br>

<img width="477" alt="performance improvement iterative" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/8869f79a-eae0-4d79-ab6f-7023ab4e7f6a">
<br>
Threading performance improvement over different number of clients
<br>

<img width="473" alt="performance improvement threading" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/28c87b0f-fce6-40dd-abac-1a2175df6ffe">

<br>

**In summary:**
1.	Iterative serving has no concurrency
2.	Threading provides concurrency via parallel threads in same process
3.	Forking provides concurrency via new processes with separate memory
<br>

**Pre threaded and pre forked approach:**
<br>
Pre-forked and pre-threaded are techniques used in server design to optimize performance by pre-initializing a pool of forked processes or threads that can handle client connections in parallel.
<br>

**Pre-forked Approach:**

1. A master parent process pre-forks multiple child process copies of itself at startup using fork() system call.
2. The child processes then listen for incoming client connections concurrently.
3. When a connection arrives, it is accepted by one of the available child processes from the pool.
4. After serving the client, the child process returns to the pool ready for next connection.
<br>

![Screenshot from 2023-12-25 12-12-24](https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/9cad03a8-4613-4604-9aaf-5bdeee31562f)
<br>

**Advantages:**
<br>
1. Avoids overhead of creating new processes for every connection.
2. Allows parallel processing of multiple clients due to pre-created pool.
<br>

**Pre-threaded Approach:**

1. The server pre-initializes a pool of threads at startup and reuses them.
2. An acceptor thread picks incoming connections and passes to worker threads.
3. Once request is served, worker thread returns to pool.
<br>
<img width="393" alt="prethreading output" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/630bfee7-65a9-493f-91ea-2c3ad079fd01">
<br>

**Advantages:**
<br>
1. Faster than creating new threads per request.
2. Achieves parallel execution via fewer threads than processes.
<br>

So in summary, pre-forking and threading optimizes servers by initializing resources for concurrency upfront before traffic starts.

