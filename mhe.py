import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg


def update_position_velocity(position, velocity, acceleration, time_interval):
    new_velocity = velocity + acceleration * time_interval
    new_position = position + velocity * time_interval + 0.5 * acceleration * time_interval ** 2
    return new_position, new_velocity


def plot_graphs(accelerations, positions, velocities, time_points, car_image):
    plt.clf()

    # Plotting the Car's Position
    plt.subplot(4, 1, 1)
    plt.imshow(car_image, aspect='auto', extent=[positions[-1] - 5, positions[-1] + 5, 0, 1], zorder=2)
    # line at the end of the road
    plt.plot([150, 150], [0, 1], color='k', linestyle='--', zorder=1)
    plt.xlim(0, 150)
    plt.ylim(0, 1)
    plt.axis('off')

    # Plotting Acceleration
    plt.subplot(4, 1, 2)
    plt.step(time_points, accelerations + [accelerations[-1]], where='post', label='Acceleration')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Piecewise Constant Acceleration')
    plt.plot([15, 15], [-10, 160], color='k', linestyle='--', zorder=1)
    plt.xlim(0, 15.5)
    plt.ylim(-10, 10)
    plt.grid(True)

    # Plotting Velocity
    plt.subplot(4, 1, 3)
    plt.plot(time_points, velocities, label='Velocity')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity Over Time')
    plt.xlim(0, 15.5)
    plt.ylim(-1, 24)
    plt.axhline(y=0, color='r', linestyle='--')  # Target Velocity
    plt.plot([15, 15], [-10, 160], color='k', linestyle='--', zorder=1)
    plt.grid(True)

    # Plotting Position
    plt.subplot(4, 1, 4)
    plt.plot(time_points, positions, label='Position')
    plt.plot([15, 15], [-10, 160], color='k', linestyle='--', zorder=1)
    plt.ylabel('Position (m)')
    plt.xlabel('Time (s)')
    plt.title('Position Over Time')
    plt.axhline(y=150, color='r', linestyle='--')  # Target Position
    plt.xlim(0, 15.5)
    plt.ylim(-15, 155)
    plt.grid(True)

    plt.tight_layout()
    plt.pause(0.001)


def calculate_score(positions, velocities, total_time):
    target_position = 150
    distance_error = abs(target_position - positions[-1])
    velocity_error = abs(velocities[-1])
    score = distance_error + 10 * velocity_error + total_time * 1000
    return score


def show_instructions():
    instructions = """
    Welcome to the Car Motion Game!

    Instructions:
    1. You will input 15 piecewise constant accelerations.
    2. The maximum velocity is 23 m/s.
    3. Your goal is to reach exactly 150 meters as quickly as possible with a velocity of 0 m/s.
    4. The game ends if your position exceeds 150 meters or if your velocity exceeds 23 m/s.
    5. The score is calculated based on the time taken to reach 150 meters, with penalties for not stopping at 0 m/s.
    6. Minimize your time to reach the target for a better score.

    Good luck!
    """
    messagebox.showinfo("Game Instructions", instructions)


def start_game():
    max_velocity = 23
    max_acceleration = 5
    min_acceleration = -7
    time_interval = 1
    total_time = 0

    accelerations = []
    positions = [0]
    velocities = [0]
    time_points = [0]

    car_image = mpimg.imread('car.png')  # Load the car image

    plt.ion()
    plt.show()

    for i in range(15):  # 15 intervals
        current_position = positions[-1]
        current_velocity = velocities[-1]
        prompt_message = f"Segment {i + 1}/15\nCurrent Position: {current_position:.2f} m, Velocity: {current_velocity:.2f} m/s\nEnter acceleration (between -7 and 5):"

        acceleration = simpledialog.askfloat("Input", prompt_message, minvalue=min_acceleration,
                                             maxvalue=max_acceleration)
        if acceleration is None:  # Cancel was pressed
            break

        position, velocity = update_position_velocity(current_position, current_velocity, acceleration, time_interval)
        total_time += time_interval
        time_points.append(total_time)
        accelerations.append(acceleration)
        positions.append(position)
        velocities.append(velocity)

        plot_graphs(accelerations, positions, velocities, time_points, car_image=car_image)

        if position > 150:
            messagebox.showinfo("Game Over", "Position exceeded 150 meters.")
            plt.ioff()
            break

        if velocity > max_velocity:
            messagebox.showinfo("Game Over", "Exceeded maximum velocity.")
            plt.ioff()
            return

    plt.ioff()
    score = calculate_score(positions, velocities, total_time)
    messagebox.showinfo("Game Result", f"Final Score: {score}")


# GUI Setup
root = tk.Tk()
root.withdraw()  # Hide the main window
show_instructions()  # Show game instructions
start_game()