
---

# Autonomous Drone Simulator

## Project Overview

In this project, we delve into the world of control and management of autonomous drones. The project is divided into two main parts:

1. **Platform Search and Sensor Modeling**: 
   - Find a platform that allows three-dimensional (or two-dimensional) modeling of a structure as the drone's sensors sense the environment.
   - Define an interface that allows the calculation of all six distances given the location and orientation of the drone.

2. **Basic Control System for a Drone**:
   - Develop a basic control system for a drone to allow it to fly over as much terrain as possible.
   - Ensure the drone returns to the take-off point when the battery reaches 50%.

### Background
- Before starting, please read the [following article](https://docs.google.com/document/d/1eo34T_M7jfduRZm_oevy94YY2LkGLzRT/edit#heading=h.pbpc1ivctwps).


Autonomous drones are increasingly becoming an integral part of various industries due to their ability to perform tasks without human intervention. These drones are used in fields such as agriculture for crop monitoring, delivery services for transporting goods, surveillance for security purposes, and environmental monitoring for data collection in hard-to-reach areas. The development of autonomous drones involves complex algorithms and precise sensor integration to ensure they can navigate and perform tasks efficiently in dynamic environments.

This project focuses on simulating the behavior of an autonomous drone in a 2D environment. It draws inspiration from a comprehensive study detailed in this article, authored by three undergraduate students. The article discusses the modeling of a Tello drone equipped with additional sensors and a mission computer. The sensors provide critical data for the drone's navigation and task execution, enabling it to operate autonomously both in simulation and real-world conditions. The following videos describe the drone's autonomous flight in simulation and in real conditions:

## Getting Started

### Prerequisites

- Python 3.x
- `pygame` library

Install the required libraries using pip:
```bash
pip install pygame
```

### Project Structure

### Explanation of the Simplified Project Structure Dependencies



![אבד](https://github.com/roni5604/Model_2D_drone_simulator/assets/98646866/2217ec9d-87f0-4f50-823f-f54da5107187)





The diagram illustrates the key dependencies between the main components of the Autonomous Drone Simulator project. Each node represents a crucial file in the project, and the arrows indicate the dependencies between them.

- **SimulationWindow.py**: This is the main simulation window and user interface. It orchestrates the overall simulation, integrating various components.
  - **Depends on**:
    - **AutoAlgo1.py**: The main algorithm for autonomous drone control. It contains the logic for navigating the drone autonomously.
    - **Drone.py**: This file represents the drone's functionalities, including its sensors and movement capabilities.
    - **CPU.py**: Manages the timing and execution of different functions, ensuring that the simulation runs smoothly.
- **AutoAlgo1.py**:
  - **Depends on**:
    - **CPU.py**: Utilized for managing the timing and execution of the drone's control algorithms.
    - **Drone.py**: Interacts with the drone's functionalities to execute control commands.
    - **Lidar.py**: Simulates the Lidar sensors on the drone, providing distance measurements crucial for navigation and obstacle avoidance.

This simplified diagram highlights the essential interactions and dependencies necessary for the drone's autonomous control and simulation environment, providing a clear view of the project's core structure.

### Running the Simulation

1. Ensure the `Maps` directory contains the map images (`p12.png`, `p13.png`, `p14.png`, `p15.png`).
2. Run the `SimulationWindow.py` to start the simulation:
```bash
python SimulationWindow.py
```

## Features

- **Autonomous Navigation**: The drone navigates the environment using its sensors.
- **Collision Detection**: The drone detects obstacles using Lidar sensors.
- **Graph Visualization**: Visualizes the drone's path and explored areas.
- **Real-time Control**: Allows user input to control the drone's speed, direction, and mode.

## User Interface

- **Start/Pause**: Toggles the simulation.
- **Speed Up/Down**: Adjusts the drone's speed.
- **Spin**: Rotates the drone by a specified angle.
- **Toggle Map**: Toggles the real map view.
- **Toggle AI**: Toggles the autonomous control.
- **Return Home**: Commands the drone to return to the starting point.
- **Open Graph**: Visualizes the path taken by the drone.
- **Snake Driver**: Toggles the snake driver movement mode.

## Drone Specifications

- **Sensors**:
  - 4 Distance Meters (right, left, forward, backward)
  - Speed Sensor (Optical Flow)
  - Orientation Sensor (IMU)
  - Barometer
  - Battery Sensor

- **Capabilities**:
  - Forward Angle (Pitch): ±10 degrees, 100 degrees/second, 1 m/s², max speed 3 m/s
  - Side Angle (Roll): ±10 degrees, 100 degrees/second, 1 m/s², max speed 3 m/s
  - Angular Velocity (Yaw): 100+ degrees/second
  - Battery Status: 8 minutes maximum flight time (480 seconds)
  - 10Hz sensor measurements: [d0-d4, yaw, Vx, Vy, Z, baro, bat, pitch, roll, accX, accY, accZ]

### Instructions

1. **Part One**:
   - Search for a platform that allows 3D or 2D modeling of a structure based on the drone's sensor data.
   - Define an interface to calculate the distances given the drone's location and orientation.

2. **Part Two**:
   - Develop a basic control system to allow the drone to explore the terrain and return to the take-off point at 50% battery.

### Sensors Characteristics

- **Distance Meter**: ±2% error, detection range 0-3 meters
- Each pixel on the map represents 2.5 cm

## Explanation of Main Classes

### AutoAlgo1

`AutoAlgo1` is the main class that controls the autonomous behavior of the drone.

- **Attributes**:
  - `map_size`: Size of the map.
  - `map`: 2D array representing the state of each pixel on the map.
  - `drone`: Instance of the `Drone` class.
  - `points`: List of points representing the drone's path.
  - `m_graph`: Instance of the `Graph` class.
  - `ai_cpu`: Instance of the `CPU` class managing the AI updates.
  - Various flags and parameters to manage the drone's behavior.

- **Methods**:
  - `play()`: Starts the drone and AI.
  - `update(delta_time)`: Updates the drone's state and AI logic.
  - `speed_up()`: Increases the drone's speed.
  - `speed_down()`: Decreases the drone's speed.
  - `update_map_by_lidars()`: Updates the map based on Lidar sensor data.
  - `update_visited()`: Marks the current position as visited.
  - `set_pixel(x, y, state)`: Sets the state of a pixel on the map.
  - `paint_blind_map(screen)`: Draws the explored map.
  - `paint_points(screen)`: Draws the path points.
  - `paint(screen)`: Draws the drone and its environment.
  - `ai(delta_time)`: Main AI logic for autonomous navigation.
  - `spin_by(degrees)`, `spin_by2(degrees, is_first, func)`: Handles drone rotation.
  - `update_rotating(delta_time)`: Updates the drone's rotation state.

### CPU

`CPU` manages the timing and execution of various functions.

- **Attributes**:
  - `hz`: Frequency of execution.
  - `functions_list`: List of functions to be executed.
  - `is_play`: Flag indicating whether the CPU is running.
  - `elapsed_milli`: Elapsed time in milliseconds.
  - `thread`: Thread running the CPU loop.

- **Methods**:
  - `stop_all_cpus()`, `resume_all_cpus()`: Static methods to stop or resume all CPUs.
  - `resume()`: Resumes the CPU.
  - `add_function(func)`: Adds a function to the execution list.
  - `play()`: Starts the CPU.
  - `stop()`: Stops the CPU.
  - `reset_clock()`: Resets the elapsed time.
  - `thread_run()`: Main loop for executing functions.

### Drone

`Drone` represents the drone and its functionalities.

- **Attributes**:
  - `real_map`: The map the drone is navigating.
  - `start_point`, `point_from_start`, `sensor_optical_flow`: Points representing various positions of the drone.
  - `lidars`: List of Lidar sensors.
  - `speed`, `rotation`, `gyro_rotation`: Movement parameters.
  - `cpu`: Instance of the `CPU` class managing the drone updates.
  - `drone_img_path`, `mImage`: Path and image of the drone.

- **Methods**:
  - `play()`, `stop()`: Start and stop the drone.
  - `add_lidar(degrees)`: Adds a Lidar sensor.
  - `get_point_on_map()`: Gets the current position of the drone on the map.
  - `update(delta_time)`: Updates the drone's state.
  - `format_rotation(rotation_value)`: Formats the rotation value.
  - `get_rotation()`, `get_gyro_rotation()`: Gets the current rotation values.
  - `get_optical_sensor_location()`: Gets the optical sensor's position.
  - `rotate_left(delta_time)`, `rotate_right(delta_time)`: Rotates the drone.
  - `speed_up(delta_time)`, `slow_down(delta_time)`: Adjusts the drone's speed.
  - `paint(screen)`: Draws the drone on the screen.

### SimulationWindow

`SimulationWindow` is the main simulation window and user interface.

- **Attributes**:
  - `screen`, `clock`: Pygame screen and clock.
  - `running`, `toogleStop`: Flags for managing the simulation state.
  - `info_label`, `info_label2_rect`: Information labels.
  - `buttons`: List of UI buttons.
  - `algo1`: Instance of the `AutoAlgo1` class.

- **Methods**:
  - `initialize()`: Initializes the

 simulation window.
  - `toggle_cpu()`, `speed_up()`, `speed_down()`, `spin_by(degrees)`: Button actions.
  - `toggle_real_map()`, `toggle_ai()`, `return_home_func()`, `open_graph()`, `toggle_snackDriver()`: Additional button actions.
  - `update_info(delta_time)`: Updates the information labels.
  - `main()`: Main loop for running the simulation.

## Additional Information

### References

- [Link to Article](https://docs.google.com/document/d/1eo34T_M7jfduRZm_oevy94YY2LkGLzRT/edit#heading=h.pbpc1ivctwps)
- [link to base project](https://github.com/vection/DroneSimulator)

---
