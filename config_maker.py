from velocity import *
from density import *

def create_input(density: list, velocity: list, solid: list, cmap="", qcolor="", filename=""):
    """Creates an input file with the Density objects, Velocity objects, Solid objects, Colormap and Quiver Color given.
    The file is created in Config folder.

    Args:
        density (list): The list of Density objects that the input will have.
        velocity (list): The list of Velocity objects that the input will have.
        solid (list): The list of Solid objects that the input will have.
        cmap (str, optional): The name of the Colormap that the input will have. Defaults to "".
            See also: https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html
        qcolor (str, optional): The name of the Color that the Quiver will have. Defaults to "".
            See also: https://matplotlib.org/stable/tutorials/colors/colors.html
        filename (str, optional): The name of the file to be read without the extension. Defaults to "".
    """
    if not cmap: cmap = "None"
    text = f"colormap={cmap}\n"

    if not cmap: cmap = "None"
    text += f"quiver={qcolor}\n"

    text += f"density={len(density)}\n"
    for den in density:
        text += f"{den}\n"

    text += f"velocity={len(velocity)}\n"
    for vel in velocity:
        text += f"{vel}\n"
    
    text += f"solid={len(solid)}\n"
    for sol in solid:
        text += f"{sol}\n"
    
    text = text[:-1]

    file = open("Config/" + filename + ".txt", "w")
    file.write(text)
    file.close()
    print(f"The file has been saved as {filename}.txt in Config folder")
    

density =   [     
                Density(25, 25, 5, 5)
            ]

velocity =  [
                Velocity(25, 25, 3, 3, VelocityAnimation.ROTATE_CW, 5)
            ]

solid =     [
                Solid(10, 10, 30, 3),
                Solid(10, 40, 30, 3),
                Solid(10, 10, 3, 30),
                Solid(40, 10, 3, 30)
            ]

create_input(density, velocity, solid, cmap="bone", qcolor="y", filename="Config3")