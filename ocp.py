from screeninfo import get_monitors

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import numpy as np


# Function to get screen size in inches
def get_screen_size_inches():
    screen = get_monitors()[0]
    pixels_per_inch = 96  # Standard pixel density
    screen_width_inches = screen.width / pixels_per_inch
    screen_height_inches = screen.height / pixels_per_inch
    return screen_width_inches, screen_height_inches


# Function to update position and velocity
def update_position_velocity(position, velocity, acceleration, delta_time):
    new_velocity = velocity + acceleration * delta_time
    new_position = position + velocity * delta_time + 0.5 * acceleration * delta_time ** 2
    return new_position, new_velocity


# Function to update the graph and display the costand constraints
def update(val):
    final_time = time_slider.val
    delta_time = final_time / num_segments
    time_points = np.linspace(0, final_time, num_segments + 1)

    positions = [0]
    velocities = [0]
    accelerations = [slider.val for slider in sliders]
    velocity_exceeded = False

    for acc in accelerations:
        new_position, new_velocity = update_position_velocity(positions[-1], velocities[-1], acc, delta_time)
        positions.append(new_position)
        velocities.append(new_velocity)
        if new_velocity > max_velocity:
            velocity_exceeded = True

    ax_acc.clear()
    ax_vel.clear()
    ax_pos.clear()

    ax_acc.step(time_points, [0] + accelerations, where='mid')
    ax_vel.plot(time_points, velocities)
    ax_pos.plot(time_points, positions)

    # Add red zone for velocity
    for i in range(num_segments):
        if velocities[i] > max_velocity:
            ax_vel.fill_between([time_points[i], time_points[i + 1]], 0, max_velocity, color='red', alpha=0.3)

    # Add vertical dashed lines for intervals
    for t in time_points:
        ax_acc.axvline(x=t, color='grey', linestyle='--', lw=0.5)
        ax_vel.axvline(x=t, color='grey', linestyle='--', lw=0.5)
        ax_pos.axvline(x=t, color='grey', linestyle='--', lw=0.5)

    # Display final position and velocity
    ax_vel.text(time_points[-1], velocities[-1], f'{velocities[-1]:.2f} m/s', verticalalignment='bottom')
    ax_pos.text(time_points[-1], positions[-1], f'{positions[-1]:.2f} m', verticalalignment='bottom')

    ax_acc.set_ylabel('Acc (m/s²)')
    ax_vel.set_ylabel('Vel (m/s)')
    ax_pos.set_ylabel('Pos (m)')
    ax_pos.set_xlabel('Time (s)')

    ax_vel.axhline(y=max_velocity, color='r', linestyle='--')  # Max Velocity Line
    ax_pos.axhline(y=150, color='r', linestyle='--')  # Target Position

    position_error = abs(150 - positions[-1])
    velocity_error = abs(velocities[-1])
    title_text = f'Cost: {final_time:.2f} s, Pos Error: {position_error:.2f}, Vel Error: {velocity_error:.2f}'
    title_color = 'green' if not velocity_exceeded and position_error == 0 and velocity_error == 0 else 'red'
    title_text += ', Velocity Exceeded!' if velocity_exceeded else ''
    fig.suptitle(title_text, fontsize=16, color=title_color)
    fig.canvas.draw_idle()


# Parameters
num_segments = 10
max_velocity = 23
initial_final_time = 12
max_acceleration = 5
min_acceleration = -7

# Getscreen size and calculate figsize
screen_width_inches, screen_height_inches = get_screen_size_inches()
fig_proportion = 0.5  # Use 50% of the screen size
figsize = (screen_width_inches * fig_proportion, screen_height_inches * fig_proportion / 3)

# Create the figure withproportional figsize
fig, (ax_acc, ax_vel, ax_pos) = plt.subplots(1, 3, figsize=figsize)
plt.subplots_adjust(bottom=0.45, top=0.85)

# Create Acceleration Sliders
slider_axes = [plt.axes([0.1, 0.05 + 0.03 * i, 0.8, 0.02], facecolor='lightgoldenrodyellow') for i in
               range(num_segments)]
sliders = [Slider(ax, f'acc_{i + 1}', min_acceleration, max_acceleration, valinit=0) for i, ax in enumerate(slider_axes)]

# Create Final Time Slider
time_slider_ax = plt.axes([0.1, 0.02, 0.8, 0.02], facecolor='lightgoldenrodyellow')
time_slider = Slider(time_slider_ax, 'Final Time', 8, 20, valinit=initial_final_time)

# Set up the update callback function for each slider
for slider in sliders:
    slider.on_changed(update)
    time_slider.on_changed(update)

# Initialize the graph
update(None)

plt.show()