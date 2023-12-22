/*
For a pre-forked approach, we can use Python's multiprocessing module to spawn multiple processes. 
However, due to Python's Global Interpreter Lock (GIL), 
true parallelism may not be achieved with threads or forks. So that I used C. 
Creating a pre-forked server in Cm involves using the 
fork system call to create child processes that handle client requests
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8080
#define MAX_CHILDREN 5
/*
Each child process continuously accepts client connections and delegates the handling of each connection 
to the handle_client function
*/
void handle_client(int client_socket) {
    // Simulate server-client interaction
    sleep(1);
    // Add your server logic here

    close(client_socket);
}

int main() {
    int server_socket, client_socket, child_pid, status;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);

    /*
    The server creates a socket, binds it to a port, and listens for incoming connections.
    */
    // Create socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    // Set up server address struct
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Bind socket to address
    if (bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Error binding socket");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_socket, 5) == -1) {
        perror("Error listening for connections");
        exit(EXIT_FAILURE);
    }
    /*
    The server enters a loop where it forks multiple child processes, each capable of handling a client connection.
    */
    // Pre-forking loop
    for (int i = 0; i < MAX_CHILDREN; ++i) {
        child_pid = fork();

        if (child_pid == 0) { // Child process
            while (1) {
                // Accept a connection
                client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &client_len);
                if (client_socket == -1) {
                    perror("Error accepting connection");
                    exit(EXIT_FAILURE);
                }

                // Handle the client request
                handle_client(client_socket);
            }
        } else if (child_pid > 0) { // Parent process
            printf("Child process created with PID %d\n", child_pid);
        } else {
            perror("Error forking process");
            exit(EXIT_FAILURE);
        }
    }

    // Wait for all child processes to finish
    for (int i = 0; i < MAX_CHILDREN; ++i) {
        waitpid(-1, &status, 0);
    }

    // Close the server socket
    close(server_socket);

    return 0;
}
