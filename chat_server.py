'''
Imported necessary modules
'''
import time
import random
import threading
import multiprocessing
from queue import Queue
'''
Server class
This class is designed to handle server operations in both an iterative and threaded manner, 
providing flexibility in the simulation based on the chosen approach.
'''
class Server:
    '''
    The constructor initializes various attributes of the server, such as name, clients_attended_day, total_clients, etc.
    lock is a threading lock used to synchronize access to shared resources.
    client_queue is a queue used for the threaded approach to enqueue clients.
    serve_client Method:
    '''
    def __init__(self, name):
        self.name = name
        self.clients_attended_day = 0
        self.clients_attended_month = 0
        self.total_clients = 0
        self.total_lost_clients = 0
        self.average_rating = 0.0
        self.current_client = None
        self.lock = threading.Lock()  # Lock for thread safety
        self.client_queue = Queue()  # Queue for threaded approach
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
    def start_serving(self, clients):
        for client in clients:
            self.serve_client(client)
    '''
    Initiates the iterative serving process and prints messages about server status.
    '''
    def run_server(self, clients):
        print(f"Server {self.name} started serving clients iteratively.")
        self.start_serving(clients)
        print(f"Server {self.name} finished serving clients. Exiting.")
    '''
    Enqueues a client in the client_queue for the threaded approach.
    Checks if the server is busy and marks the client as lost if necessary.
    '''
    def enqueue_client(self, client):
        with self.lock:
            if self.clients_attended_day >= 3:
                print(f"Server {self.name} is busy. Client {client.name} is a lost client.")
                self.total_lost_clients += 1
            else:
                self.client_queue.put(client)
                self.total_clients += 1
                print(f"Client {client.name} is being served by Server {self.name}.")
    '''
    Continuously runs in a separate thread to serve clients from the queue.
    '''
    def start_serving_threaded(self):
        while True:
            if not self.client_queue.empty():
                client = self.client_queue.get()
                self.current_client = client.name
                self.serve_client(client)
            else:
                time.sleep(1)
    '''
    Starts the threaded serving process in a separate thread.
    '''
    def run_server_threaded(self):
        server_thread = threading.Thread(target=self.start_serving_threaded, daemon=True)
        server_thread.start()
    '''
    Returns a dictionary containing information about the server, such as its name, the number of clients attended, average rating, etc
    '''
    def get_server_info(self):
        with self.lock:
            return {
                "Name": self.name,
                "Date and Time": time.ctime(),
                "Clients Attended Today": self.clients_attended_day,
                "Clients Attended Month": self.clients_attended_month,
                "Average Rating": self.average_rating,
                "Total Clients Serviced": self.total_clients,
                "Total Lost Clients": self.total_lost_clients,
                "Current Client": self.current_client
            }
'''
client class
'''
class Client:
    '''
    The constructor initializes various attributes of the client, 
    such as name, server_name, rating, and chat_duration.
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
    '''
    Records the duration of the chat in seconds.
    Prints a message indicating the chat duration.
    '''
    def record_chat_duration(self, duration):
        self.chat_duration = duration
        print(f"Client {self.name} had a chat duration of {duration} seconds.")
'''
The Simulate class acts as a utility class to coordinate the simulation process, 
allowing for different approaches (iterative, threading, forking) and printing server information 
after the simulation.
'''
class Simulate:
    '''
    Takes a Client instance and a Server instance as arguments.
    Simulates a client requesting the server by calling the server's enqueue_client method.
    Records the chat duration using the record_chat_duration method of the client.
    '''
    @staticmethod
    def simulate_client(server, client):
        # Simulate client requesting server
        start_time = time.time()
        time.sleep(random.uniform(0.1, 0.5))
        server.enqueue_client(client)
        client.server_name = server.name
        end_time = time.time()
        client.finish_chat(random.randint(1, 5))
        client.record_chat_duration(end_time - start_time)
    '''
    Takes a Server instance as an argument and simulates the server's behavior by calling its run_server method.
    This method is used to simulate the server's operation in an iterative manner.
    '''
    @staticmethod
    def simulate_server(server):
        server.run_server(clients)

    @staticmethod
    def simulate_threaded(server):
        server.run_server_threaded()

    '''
    Takes the number of clients, number of servers, simulation approach (iterative, threading, forking), and a list of client instances as arguments.
    Creates server instances and assigns clients to servers.
    Simulates server and client interactions based on the chosen approach.
    For iterative serving, it iterates through servers and clients.
    For threading, it starts separate threads for each server and client.
    For forking, it starts separate processes for each server and client.
    '''
    @staticmethod
    def simulate_load_test(num_clients, num_servers, approach):
        clients = [Client(f"Client {i}") for i in range(num_clients)]
        servers = [Server(f"Server {i}") for i in range(num_servers)]

        if approach == "iterative":#For iterative serving, it iterates through servers and clients.
            for server in servers:
                Simulate.simulate_server(server)
        elif approach == "threading":#For threading, it starts separate threads for each server and client.
            for server in servers:
                threading.Thread(target=Simulate.simulate_threaded, args=(server,), daemon=True).start()
            for i, client in enumerate(clients):
                threading.Thread(target=Simulate.simulate_client, args=(random.choice(servers), client)).start()
        elif approach == "forking":#For forking, it starts separate processes for each server and client.
            processes = []
            for server in servers:
                process = multiprocessing.Process(target=Simulate.simulate_server, args=(server,))
                processes.append(process)
                process.start()
            for i, client in enumerate(clients):
                process = multiprocessing.Process(target=Simulate.simulate_client, args=(random.choice(servers), client))
                processes.append(process)
                process.start()
            for process in processes:
                process.join()

    '''
    Takes a list of server instances as an argument.
    Prints information about each server using the get_server_info method of the Server class.
    '''
    @staticmethod
    def print_server_info(servers):
        for server in servers:
            print(server.get_server_info())

if __name__ == "__main__":
    '''
    Define the number of clients and servers for the load test
    '''
    num_clients = 1000
    num_servers = 3
    servers = [Server(f"Server {i}") for i in range(num_servers)]
    clients = [Client(f"Client {i}") for i in range(num_clients)]  # Define clients here

    '''
    Simulate the load test using iterative serving
    '''
    # Iterative Serving
    Simulate.simulate_load_test(num_clients, num_servers, "iterative")
    Simulate.print_server_info(servers)
    '''
    Simulate the load test using threading
    '''
    # Threading
    Simulate.simulate_load_test(num_clients, num_servers, "threading")
    Simulate.print_server_info(servers)
    '''
    Simulate the load test using forking
    '''
    # Forking
    Simulate.simulate_load_test(num_clients, num_servers, "forking")
    Simulate.print_server_info(servers)
