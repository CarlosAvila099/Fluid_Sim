import sys
from density import *
from velocity import *
from fluid import Fluid

CMAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']

QCOLOR = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

def read_input(filename=""):
    """Reads input from a txt file. If none is given, lets the user enter a name.
    The file must be in Config folder.

    Args:
        filename (str, optional): The name of the file to be read without the extension. Defaults to "".

    Returns:
        [str, str, list, list, list]
            str: String of the Colormap written.
            str: String of the Quiver Color written.
            list: List of Density objects.
            list: List of Velocity objects.
            list: List of Solid objects.
    """
    if not filename:
        print("The filename must be a txt file and within the Config folder of the project.")
        filename = input("Enter the filename without extension (default Input): ") or "Input"

    try:
        file = open("Config/" + filename + ".txt", "r")
    except FileNotFoundError:
        print("The file was not found, please check the spelling of filename.")
        sys.exit()
    lines = file.read().split("\n")
    den_array = []
    vel_array = []
    sol_array = []
    colormap = ""
    qcolor = ""
    current = ""
    length = 0
    for line in lines:
        if "colormap" in line:
            colormap = line.split("=")[1]
        elif "quiver" in line:
            qcolor = line.split("=")[1]
        elif "density" in line:
            length = int(line.split("=")[1])
            current = "density"
        elif "velocity" in line:
            length = int(line.split("=")[1])
            current = "velocity"
        elif "solid" in line:
            length = int(line.split("=")[1])
            current = "solid"
        elif length > 0:
            length -= 1
            if current == "density": den_array.append(line)
            elif current == "velocity": vel_array.append(line)
            elif current == "solid": sol_array.append(line)
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
    
    solids = []
    for sol in sol_array:
        info = sol.split(", ")
        pos_x = int(info[0])
        pos_y = int(info[1])
        size_x = int(info[2])
        size_y = int(info[3])
        temp_sol = Solid(pos_x, pos_y, size_x, size_y)
        solids.append(temp_sol)

    return colormap, qcolor, densities, velocities, solids

def create_from_input(fluid: Fluid, filename=""):
    """Adds Density and Velocity to a Fluid from an input file.

    Args:
        fluid (Fluid): The Fluid object to be modified.
        filename (str, optional): The name of the file to be read without the extension. Defaults to "".

    Returns:
        [str, str, list, list]
            str: Name of the Colormap to be used.
            str: Name of the Quiver Color to be used.
            list: List of Density objects.
            list: List of Velocity objects.
    """
    cmap, qcolor, densities, velocities, solids = read_input(filename)
    colormap = choose_color(cmap)
    q_color = choose_quiver(qcolor)

    fluid.solid = solids
    maintain_step(fluid, densities, velocities, solids)

    return colormap, q_color, densities, velocities, solids

def choose_color(color_name=""):
    """Gets the Colormap from the name given, if none is given, lets the user choose one.

    Args:
        color_name (str, optional): The name of the Colormap. Defaults to "".
            See also: https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html

    Returns:
        str: Name of Colormap to be used.
    """
    color_map = ""
    if color_name and not color_name == "None":
        for color in CMAPS:
            if color_name.lower() == color.lower(): color_map = color
    if not color_map:
        defaults = ["Paired", "viridis", "bone"]
        print("1. Temperature Map")
        print("2. Purple to yellow")
        print("3. Blue to green")
        while True:
            color = int(input("Choose a color (default 1): ") or 1)
            if color in [1, 2, 3]: break
        color_map = defaults[color - 1]
    return color_map

def choose_quiver(color_name=""):
    """Gets the Quiver Color from the name given, if none is given, lets the user choose one.

    Args:
        color_name (str, optional): The name of the Color. Defaults to "".
            See also: https://matplotlib.org/stable/tutorials/colors/colors.html

    Returns:
        str: Name of Quiver Color to be used.
    """
    q_color = ""
    if color_name and not color_name == "None":
        for color in QCOLOR:
            if color_name.lower() == color.lower(): q_color = color
    if not q_color:
        defaults = ["k", "y", "w"]
        print("1. Black")
        print("2. Yellow")
        print("3. White")
        while True:
            color = int(input("Choose a color (default 1): ") or 1)
            if color in [1, 2, 3]: break
        q_color = defaults[color - 1]
    return q_color

def add_density(fluid: Fluid, density: Density):
    """Adds a Density to the Fluid given.

    Args:
        fluid (Fluid): The Fluid object that will be modified.
        density (Density): The Density object that will be added.
    """
    fluid.density[density.pos_y:density.pos_y + density.size_y, density.pos_x:density.pos_x + density.size_x] = density.density

def add_velocity(fluid: Fluid, velocity: Velocity):
    """Adds a Velocity to the Fluid given

    Args:
        fluid (Fluid): The Fluid object that will be modified.
        velocity (Velocity): The Velocity object that will be added.
    """
    fluid.velo[velocity.pos_y, velocity.pos_x] = velocity.get_dir()

def maintain_step(fluid: Fluid, densities: list, velocities: list, solids):
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

    for sol in solids:
        fluid.velo[sol.pos_y:sol.pos_y + sol.size_y, sol.pos_x:sol.pos_x + sol.size_x] = 0
        fluid.density[sol.pos_y:sol.pos_y + sol.size_y, sol.pos_x:sol.pos_x + sol.size_x] = 0