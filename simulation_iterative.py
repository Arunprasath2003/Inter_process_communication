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
    # Create a function to simulate the performance improvement with different numbers of clients
    def simulate_performance(client_numbers):
        results = []

        for num_clients in client_numbers:
            serverA = Server("Server A")
            clients = [Client(f"Client {i}") for i in range(num_clients)]

            start_time = time.time()
            serverA.run_server(clients)
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
    
  # Print server statistics
    for num_clients in client_numbers:
        server = Server("Server A")
        clients = [Client(f"Client {i}") for i in range(num_clients)]
        server.run_server(clients)

        print(f"\nServer A Statistics for {num_clients} clients:")
        print(f"Attended Clients (Day): {server.clients_attended_day}")
        print(f"Attended Clients (Month): {server.clients_attended_month}")
        print(f"Average Rating: {server.average_rating}")
        print(f"Total Clients: {server.total_clients}")
        print(f"Total Lost Clients: {server.total_lost_clients}")


