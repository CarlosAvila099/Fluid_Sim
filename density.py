class Density:
    """Represents a density in the fluid simulation.
    """
    def __init__(self, pos_x: int, pos_y: int, size_x: int, size_y: int, density=100):
        """Creates a Density object.

        Args:
            pos_x (int): The x position of the Density.
            pos_y (int): The y position of the Density.
            size_x (int): The width of the Density.
            size_y (int): The height of the Density.
            density (int, optional): The density value. Defaults to 100.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.density = density

    def __str__(self):
        """String conversion of a Density object.

        Returns:
            str: The string form of the Density object.
        """
        return f"{self.pos_x}, {self.pos_y}, {self.size_x}, {self.size_y}, {self.density}"

class Solid:
    """Represents a solid in the fluid simulation.
    """
    def __init__(self, pos_x: int, pos_y: int, size_x: int, size_y: int):
        """Creates a Solid object.

        Args:
            pos_x (int): The x position of the Solid.
            pos_y (int): The y position of the Solid.
            size_x (int): The width of the Solid.
            size_y (int): The height of the Solid.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def __str__(self):
        """String conversion of a Solid object.

        Returns:
            str: The string form of the Solid object.
        """
        return f"{self.pos_x}, {self.pos_y}, {self.size_x}, {self.size_y}"