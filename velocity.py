from enum import Enum
import numpy as np

class VelocityAnimation(Enum):
    """Enum class to represent possible VelocityAnimations.

    Type:
        NORMAL: Stays the same through all the animation.
        ROTATE_CW: Rotates in a clockwise manner.
        ROTATE_CCW: Rotates in a counter-clockwise manner.
        RETURN_X: Moves back and forth in the x axis.
        RETURN_Y: Moves back and forth in the y axis.
    """
    NORMAL = 1
    ROTATE_CW = 2
    ROTATE_CCW = 3
    RETURN_X = 4
    RETURN_Y = 5

    def __int__(self):
        """Convertion to int.

        Returns:
            int: Value of enum in int.
        """
        return self.value

class Velocity:
    """Represents a velocity in the fluid simulation.
    """
    def __init__(self, pos_x: int, pos_y: int, strength_x: int, strength_y: int, animation=VelocityAnimation.NORMAL, animation_value=0):
        """Creates a Velocity object.

        Args:
            pos_x (int): The x position of the Velocity.
            pos_y (int): The y position of the Velocity.
            strength_x (int): The strength of the Velocity in the x vector.
            strength_y (int): The strength of the Velocity in the y vector.
            animation (VelocityAnimation, optional): Type of VelocityAnimation. Defaults to VelocityAnimation.NORMAL.
            animation_value (int, optional): Animation Value. Defaults to 0.
                Rotations: Angle in degrees of rotation per step.
                Return: Range of movement.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.strength_x = strength_x
        self.strength_y = strength_y
        self.__dir_x = self.strength_x
        self.__dir_y = self.strength_y

        if animation not in [VelocityAnimation.ROTATE_CW, VelocityAnimation.ROTATE_CCW, VelocityAnimation.RETURN_X, VelocityAnimation.RETURN_Y]: animation = VelocityAnimation.NORMAL
        self.__animation = animation

        self.__rotation = 0
        self.__current_rot = 0

        self.__length = 0
        self.__current_length = 0
        self.__step = 1

        if self.__animation in [VelocityAnimation.ROTATE_CW, VelocityAnimation.ROTATE_CCW]: self.__rotation = animation_value
        elif self.__animation in [VelocityAnimation.RETURN_X, VelocityAnimation.RETURN_Y]: self.__length = animation_value

    def __rotate(self):
        """Rotates the Velocity as the animation dictates.
        """
        if self.__animation == VelocityAnimation.ROTATE_CW: self.__current_rot += np.deg2rad(self.__rotation)
        elif self.__animation == VelocityAnimation.ROTATE_CCW: self.__current_rot -= np.deg2rad(self.__rotation)

        self.__dir_x = self.strength_x * np.cos(self.__current_rot)
        self.__dir_y = self.strength_y * np.sin(self.__current_rot)

    def __return(self):
        """Moves the position of the Velocity as the animation dictates.
        """
        if abs(self.__current_length) >= self.__length: self.__step *= -1
        self.__current_length += self.__step

        if self.__animation == VelocityAnimation.RETURN_X: self.pos_x += self.__current_length
        elif self.__animation == VelocityAnimation.RETURN_Y: self.pos_y += self.__current_length

    def get_dir(self):
        """Returns the resulting direction of the Velocity.

        Returns:
            [float, float]
            float: The direction in the y axis of the Velocity.
            float: The direction in the x axis of the Velocity.
        """
        return [self.__dir_y, self.__dir_x]

    def step(self):
        """Modifies a vector of the Velocity depending on its animation.
        """
        if self.__animation in [VelocityAnimation.ROTATE_CW, VelocityAnimation.ROTATE_CCW]: self.__rotate()
        elif self.__animation in [VelocityAnimation.RETURN_X, VelocityAnimation.RETURN_Y]: self.__return()

    def to_string(self):
        """Makes a string containing all the values of a Velocity object.

        Returns:
            str: The string form of the Velocity object.
        """
        string = f"{self.pos_x}, {self.pos_y}, {self.strength_x}, {self.strength_y}, {int(self.__animation)}"
        if self.__animation in [VelocityAnimation.ROTATE_CW, VelocityAnimation.ROTATE_CCW]: string += f", {self.__rotation}"
        elif self.__animation in [VelocityAnimation.RETURN_X, VelocityAnimation.RETURN_Y]: string += f", {self.__length}"
        return string
        