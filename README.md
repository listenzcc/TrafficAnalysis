# Traffic Analysis

The project will **construct** the Traffic Situations.

And several Analysis will be performed to **simulate** the traffic pressure under different conditions.

Last but not least, the **optimized** implementation of traffic situation will thus be proposed.

---
- [Traffic Analysis](#traffic-analysis)
  - [Overview](#overview)
  - [Details](#details)
    - [Traffic Situations Construction](#traffic-situations-construction)
    - [Traffic Pressure Simulation](#traffic-pressure-simulation)
    - [Optimized Implementation](#optimized-implementation)
  - [Developing Diary](#developing-diary)

## Overview

- Project Overview

![project](project.svg)

The Project contains `3` components as planned

- Traffic Situations Construction

   Construct traffic situations in graph manner.

- Traffic Pressure Simulation

   Simulate the traffic situation with a large number of cars.

- Optimized Implementation

    Evaluate and optimize the traffic situation based on the simulations.

## Details

### Traffic Situations Construction

### Traffic Pressure Simulation

### Optimized Implementation

## Developing Diary

- 2020-07-04
  - Initialize the project;
  - Build Initial Overview.

- 2020-07-05
  - Setup .vscode dot files;
  - Developed [random_layout.py](./Construction/random_layout.py "random_layout.py") V0.0, Randomly Set Nodes.

- 2020-07-06
  - Improve [settings.py](./settings.py "settings.py");
  - Developed [least_length.py](./RouteLayout/least_length.py "least_length.py") V0.0, Compute Least Length Route.

- 2020-07-07
  - Improve [least_length.py](./RouteLayout/least_length.py "least_length.py") to V0.1;
  - Added Graph Spectral Clustering method and Compute Distance in Graph Space.

- 2020-07-08
  - Developed [least_length_chinamap.py](./RouteLayout/least_length_chinamap.py "least_length_chinamap") V0.11;
  - It is a special Version for Explaining Spectral Clustering.

- 2020-07-09
  - Developed [least_length_superGraph.py](./RouteLayout/least_length_superGraph.py "least_length_superGraph") V0.0;
  - The Script is Developed based on [least_length.py](./RouteLayout/least_length.py "least_length.py") to V0.1;
  - It is used for Compute ShortCuts between Labels.

- 2020-07-10
  - Improved [settings.py](./settings.py "settings");
  - Add Overall Dumping and Loading Methods.

- 2020-07-11
  - Re-Organizing the Program;
  - The Process is Under-Going;
  - Until Now, the Global Part of the [utils](./RouteLayout/utils "utils") is Developed.