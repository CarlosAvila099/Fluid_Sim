# Development Log
## Tasks
For this project, we were given a functional fluid simulator and we needed to add 4 principal parts.
* Create multiple sources of velocity and density, via command line or file.
* Animate velocity forces, there must be 2 behaviors.
* Create color schemas for the simulation.
* Simulate presence of objects in the simulation.

## Animate Velocity Forces
For this part of the simulation I created a Velocity class to make it easier for me to represent the things needed to animate the velocities. Then I added the animations I thought of: Rotation and Return.
### Rotation Animation
I simply rotated the direction of the velocity depending on the angle given.
The animation is separated into two possible rotations depending on whether the direction adds the rotation vector (Clockwise) or it
substracts it (Counter-Clockwise).
### Return Animation
This animation moves back and forth the position of the velocity depending on the axis selected.
The animation creates a variable to check how many steps the animation has taken, this is used to create the moving loop.

## Create Multiple Sources of Velocity and Density
For this part I needed to create the way to read the velocities and densities, while making the functions to modify the fluid with the multiple velocities and densities.
After creating read_input() I modified the density array and the velocities array from the fluid.
Then I created a way for this new densities and velocities to mantain throughout the simulation, so maintain_step() came to be.

## Create Color Schemas
After adding all the velocities and densities I started to investigate how to change color schemas for the animation, my solution was to use the Colormaps that matplotlib already has.
I only needed to make it a possible variable for the input, this was already solved when I added multiple velocities and densities, so it wasn't a problem.
The user can change the animation [https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html](Colormap) and the [https://matplotlib.org/stable/tutorials/colors/colors.html](Quiver Color).


## Simulate Presence of Objects