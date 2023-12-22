import time
import random
import threading
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
    