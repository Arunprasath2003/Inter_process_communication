/*
For a pre-forked approach, we can use Python's multiprocessing module to spawn multiple processes. 
However, due to Python's Global Interpreter Lock (GIL), 
true parallelism may not be achieved with threads or forks. So that I used C. 
Creating a pre-forked server in Cm involves using the 
fork system call to create child processes that handle client requests
*/
//The server forks multiple child processes to handle incoming connections concurrently.
//used linux(ubuntu) to run this code
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h> // works only on unix based systems
#include <netinet/in.h>
#include <sys/wait.h>

#define PORT 8080
#define MAX_CHILDREN 5

void handle_client(int client_socket) {
    // Simulate server-client interaction
    sleep(1);
    // Obtain rating from client
    int rating = rand() % 5 + 1;
    printf("Server handling client. Rating: %d\n", rating);

    close(client_socket);
}

int main() {
    int server_socket, client_socket, child_pid;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);

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

    // Pre-forking loop
    for (int i = 0; i < MAX_CHILDREN; ++i) {
        child_pid = fork();

        if (child_pid == 0) { // Child process
            printf("Child process created with PID %d\n", getpid());

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
            printf("Parent process continuing\n");
        } else {
            perror("Error forking process");
            exit(EXIT_FAILURE);
        }
    }

    // Parent process waits for all child processes to finish
    for (int i = 0; i < MAX_CHILDREN; ++i) {
        wait(NULL);
    }

    // Close the server socket
    close(server_socket);

    return 0;
}
