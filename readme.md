
# 2D Drone Simulation

This project simulates a drone navigating within a 2D environment. The drone's sensors calculate distances forward, backward, right, and left, and log these distances along with the drone's instantaneous speed. The simulation allows for user-controlled movements and logs data to a CSV file.

## Assessment

**Objective:** Two-dimensional modeling of a structure as the drone's sensors "sense the environment". This involves creating a code that models all the drone's sensors (odometer forward, backward, right, and left) given its position and speed. The code should define an interface that allows the calculation of all four distances given the location and orientation of the drone.

### Solution Overview

The project is structured into various modules to handle different aspects of the simulation. The main components are:

- **AutoAlgo:** Contains algorithms for sensor calculations.
- **Drone:** Manages the drone's state and movement logic.
- **Graph:** Handles graphical operations such as drawing the map and the drone.
- **Map:** Manages loading and checking the map.
- **Point:** Provides basic operations related to points (optional).
- **Tools:** Contains utility functions.
- **WorldParams:** Contains parameters and constants for the world.
- **SimulationWindow:** Sets up the main simulation window and handles events.
- **DistanceLogger:** Calculates and logs distances 10 times per second.

### AutoAlgo

The `AutoAlgo` class is responsible for the core algorithms used to calculate distances. This includes methods to compute the distance between two points and to calculate the distances sensed by the drone's sensors (forward, backward, right, and left) based on its position and speed.

### Drone

The `Drone` class manages the drone's state, including its position, speed, pitch, roll, yaw, and battery status. It also contains methods to update the drone's position and speed based on its movement and sensor readings.

### Graph

The `Graph` class handles all graphical operations. This includes drawing the drone on the screen and managing the graphical representation of buttons used to start and stop the simulation.

### Map

The `Map` class is responsible for loading the map image and checking whether a given position on the map is walkable. This ensures that the drone can only move within designated areas.

### Point

The `Point` class provides basic operations related to points, such as calculating the distance between two points. This class is optional and can be used to extend the functionality as needed.

### Tools

The `Tools` module includes utility functions such as finding a safe starting position for the drone, ensuring it starts within a walkable area and at a safe distance from obstacles.

### WorldParams

The `WorldParams` module contains various constants and parameters used throughout the simulation, such as screen dimensions, drone speed, acceleration, and button dimensions.

### SimulationWindow

The `SimulationWindow` class sets up the main simulation window and handles user interactions, including starting and stopping the simulation and controlling the drone's movement. It integrates all the other modules to provide a cohesive simulation environment.

### DistanceLogger

The `DistanceLogger` class calculates and logs the distances sensed by the drone's sensors 10 times per second. It writes this data to a CSV file, including forward, backward, right, left distances, and the drone's instantaneous speed.

## Usage

1. **Run the simulation:**

    ```sh
    python SimulationWindow.py
    ```

2. **Control the drone:**

    - **Start the simulation:** Click the "Start" button.
    - **Stop the simulation:** Click the "Stop" button.
    - **Control the drone:**
      - **Arrow keys:** Control the pitch and roll (direction of movement).
      - **W/S keys:** Control the yaw (rotation).
      - **Space key:** Toggle takeoff and landing.

3. **Logging:**

    The simulation logs the forward, backward, right, left distances, and the instantaneous speed of the drone to `distance_log.csv` 10 times per second.

## Logging Data

The `DistanceLogger` module logs the distances and speeds to a CSV file named `distance_log.csv` located in the same directory as the script. The data is logged 10 times per second and includes:

- Forward distance
- Backward distance
- Right distance
- Left distance
- Instantaneous speed
- Timestamp

## Contributing

Feel free to fork this repository, create a feature branch, and submit a pull request. We welcome contributions that improve the simulation or add new features.

## License

need to change
