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
    The animation is separated into two possible rotations depending on whether the direction adds the rotation vector (Clockwise) or it substracts it (Counter-Clockwise).
### Return Animation
    This animation moves back and forth the position of the velocity depending on the axis selected.
    The animation creates a variable to check how many steps the animation has taken, this is used to create the moving loop.


## Create Multiple Sources of Velocity and Density

## Create Color Schemas

## Simulate Presence of Objects