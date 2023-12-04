# 129L Project
## Proposal 

The double pendulum is a classic example in physics that showcases chaotic behavior. This system consists of two simple pendulums connected in series, and its motion is highly sensitive to initial conditions. By simulating a double pendulum computationally, we can gain insights into chaotic dynamics and explore the fascinating world of classical mechanics. 
  
In this project, I will implement the equations of motion for a double pendulum using numerical integration methods, simulate and visualize the motion of the double pendulum in 2D or 3D space to investigate the chaotic behavior by varying initial conditions and observing trajectory changes. I can also analyze and visualize the energy evolution of the double pendulum over time. I can start with the analytical classical equations of motion, then numerically implement them in Python and solve and graph them numerically. It should be possible to generate the motion as a video, and analyze the effect of small perturbations on the system. 

This problem is interesting because it falls into the field of chaos theory, and thus is very hard to demonstrate not only analytically, but even experimentally. The differential equations of motion are nonlinear, and the impact of human error on physical trials is much greater than normal in chaotic systems. Being able to see the impact of even slight parameters on the double pendulum in ideal conditions would be quite interesting. 

## Milestones
### Milestone 1 (11/17/2023)
I've done the basics. I have a simple python code that plays out the animation of a double pendulum, which should be in this repository under "Week 1 Basics".

I'm still thinking about in which way I want to take this. I'm thinking I explore the differing effects of different initial conditions, and maybe finding a metric in which I can track the pendulum's divergence from a normal mode. 

### Milestone 2 (11/24/2023)
I've been fighting my code in PyCharm, trying to plot two different pendulums on top of each other with slightly different initial conditions. I also am trying to simulate the triple pendulum. I want to also see if I can trace out the motion of the pendulum.

I've been fighting errors for the past few hours. I'll have the code in the repository by tomorrow (11/25) hopefully. 

### Milestone 3 (12/2/2023)
I wrote a script that lets me compare two different pendulums and see the error between them. I've generalized the motion of the pendulum to fit into a function. I think I will finish by plotting the distance between the ends of the pendulum against the difference in initial conditions. I'll have a bunch of different scripts and images done in the next few days. I'll add all my plots to the presentation as well. 
https://docs.google.com/presentation/d/1ImTKsA4iOFMFbpgbganmPuCq_QyqLenp_ltUcJIkXCs/edit?usp=sharing 
