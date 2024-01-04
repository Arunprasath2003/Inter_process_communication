# simulation.py
import threading
import time
import random
from server import Server
from client import Client
import matplotlib.pyplot as plt
import multiprocessing

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
    interact with them.
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
