# Project Plan
[Docs][docs-url] -> Getting Started


Considering the difficulty of this project, we divided it into several projects, each building on the previous one. It's highly probable that we have yet to finish some of them, but again, this is a work in progress.

## Projects
1.  [Lane Detection](#Lane-Detection)  
2.  [Self-Driving using Lane Detection](#Self-Driving-using-Lane-Detection)  
3.  [Traffic signs detection](#Traffic-signs-detection)  
4.  [Obstacle detection](#Obstacle-detection)  

## Lane Detection
This project is the base project, its purpose it to build an integrated system with CARLA capable of retrieving a live video and display lane markings.

This project can also be divided into epics/milestones:
1.  Connecting with CARLA
2.  Getting Live feed from CARLA
3.  Apply Canny detector to detect edges
4.  Apply Gaussian filter to reduce noise
5.  Apply Sobel filter in the x and y axis to detect orientation of edges
6.  Apply Non-maximum suppression filter to sharpen edges
7.  Apply frequency threshold filter to consider low-intensity pixels that might be edges
8.  Segment lane area


## Self-Driving using Lane Detection

## Traffic signs detection

## Obstacle detection



[docs-url]: https://github.com/eamorgado/Car-Self-driving-Simulator/blob/main/README.md
