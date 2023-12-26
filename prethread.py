import time
import random
import threading
from queue import Queue
'''
In a pre-threaded or pre-forked approach, the servers are pre-created and running before clients start interacting 
with them. This is in contrast to the on-demand approach, where servers are spawned or instantiated dynamically 
as clients request service. The pre-threaded and pre-forked approach aims to improve efficiency by having a 
pool of ready-to-serve servers.
'''
class prethreaded:
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
        '''
         This method creates a loop where the server continuously checks for clients in its queue. 
         If there are clients waiting, it takes one client at a time, serves it, and then repeats the process. 
         If there are no clients in the queue, it waits for 1 second before checking again.
        '''
        def start_serving(self):
            while True:
                if not self.client_queue.empty():
                    client = self.client_queue.get()
                    self.current_client = client.name
                    self.serve_client(client)
                else:
                    time.sleep(1)
        '''
        The run_server method creates a new thread and sets its target to the start_serving method. 
        The thread is then marked as a daemon thread and started. The start_serving method, which 
        continuously serves clients, will run concurrently in the background while the main program or 
        other threads can continue their execution.
        '''
        def run_server(self):
            server_thread = threading.Thread(target=self.start_serving, daemon=True)
            server_thread.start()

    class Client:
        '''
        The constructor initializes various attributes of the client, 
        such as name, server_name, rating, and chat_duration.
        '''
        def __init__(self, name):
            self.name = name
            self.server_name = None
            self.rating = None
            self.chat_duration = 0  # Track the duration of the chat in seconds
        '''
        Simulates finishing the chat and providing a rating.
        Sleeps for a short time to simulate processing.
        Prints a message indicating the client's rating for the server.
        '''
        def finish_chat(self, rating):
            self.rating = rating
            print(f"Client {self.name} has rated Server {self.server_name} with {rating} stars.")
        '''
        Records the duration of the chat in seconds.
        Prints a message indicating the chat duration.
        '''
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
        '''
        Two server instances (server_a and server_b) are created and their threads are started before any clients 
        interact with them.(pre threaded approach)
        '''
        # Create server instances
        server_a = Server("Server A")
        server_b = Server("Server B")

        # Start server threads
        server_a.run_server()
        server_b.run_server()

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
