# Undergraduate Research with P. Pham
Spring 2025

### Computer Vision and Robotics

Our motivation this spring is to analyze plants growing, specifically from Evergreen's Organic Farm, based on images taken in a repeatable way from six-legged (hexapod) robot traveling close to the ground. We will build and program a shared Freenove Hexapod Robot controlled by a Raspberrry Pi in class.

Like our robot, we live and move around in a world of three dimensions, yet the sensors we most often connect to computers are two-dimensional: cameras.

Reconstructing a 3D object, such as a plant, large building exterior, or even a person from 2D images, uses an area of computer vision called *multiple view geometry* or *projective geometry*, specifically transformations between vector spaces that are usually encoded as matrices or tensors.

This is an experimental offering where we will be attempting to reproduce several challenging tasks from known research and existing curricula:
* Making a circuit for one, two, and three infrared "tape measure"s using an IR sensor and transmitter, we will  triangulate our robot's position and its images to geo-locate them on Google Earth
* Segmenting the foreground of an image (a plant) from the background (the environment) using OpenCV, for two different species
* Creating a 3D mesh of points from one, two, and three 2D images of the segmented foreground, that can be used to build a "digital twin" viewable on an a website
* Clustering these 3D mesh of points to build a classifier for distinguishing future plants encountered by our robot.

Linear algebra, Python programming, and using circuits with Raspberry Pi single-board computers are helpful, but they can also be learned as we go in this UGR. Just bring your curiosity and enjoyment of staring at math, typing lines of code, and bending wires.

This is a collaborative learning experience where we value helping each other and documenting what we learn to share with the world as an open source project.
#### Schedule

Monday 1-2:30pm LIB 2708 (Physical Computing Center)
Tuesday 1-2:30pm Lab II 2238 (Physics Lab)
#### Course Notes:

We will be following course notes from [Stanford's CS231a](https://web.stanford.edu/class/cs231a/course_notes.html)

and [Daniel Cremers video playlist](https://www.youtube.com/playlist?list=PLTBdjV_4f-EJn6udZ34tht9EVIW7lbeo4) 

Our goal will be to construct in Python using the OpenCV, Numpy, Pytorch, and other libraries, the mathematics from this course and the textbook below.

#### Textbooks:

Multiple View Geometry in Computer Vision  
Second Edition
Richard Hartley and Andrew Zisserman,  
Cambridge University Press, March 2004.
https://www.robots.ox.ac.uk/~vgg/hzbook/

Implementation of some of the MVG ideas in the Hartley-Zisserman book and some more recent 2012-2013 papers, in C++
https://github.com/openMVG/openMVG

A circuit for distance measuring with infrared diode + photoresistor using Arduino
https://www.alanzucconi.com/2015/10/14/how-to-build-a-distance-sensor-with-arduino/

### Credits:
Up to 6 upper division computer science awarded in *Computer Vision for Robotics*

 Students will be awarded credit for attendance and effort.
