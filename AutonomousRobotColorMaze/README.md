# Autonomous Robot Color Recognition

<img src="https://i.ibb.co/kBZ8fDj/Jeffrey.jpg" alt="Jeffrey" width="384" height="512">

## About The Project

Autonomous machine maze navigation using color recognition.<br><br>
Code utilizes GoPiGo's motors for motion, camera for taking frames and analyzing them for color content in a resized down image, and distance sensor to determine whether it is facing an object or wall. If the robot detects an object without target colors within a user-defined distance, it will stop. Otherwise, if it does detect a user set target color, it will take appropriate action listed below. Multiple threads are utilized for each color target for better performance. <br><br>
<b>Default Target Colors & Actions</b>
- Red: Turn Right
- Blue: Turn Left
- Yellow: Turn Around

### Built With

[Python](https://www.python.org/)

#### Libraries:

* [GoPiGo](https://gopigo.io/)

## Setup

1.) Obtain a GoPiGo robot kit from Dexter Industries.<br>
2.) Install DexterOS on a memory card.<br>
3.) While the OS is installing, assemble the robot using the instructions from the kit.<br>
4.) Download this directory's Jupyter Notebook file: `MazeNavigation.ipynb`.<br>
5.) Upload the file into the robot's file system.<br>
6.) Open the file and shift enter each cell in order to run the program.<br>
7.) Adjust the distance value `dist_value` in cell 3 under function `do_work` to determine distance from an object before the robot takes an action. There are two locations of `dist_value`, the first determines no detection of color in an object to stop, and the second determines color detection in an object.<br> 
8.) Adjust the `robot.drive_cm()` to however far you want the robot to drive each step it takes before analyzing the next queue of frames.<br>
9.) Adjust the colors `target_one, target_two, target_three` in cell 4 for desired RGB code color that you want the robot to detect.

## Contributing

<ol>
  <li> Fork the Project </li>
  <li> Create your Feature Branch  </li>
  <li> Commit your Changes  </li>
  <li> Push to the Branch  </li>
  <li> Open a Pull Request </li>
</ol>

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

William Jones - [LinkedIn](https://www.linkedin.com/in/william-jones-11180a210/) - will.jones11@hotmail.com <br>
Project Link: https://github.com/willjones11/CSC4120/AutonomousRobotColorRecognition


Danny Nguyen - [LinkedIn](https://www.linkedin.com/in/ndanny09/) - ndanny09@gmail.com <br>
Project Link: https://github.com/ndanny09/AutonomousRobotColorRecognition

## Acknowledgements

* [README Template](https://github.com/othneildrew/Best-README-Template#prerequisites)
