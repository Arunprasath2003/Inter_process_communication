'''
Imported necessary modules
'''
import time
import random
import os
import signal
import multiprocessing
'''
On Windows, the multiprocessing module is typically used for parallel processing. Both multiprocessing and forking allow creating separate child processes from a parent process.
They enable parallel execution of code across multiple processes simultaneously.
Processes have their own isolated memory spaces allowing simpler synchronization compared to threads.
'''
class Client:
    '''
    The constructor initializes various attributes of the client, 
    such as name, server_name and rating
    '''
    def __init__(self, name):
        self.name = name
        self.server_name = None
        self.rating = None
    '''
    Simulates finishing the chat and providing a rating.
    Sleeps for a short time to simulate processing.
    Prints a message indicating the client's rating for the server.
    '''
    def finish_chat(self, rating):
        # Simulate finishing the chat and providing a rating
        time.sleep(0.1)
        print(f"Client {self.name} has rated Server {self.server_name} with {rating} stars.")

class Server:
    def __init__(self, name):
        self.name = name
        self.clients_attended_day = 0
        self.clients_attended_month = 0
        self.total_clients = 0
        self.total_lost_clients = 0
        self.average_rating = 0.0
        self.current_client = None
        self.client_queue = []
        self.lock = multiprocessing.Lock()

    '''
    Simulates the interaction between the server and a client.
    Sleeps for a random time to simulate processing.
    Obtains a rating from the client and updates the server's statistics.
    '''
    def serve_client(self, client):
        # Simulate server-client interaction
        time.sleep(random.uniform(0.1, 0.5))
        # Obtain rating from client
        rating = random.randint(1, 5)
        with self.lock:
            self.average_rating = (self.average_rating * self.clients_attended_day + rating) / (self.clients_attended_day + 1)
            self.clients_attended_day += 1
            self.clients_attended_month += 1
            self.current_client = None
            self.total_clients += 1
    '''
    Iteratively serves a list of clients using the serve_client method.
    '''
    def start_serving(self):
        for client in self.client_queue:
            self.serve_client(client)
    '''
    Initiates the iterative serving process and prints messages about server status.
    '''
    def run_server(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        print(f"Server {self.name} started serving clients using multiprocessing.")
        self.start_serving()
        print(f"Server {self.name} finished serving clients. Exiting.")
'''
 The function determines whether the server can attend to the client or if the client should be marked as lost. 
 If the server is available, the client is added to the server's queue, and the server starts serving the client.
'''
def simulate_client(server, client):
    if server.clients_attended_day >= 3:
        print(f"Server {server.name} is busy. Client {client.name} is a lost client.")
        server.total_lost_clients += 1
    else:
        server.client_queue.append(client)
        client.server_name = server.name
        print(f"Client {client.name} is being served by Server {server.name}.")

if __name__ == "__main__":
    serverA = Server("Server A")
    serverB = Server("Server B")

    with open("client_data.txt", "r") as file:
        client_names = [line.strip() for line in file]

    clients = [Client(name) for name in client_names]

    # Use multiprocessing for both Unix-like and Windows systems
    process_a = multiprocessing.Process(target=serverA.run_server)
    process_a.start()

    process_b = multiprocessing.Process(target=serverB.run_server)
    process_b.start()

    # Simulate clients for both servers
    for client in clients:
        if random.choice([True, False]):  # Simulate random assignment to servers
            simulate_client(serverA, client)
        else:
            simulate_client(serverB, client)

    # Signal servers to exit
    process_a.join()
    process_b.join()

    # Print server statistics
    print(f"\nServer A Statistics:")
    print(f"Attended Clients (Day): {serverA.clients_attended_day}")
    print(f"Attended Clients (Month): {serverA.clients_attended_month}")
    print(f"Average Rating: {serverA.average_rating}")
    print(f"Total Clients: {serverA.total_clients}")
    print(f"Total Lost Clients: {serverA.total_lost_clients}")

    print(f"\nServer B Statistics:")
    print(f"Attended Clients (Day): {serverB.clients_attended_day}")
    print(f"Attended Clients (Month): {serverB.clients_attended_month}")
    print(f"Average Rating: {serverB.average_rating}")
    print(f"Total Clients: {serverB.total_clients}")
    print(f"Total Lost Clients: {serverB.total_lost_clients}")
    #CONCURRENCY
    print(f"Number of Concurrent Processes: {multiprocessing.active_children()}")
