from velocity import *
from density import Density

def create_input(density: list, velocity: list, cmap="", filename=""):
    """Creates an input file with the Density, Velocity and Colormap given.
    The file is created in Config folder.

    Args:
        density (list): The list of Density objects that the input will have.
        velocity (list): The list of Velocity objects that the input will have.
        cmap (str, optional): The name of the Colormap that the input will have. Defaults to "".
        filename (str, optional): The name of the file to be read without the extension. Defaults to "".
    """
    if not cmap: cmap = "None"
    text = f"colormap={cmap}\n"

    text += f"density={len(density)}\n"
    for den in density:
        text += f"{den.to_string()}\n"

    text += f"velocity={len(velocity)}\n"
    for vel in velocity:
        text += f"{vel.to_string()}\n"
    
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
                Velocity(20, 40, 5, 5, VelocityAnimation.ROTATE_CW, 5)
            ]

create_input(density, velocity, cmap="Paired", filename="Config1")