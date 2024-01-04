import time
import random
from multiprocessing import Process, Manager
from server import Server
from client import Client
import matplotlib.pyplot as plt

def simulate_server(server, lock, clients_attended_day, clients_attended_month, total_lost_clients, average_rating, total_clients):
    server.run_server(lock, clients_attended_day, clients_attended_month, total_lost_clients, average_rating, total_clients)

def simulate_client(client, server, lock, clients_attended_day, total_lost_clients):
    # Simulate client requesting server
    start_time = time.time()
    time.sleep(random.uniform(0.1, 0.5))
    
    with lock:
        if clients_attended_day.value >= 3:
            print(f"Server {server.name} is busy. Client {client.name} is a lost client.")
            total_lost_clients.value += 1
        else:
            server.client_queue.put(client)
            client.server_name = server.name
            total_clients.value += 1
            print(f"Client {client.name} is being served by Server {server.name}.")
    
    end_time = time.time()
    client.record_chat_duration(end_time - start_time)

if __name__ == "__main__":
    manager = Manager()
    lock = manager.Lock()
    clients_attended_day = manager.Value('i', 0)
    clients_attended_month = manager.Value('i', 0)
    total_lost_clients = manager.Value('i', 0)
    average_rating = manager.Value('d', 0.0)
    total_clients = manager.Value('i', 0)

    # Create server instances
    server_a = Server("Server A")
    server_b = Server("Server B")

    # Create server processes
    process_a = Process(target=simulate_server, args=(server_a, lock, clients_attended_day, clients_attended_month, total_lost_clients, average_rating, total_clients))
    process_b = Process(target=simulate_server, args=(server_b, lock, clients_attended_day, clients_attended_month, total_lost_clients, average_rating, total_clients))

    # Start server processes
    process_a.start()
    process_b.start()

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
                simulate_client(client, server_a, lock, clients_attended_day, total_lost_clients)
            else:
                simulate_client(client, server_b, lock, clients_attended_day, total_lost_clients)

        # Allow time for processes to finish serving remaining clients
        process_a.join()
        process_b.join()

        end_time = time.time()
        elapsed_time = end_time - start_time
        performance_results.append(elapsed_time)

    # Plot the results
    plt.plot(client_numbers, performance_results, marker='o')
    plt.title('Performance Improvement with Different Numbers of Clients')
    plt.xlabel('Number of Clients')
    plt.ylabel('Elapsed Time (seconds)')
    plt.show()

    # Print server statistics
    print(f"\nServer A Statistics:")
    print(f"Attended Clients (Day): {clients_attended_day.value}")
    print(f"Attended Clients (Month): {clients_attended_month.value}")
    print(f"Average Rating: {average_rating.value}")
    print(f"Total Clients: {total_clients.value}")
    print(f"Total Lost Clients: {total_lost_clients.value}")

    print(f"\nServer B Statistics:")
    print(f"Attended Clients (Day): {clients_attended_day.value}")
    print(f"Attended Clients (Month): {clients_attended_month.value}")
    print(f"Average Rating: {average_rating.value}")
    print(f"Total Clients: {total_clients.value}")
    print(f"Total Lost Clients: {total_lost_clients.value}")

