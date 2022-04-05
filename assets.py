from typing import List
from density import Density
from velocity import *
from fluid import Fluid

CMAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']

def read_input(filename=""):
    """Reads input from a txt file. If none is given, lets the user enter a name.

    Args:
        filename (str, optional): The name of the file to be read without the extension. Defaults to "".

    Returns:
        [str, list, list]
            str: String of the Colormap written.
            list: List of Density objects.
            list: List of Velocity objects.
    """
    if not filename:
        print("The filename must be a txt file and within the same folder as the python file.")
        filename = input("Enter the filename without extension (default Input): ") or "Input"

    file = open(filename + ".txt", "r")
    lines = file.read().split("\n")
    den_array = []
    vel_array = []
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
            if current == "density": den_array.append(line)
            elif current == "velocity": vel_array.append(line)
    file.close()

    densities = []
    for den in den_array:
        info = den.split(", ")
        pos_x = int(info[0])
        pos_y = int(info[1])
        size_x = int(info[2])
        size_y = int(info[3])
        density = int(info[4])
        temp_den = Density(pos_x, pos_y, size_x, size_y, density)
        densities.append(temp_den)

    velocities = []
    for vel in vel_array:
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
        velocities.append(temp_vel)

    return colormap, densities, velocities

def create_from_input(fluid: Fluid, filename=""):
    """Adds Density and Velocity to a Fluid from an input file.

    Args:
        fluid (Fluid): The Fluid object to be modified.
        filename (str, optional): The name of the file to be read without the extension. Defaults to "".

    Returns:
        [str, list, list]
            str: Name of the Colormap to be used.
            list: List of Density objects.
            list: List of Velocity objects.
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
    if color_name and not color_name == "None":
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

def add_density(fluid: Fluid, density: Density):
    """Adds a Density to the Fluid given.

    Args:
        fluid (Fluid): The Fluid object that will be modified.
        density (Density): The Density object that will be added.
    """
    fluid.density[density.pos_y:density.pos_y + density.size_y, density.pos_x:density.pos_x + density.size_x] += density.density

def add_velocity(fluid: Fluid, velocity: Velocity):
    """Adds a Velocity to the Fluid given

    Args:
        fluid (Fluid): The Fluid object that will be modified.
        velocity (Velocity): The Velocity object that will be added.
    """
    fluid.velo[velocity.pos_y, velocity.pos_x] = velocity.get_dir()

def maintain_step(fluid: Fluid, densities: list, velocities: list):
    """Adds all the Density and Velocity given to the Fluid. The Velocity suffer a step.

    Args:
        fluid (Fluid): The Fluid to be modified.
        densities (list): The list of Density objects to be added.
        velocities (list): The list of Velocity objects to be added.
    """
    for den in densities:
        add_density(fluid, den)
    
    for vel in velocities:
        add_velocity(fluid, vel)
        vel.step()