#ITERATIVE SERVING APPROACH
import time #Can use the time module in Python scripts to work with time
import random #for generating or manipulating random integers
import threading #to run multiple threads (tasks, function calls) at the same time
from queue import Queue
from server import Server
from client import Client
import signal #Set handlers for asynchronous events
import multiprocessing
#On Windows, the multiprocessing module is typically used for parallel processing. Both multiprocessing and forking allow creating separate child processes from a parent process.
#They enable parallel execution of code across multiple processes simultaneously.
#Processes have their own isolated memory spaces allowing simpler synchronization compared to threads.
class iterative:#iterative serving
    class Server:
        def __init__(self, name):
            self.name = name
            self.clients_attended_day = 0
            self.clients_attended_month = 0
            self.total_clients = 0
            self.total_lost_clients = 0
            self.average_rating = 0.0
            self.current_client = None

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
        #ITERATIVE SERVING
        def start_serving(self, clients):
            for client in clients:
                self.serve_client(client)

        def run_server(self, clients):
            self.lock = threading.Lock()
            print(f"Server {self.name} started serving clients iteratively.")
            self.start_serving(clients)
            print(f"Server {self.name} finished serving clients. Exiting.")

    class Client:
        def __init__(self, name):
            self.name = name
            self.server_name = None
            self.rating = None

        def finish_chat(self, rating):
            # Simulate finishing the chat and providing a rating
            time.sleep(0.1)
            print(f"Client {self.name} has rated Server {self.server_name} with {rating} stars.")

    if __name__ == "__main__":
        serverA = Server("Server A")
        serverB = Server("Server B")

        with open("client_data.txt", "r") as file:
            client_names = [line.strip() for line in file]

        clients = [Client(name) for name in client_names]

        serverA.run_server(clients)
        serverB.run_server(clients)

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
        #LOAD FACTORS
        load_factor_serverA = serverA.clients_attended_day / (serverA.clients_attended_day + serverA.total_lost_clients)
        load_factor_serverB = serverB.clients_attended_day / (serverB.clients_attended_day + serverB.total_lost_clients)

#THREADING APPROACH
class threading:
    class Server:
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
            if server.clients_attended_day >= 3: #if server is already attending 3 clients, then server can't attend the client. Therefore it is lost client
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

        # Start server threads
        threading.Thread(target=simulate_server, args=(server_a,), daemon=True).start()
        threading.Thread(target=simulate_server, args=(server_b,), daemon=True).start()

        # Simulate client-server communication
        for i in range(1000):
            client = Client(f"Client {i}")
            if i % 2 == 0:
                simulate_client(client, server_a)
            else:
                simulate_client(client, server_b)

        # Allow time for threads to finish serving remaining clients
        time.sleep(5)

        # Print server statistics
        print(f"\nServer A Statistics:")
        print(f"Attended Clients (Day): {server_a.clients_attended_day}")
        print(f"Attended Clients (Month): {server_a.clients_attended_month}")
        print(f"Average Rating: {server_a.average_rating}")
        print(f"Total Clients: {server_a.total_clients}")
        print(f"Total Lost Clients: {server_a.total_lost_clients}")

        print(f"\nServer B Statistics:")
        print(f"Attended Clients (Day): {server_b.clients_attended_day}")
        print(f"Attended Clients (Month): {server_b.clients_attended_month}")
        print(f"Average Rating: {server_b.average_rating}")
        print(f"Total Clients: {server_b.total_clients}")
        print(f"Total Lost Clients: {server_b.total_lost_clients}")

#FORKING TECHNIQUE
class fork:
    class Server:
        def __init__(self, name):
            self.name = name
            self.start_time = time.time()
            self.clients_attended_today = 0
            self.clients_attended_month = 0
            self.total_clients_serviced = 0
            self.total_lost_clients = 0
            self.total_rating = 0
            self.current_client = None
            self.lock = multiprocessing.Lock()
            self.rating_lock = multiprocessing.Lock()

        def serve_client(self, client):
            with self.lock:
                self.current_client = client
                self.clients_attended_today += 1
                self.clients_attended_month += 1
                self.total_clients_serviced += 1
                self.total_rating += self.get_client_rating()
                print(f"{self.name} serving {client.name}")

                # Simulate processing time
                time.sleep(random.uniform(1, 5))

                # End session
                self.current_client = None

        def get_client_rating(self):
            # Simulate getting a rating from the client
            return random.randint(1, 5)

        def get_server_info(self):
            with self.lock:
                return {
                    "Name": self.name,
                    "Date and Time": time.ctime(),
                    "Clients Attended Today": self.clients_attended_today,
                    "Clients Attended Month": self.clients_attended_month,
                    "Average Rating": self.total_rating / max(1, self.total_clients_serviced),
                    "Total Clients Serviced": self.total_clients_serviced,
                    "Total Lost Clients": self.total_lost_clients,
                    "Current Client": self.current_client.name if self.current_client else None
                }

    class Client:
        def __init__(self, name, server):
            self.name = name
            self.server = server
            self.rating = None

        def start_session(self):
            print(f"{self.name} starting session with {self.server.name}")
            self.server.serve_client(self)
            self.rating = self.get_client_rating()
            print(f"{self.name} session ended. Rating: {self.rating}")

        def get_client_rating(self):
            # Simulate obtaining a rating from the client
            return random.randint(1, 5)

    def simulate_chat(client):
        client.start_session()

    def simulate_load_test(num_clients, num_servers):
        clients = [Client(f"Client {i}", random.choice(servers)) for i in range(num_clients)]
        processes = []

        for client in clients:
            process = multiprocessing.Process(target=simulate_chat, args=(client,))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

    if __name__ == "__main__":
        server_names = ["Server A", "Server B", "Server C"]
        servers = [Server(name) for name in server_names]

        # Assign servers to clients
        for server in servers:
            server_clients = random.sample(servers, min(3, len(servers)))
            server.clients = server_clients
            for client in server_clients:
                client.server = server

        simulate_load_test(num_clients=1000, num_servers=len(servers))

        # Print server information after load test
        for server in servers:
            print(server.get_server_info())
