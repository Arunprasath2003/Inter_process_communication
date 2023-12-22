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
<img width="477" alt="performance improvement iterative" src="https://github.com/Arunprasath2003/Inter_process_communication/assets/98107416/8869f79a-eae0-4d79-ab6f-7023ab4e7f6a">
<br>

**In summary:**
1.	Iterative serving has no concurrency
2.	Threading provides concurrency via parallel threads in same process
3.	Forking provides concurrency via new processes with separate memory

