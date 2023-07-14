# eyrc22_PB_1660 
## Introduction
In the modern age, ensuring efficient mobility solutions is crucial for a city's transformation into a "Smart" city. While home delivery has been widely adopted by various industries to enhance their services, it often relies on human labor and vehicles, leading to increased fuel consumption. This project tackles this challenge by proposing the development of autonomous delivery robot specifically designed for our "Smart city" environment. The robot will seamlessly navigate the city, retrieve the required packets from designated shops, and transport them to the correct locations based on customer requests. Moreover, it will consider various arena parameters such as traffic signals and road closures due to ongoing construction, ensuring efficient and obstacle-free delivery operations.

## Description
- Design of an autonomous bot capable of traversing a 5X5 grid representing a smart city.
- The grid consists of two parts: the first row represents five medical shops where medicine packages are stored, and the remaining rows represent the smart city where packages are delivered.Packages are differentiated by shape (Square, Triangle, Circle) and color (Sky Blue, Pink, Orange, Green). Each shop's packages have unique colors, and no two packages in a cell have the same color.
- Each node in the grid has a color representing start, traffic, or end nodes. Nodes are connected by black roads of length 5cm, but some nodes are not connected due to "Horizontal Roads Under Construction" and "Vertical Roads Under Construction."
- Drop-locations of packages are encrypted in QR codes placed at the PN (Package Node) of each shop(in coppeliasim scene).
- ___The physical arena consists only of the grid, and a layout of the arena is provided using an image for setting up the CoppeliaSim software.The CoppeliaSim scene includes representations of traffic signals, roads under construction, and packages, which can be enhanced by placing 3D models.___
- The live location and orientation of the robot are monitored using an ArUco marker placed on the robot.
- The virtual arena in CoppeliaSim should indicate package pick-up and delivery since the robot does not have a mechanism for it.

## Test Video
[![Final Video](https://img.youtube.com/vi/4wBZM202DNg/hqdefault.jpg)](https://www.youtube.com/watch?v=4wBZM202DNg)

## Robot Picture
![image](https://github.com/madmaverickminion/eyrc22_PB_1660/assets/88222914/34c63ae1-1b87-44d1-889e-396164d158d2)
![image](https://github.com/madmaverickminion/eyrc22_PB_1660/assets/88222914/6d06cc77-99bb-43e4-babd-e5dbeb728f28)




## Hardware used
- Raspberry pi
- AlphaBot Kit
- Web Camera and USB cable (for emulation)
- 18650 Batteries(4) and Battery Charger
- Jumper wires
- RBG LED(4)




