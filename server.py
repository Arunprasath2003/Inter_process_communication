# server.py
import threading
import time
import random
from queue import Queue

class Server:
    def __init__(self, name):
        '''
        The constructor initializes various attributes of the server, such as name, clients_attended_day, total_clients, etc.
        '''
        self.name = name
        self.clients_attended_day = 0
        self.clients_attended_month = 0
        self.total_clients = 0
        self.total_lost_clients = 0
        self.average_rating = 0.0
        self.current_client = None
        self.client_queue = Queue()
        self.lock = threading.Lock()

    def serve_client(self, client):
        '''
        Simulates the interaction between the server and a client.
        Sleeps for a random time to simulate processing.
        Obtains a rating from the client and updates the server's statistics.
        '''
        # Simulate server-client interaction
        time.sleep(random.uniform(0.1, 0.5))
        # Obtain rating from client
        rating = random.randint(1, 5)
        with self.lock:
            self.average_rating = (self.average_rating * self.clients_attended_day + rating) / (self.clients_attended_day + 1)
            self.clients_attended_day += 1
            self.clients_attended_month += 1
            self.current_client = None

    def start_serving(self, clients=None):
        if clients is None:
            # Default behavior, serve clients from the queue
            while True:
                if not self.client_queue.empty():
                    client = self.client_queue.get()
                    self.current_client = client.name
                    self.serve_client(client)
                else:
                    time.sleep(1)
        else:
            # Iterative serving for a list of clients
            for client in clients:
                self.serve_client(client)

    def run_server(self, clients=None):
        self.lock = threading.Lock()
        if clients is None:
            # Start serving from the queue
            server_thread = threading.Thread(target=self.start_serving, daemon=True)
            server_thread.start()
        else:
            # Start iterative serving
            print(f"Server {self.name} started serving clients iteratively.")
            self.start_serving(clients)
            print(f"Server {self.name} finished serving clients. Exiting.")

