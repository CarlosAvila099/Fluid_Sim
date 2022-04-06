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
                Density(14, 14, 3, 3), 
                Density(45, 45, 1, 6),
                Density(0, 0, 4, 4),
                Density(30, 25, 7, 2),
                Density(30, 15, 3, 3)
            ]

velocity =  [
                Velocity(20, 40, 5, 5, VelocityAnimation.ROTATE_CW, 5),
                Velocity(30, 10, 0, 5, VelocityAnimation.RETURN_X, 5)
            ]

solid =     [
                Solid(30, 30, 10, 2)
            ]

create_input(density, velocity, solid, cmap="Paired", qcolor="k", filename="Config1")