import csv
import time
from threading import Thread

class DistanceLogger:
    def __init__(self, drone, interval=0.1):
        self.drone = drone
        self.interval = interval
        self.running = False
        self.thread = None

    def calculate_distances(self):
        forward_distance = self.drone.x + self.drone.speed_x
        backward_distance = self.drone.x - self.drone.speed_x
        right_distance = self.drone.y + self.drone.speed_y
        left_distance = self.drone.y - self.drone.speed_y
        return forward_distance, backward_distance, right_distance, left_distance

    def log_distances(self):
        with open('distance_log.csv', 'w', newline='') as csvfile:
            fieldnames = ['Time', 'Forward', 'Backward', 'Right', 'Left', 'Speed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            start_time = time.time()
            while self.running:
                forward, backward, right, left = self.calculate_distances()
                speed = (self.drone.speed_x**2 + self.drone.speed_y**2)**0.5
                writer.writerow({
                    'Time': time.time() - start_time,
                    'Forward': forward,
                    'Backward': backward,
                    'Right': right,
                    'Left': left,
                    'Speed': speed
                })
                time.sleep(self.interval)

    def start_logging(self):
        self.running = True
        self.thread = Thread(target=self.log_distances)
        self.thread.start()

    def stop_logging(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
