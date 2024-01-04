# client.py

import time

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
