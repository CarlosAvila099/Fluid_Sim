from typing import List
from velocity import *
from fluid import Fluid

CMAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']

def read_input(filename=""):
    """Reads input from a txt file. If none is given, lets the user enter a name.

    Args:
        filename (str, optional): The name of the file to be read. Defaults to "".

    Returns:
        [str, list, list]
            str: String of the colormap written.
            list: List of densities.
            list: List of velocities.
    """
    if not filename:
        print("The filename must be a txt file and within the same folder as the python file.")
        filename = input("Enter the filename without extension (default Input): ") or "Input"

    file = open(filename + ".txt", "r")
    lines = file.read().split("\n")
    densities = []
    velocities = []
    colormap = ""
    current = ""
    length = 0
    for line in lines:
        if "colormap" in line:
            colormap = line.split("=")[1]
        elif "density" in line:
            length = int(line.split("=")[1])
            current = "density"
        elif "velocity" in line:
            length = int(line.split("=")[1])
            current = "velocity"
        elif length > 0:
            length -= 1
            if current == "density": densities.append(line)
            elif current == "velocity": velocities.append(line)
    file.close()

    vel_array = []
    for vel in velocities:
        info = vel.split(", ")
        animation_value = 0

        pos_x = int(info[0])
        pos_y = int(info[1])
        strength_x = int(info[2])
        strength_y = int(info[3])
        animation = VelocityAnimation(int(info[4]))
        if animation in [VelocityAnimation.ROTATE_CW, VelocityAnimation.ROTATE_CCW, VelocityAnimation.RETURN_X, VelocityAnimation.RETURN_Y]:
            animation_value = int(info[5])

        temp_vel = Velocity(pos_x, pos_y, strength_x, strength_y, animation, animation_value)
        vel_array.append(temp_vel)

    return colormap, densities, vel_array

def create_from_input(fluid: Fluid, filename=""):
    """Adds densities and velocities to a fluid from an input file.

    Args:
        fluid (Fluid): The fluid to be modified.
        filename (str, optional): The name of the file to be read. Defaults to "".

    Returns:
        [str, list, list]
            str: Name of the Colormap to be used.
            list: List of densities.
            list: List of velocities.
    """
    cmap, densities, velocities = read_input(filename)
    colormap = choose_color(cmap)

    maintain_step(fluid, densities, velocities)

    return colormap, densities, velocities

def choose_color(color_name=""):
    """Gets the Colormap from the name given, if none is given, lets the user choose one.

    Args:
        color_name (str, optional): The name of the Colormap. Defaults to "".
            See also: https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html

    Returns:
        str: Name of Colormap to be used.
    """
    if color_name:
        for color in CMAPS:
            if color_name.lower() == color.lower(): color_name = color
    else:
        defaults = ["viridis", "Wistia", "winter"]
        print("1. Purple to yellow")
        print("2. Yellow to orange")
        print("3. Blue to green")
        while True:
            color = int(input("Choose a color (default 1): ") or 1)
            if color in [1, 2, 3]: break
        color_name = defaults[color - 1]
    return color_name

def add_density(fluid: Fluid, pos_x: int, pos_y: int, size_x: int, size_y: int, density=100):
    """Adds a density to the fluid given.

    Args:
        fluid (Fluid): The fluid that will be modified.
        pos_x (int): The x position of the density to be added.
        pos_y (int): The y position of the density to be added.
        size_x (int): The width of the density to be added.
        size_y (int): The height of the density to be added.
        density (int, optional): The density value. Defaults to 100.
    """
    fluid.density[pos_y:pos_y + size_y, pos_x:pos_x + size_x] += density

def add_velocity(fluid: Fluid, velocity: Velocity):
    """Adds a velocity to the fluid given

    Args:
        fluid (Fluid): The fluid that will be modified.
        velocity (Velocity): The velocity that will be added.
    """
    fluid.velo[velocity.pos_y, velocity.pos_x] = velocity.get_dir()

def maintain_step(fluid: Fluid, densities: list, velocities: list):
    """Adds all the densities and velocities given to the fluid. The velocities suffer a step.

    Args:
        fluid (Fluid): The fluid to be modified.
        densities (list): The list of densities to be added.
        velocities (list): The list of velocities to be added.
    """
    for den in densities:
        info = den.split(", ")
        pos_x = int(info[0])
        pos_y = int(info[1])
        size_x = int(info[2])
        size_y = int(info[3])
        density = float(info[4])
        add_density(fluid, pos_x, pos_y, size_x, size_y, density)
    
    for vel in velocities:
        add_velocity(fluid, vel)
        vel.step()