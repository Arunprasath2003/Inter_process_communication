#Imported necessary modules
import time
import random
import threading
import matplotlib.pyplot as plt #TO PLOT GRAPH

class Server:
    def __init__(self, name):
        self.name = name
        self.clients_attended_day = 0
        self.clients_attended_month = 0
        self.total_clients = 0
        self.total_lost_clients = 0
        self.average_rating = 0.0
        self.current_client = None
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

    # ITERATIVE SERVING
    def start_serving(self, clients):
        for client in clients:
            self.serve_client(client)
    
    def run_server(self, clients):
        self.lock = threading.Lock()
        print(f"Server {self.name} started serving clients iteratively.")
        self.start_serving(clients)
        print(f"Server {self.name} finished serving clients. Exiting.")

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

if __name__ == "__main__":
    # Create a function to simulate the performance improvement with different numbers of clients
    def simulate_performance(client_numbers):
        results = []

        for num_clients in client_numbers:
            server = Server("Server A")
            clients = [Client(f"Client {i}") for i in range(num_clients)]

            start_time = time.time()
            server.run_server(clients)
            end_time = time.time()

            # Collect performance metrics
            elapsed_time = end_time - start_time
            results.append(elapsed_time)

        return results
    '''
    client numbers are varied accordingly
    '''
    # Vary the number of clients for performance testing
    client_numbers = [50, 100, 150, 200, 250, 300]

    # Simulate performance improvement with different numbers of clients
    performance_results = simulate_performance(client_numbers)

    # Plot the results
    plt.plot(client_numbers, performance_results, marker='o')
    plt.title('Performance Improvement with Different Numbers of Clients')
    plt.xlabel('Number of Clients')
    plt.ylabel('Elapsed Time (seconds)')
    plt.show()
