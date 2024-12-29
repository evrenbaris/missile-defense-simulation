import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Simulation parameters
time_step = 0.1
simulation_time = 20

# Initial positions
missile_pos = np.array([0, 0])
target_pos = np.array([100, 50])

# Speeds
missile_speed = 5
target_speed = 1

# Flare parameters
flare_active = False
flare_pos = None
flare_probability = 0.3

# Lists for paths
missile_path = [missile_pos.copy()]
target_path = [target_pos.copy()]

# Target zigzag movement
def move_target(position, step, direction):
    new_position = position + np.array([step, direction * step])
    if new_position[1] > 60 or new_position[1] < 40:  # Change direction
        direction *= -1
    return new_position, direction

# Missile homing with flares
def move_missile(missile, target, speed, flare_pos=None, flare_active=False):
    if flare_active and flare_pos is not None:
        target = flare_pos  # Lock onto the flare
    direction = target - missile
    norm = np.linalg.norm(direction)
    if norm == 0:
        return missile
    return missile + (direction / norm) * speed

# Simulation loop
fig, ax = plt.subplots()
ax.set_xlim(-10, 120)
ax.set_ylim(-10, 80)

missile_line, = ax.plot([], [], 'r-', label="Missile Path")
target_line, = ax.plot([], [], 'b-', label="Target Path")
flare_point, = ax.plot([], [], 'go', label="Flare", markersize=10)
missile_point, = ax.plot([], [], 'ro', label="Missile")
target_point, = ax.plot([], [], 'bo', label="Target")

direction = 1
time = 0

def update(frame):
    global missile_pos, target_pos, flare_pos, flare_active, direction, time

    # Move the target
    target_pos, direction = move_target(target_pos, target_speed * time_step, direction)
    target_path.append(target_pos.copy())

    # Activate flare randomly
    if not flare_active and np.random.random() < 0.1:
        flare_active = True
        flare_pos = target_pos + np.array([np.random.uniform(-5, 5), np.random.uniform(-5, 5)])

    # Move the missile
    missile_pos = move_missile(
        missile_pos,
        target_pos,
        missile_speed * time_step,
        flare_pos=flare_pos,
        flare_active=flare_active,
    )
    missile_path.append(missile_pos.copy())

    # Deactivate flare after being used
    if flare_active and np.linalg.norm(missile_pos - flare_pos) < 5:
        flare_active = False

    # Update visualization
    missile_line.set_data(*zip(*missile_path))
    target_line.set_data(*zip(*target_path))
    missile_point.set_data(*missile_pos)
    target_point.set_data(*target_pos)
    if flare_active:
        flare_point.set_data(*flare_pos)
    else:
        flare_point.set_data([], [])

    time += time_step
    return missile_line, target_line, missile_point, target_point, flare_point

ani = FuncAnimation(fig, update, frames=int(simulation_time / time_step), interval=50, blit=True)

plt.legend()
plt.title("Missile Defense Simulation")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid()

# Display the animation inline in Colab
HTML(ani.to_jshtml())
