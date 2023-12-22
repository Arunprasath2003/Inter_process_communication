'''
Imported necessary modules
'''
import time
import random
import threading
import matplotlib.pyplot as plt #TO PLOT GRAPH
from queue import Queue

class Server:
    '''
    The constructor initializes various attributes of the server, such as name, clients_attended_day, total_clients, etc.
    lock is a threading lock used to synchronize access to shared resources.
    client_queue is a queue used for the threaded approach to enqueue clients.
    '''
    def __init__(self, name):
        self.name = name
        self.clients_attended_day = 0
        self.clients_attended_month = 0
        self.total_clients = 0
        self.total_lost_clients = 0
        self.average_rating = 0.0
        self.current_client = None
        self.client_queue = Queue()
        self.lock = threading.Lock()

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

    def start_serving(self):
        while True:
            if not self.client_queue.empty():
                client = self.client_queue.get()
                self.current_client = client.name
                self.serve_client(client)
            else:
                time.sleep(1)

    def run_server(self):
        server_thread = threading.Thread(target=self.start_serving, daemon=True)
        server_thread.start()
class Client:
    def __init__(self, name):
        self.name = name
        self.server_name = None
        self.rating = None
        self.chat_duration = 0  # Track the duration of the chat in seconds

    def finish_chat(self, rating):
        # Simulate finishing the chat and providing a rating
        self.rating = rating
        print(f"Client {self.name} has rated Server {self.server_name} with {rating} stars.")

    def record_chat_duration(self, duration):
        self.chat_duration = duration
        print(f"Client {self.name} had a chat duration of {duration} seconds.")

def simulate_server(server):#simulate the server
    server.run_server()

def simulate_client(client, server):
    # Simulate client requesting server
    start_time = time.time()
    time.sleep(random.uniform(0.1, 0.5))
    with server.lock:
        if server.clients_attended_day >= 3:
            print(f"Server {server.name} is busy. Client {client.name} is a lost client.")
            server.total_lost_clients += 1
        else:
            server.client_queue.put(client)
            client.server_name = server.name
            server.total_clients += 1
            print(f"Client {client.name} is being served by Server {server.name}.")
    end_time = time.time()
    client.record_chat_duration(end_time - start_time)

if __name__ == "__main__":
    # Create server instances
    server_a = Server("Server A")
    server_b = Server("Server B")

    # Vary the number of clients for performance testing
    client_numbers = [50, 100, 150, 200, 250, 300]

    # Simulate performance improvement with different numbers of clients
    performance_results = []

    for num_clients in client_numbers:
        start_time = time.time()

        # Simulate client-server communication
        for i in range(num_clients):
            client = Client(f"Client {i}")
            if i % 2 == 0:
                simulate_client(client, server_a)
            else:
                simulate_client(client, server_b)

        # Allow time for threads to finish serving remaining clients
        time.sleep(5)

        end_time = time.time()
        elapsed_time = end_time - start_time
        performance_results.append(elapsed_time)

    # Plot the results
    plt.plot(client_numbers, performance_results, marker='o')
    plt.title('Performance Improvement with Different Numbers of Clients')
    plt.xlabel('Number of Clients')
    plt.ylabel('Elapsed Time (seconds)')
    plt.show()
