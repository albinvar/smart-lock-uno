<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/albinvar/smart-lock-uno">
    <img src="https://i.ibb.co/h2HFdvT/3824032-removebg-preview.png" alt="Logo" width="260" height="260">
  </a>
  
  <h3 align="center">Multi-Level Authentication Smart Lock</h3>

  <p align="center">
    A smart lock system with facial recognition, RFID authentication, and web API control using Arduino Uno and Python
    <br />
    <br />
    <img src="https://img.shields.io/packagist/v/albinvar/smart-lock-uno?label=version">
    <img src="https://poser.pugx.org/albinvar/smart-lock-uno/downloads">
    <a href="https://github.com/albinvar/smart-lock-uno/actions/workflows/tests.yml">
          <img src="https://github.com/albinvar/smart-lock-uno/actions/workflows/tests.yml/badge.svg"></a>
    <img src="https://img.shields.io/github/repo-size/albinvar/smart-lock-uno">
    <a href="LICENSE"><img src="https://img.shields.io/apm/l/Github"></a>
    <br />
    <a href="https://github.com/albinvar/smart-lock-uno"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/albinvar/smart-lock-uno">View Demo</a>
    ·
    <a href="https://github.com/albinvar/smart-lock-uno/issues">Report Bug</a>
    ·
    <a href="https://github.com/albinvar/smart-lock-uno/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Smart Lock Uno is a versatile and reliable prototype for a secure access control system. Built with Arduino Uno and Python. With its modular design and open-source code, Smart Lock Uno provides a starting point for young innovators  to build their own customized access control solutions. Smart Lock Uno offers a flexible and affordable way to manage access control.

This project is an open source implementation of a smart lock that allows users to unlock a door using three different authentication methods: 

- Facial Recognition  👦🏻
- RFID Authentication  💳
- Authentication through a Web API 🌐

The project uses an **Arduino Uno R3 microcontroller** and various electronic components to control a 12V solenoid lock.

## Requirements

To use this project, you will need the following components:

#### Hardware

- Arduino Uno R3 microcontroller
- 12 V solenoid lock
- 3.3 V RFID reader
- Jumper Wires
- Laptop with webcam and internet connectivity
- 5 V single channel relay

#### Software

- Python v3.0
- Pip

## Features

Three different authentication methods: facial recognition, RFID authentication, and authentication through a web API

- Uses a laptop's webcam / external webcam for facial recognition to cut down on costs.
- Trains facial recognition model using OpenCV Python.
- Handles all processing tasks directly from the laptop to minimize the load on the Arduino board.
- Uses Flask framework to connect the Arduino to the internet for web API authentication.
- Three authentication programs are split into separate threads to achieve concurrency.
- Sends signals to the Arduino board to unlock the solenoid lock for 10 seconds upon successful identification/authentication.
- Uses a 5V relay to power the 12V solenoid lock.

## Explanation

The project aims in demonstrating a simple multi-level authentication smart lock which can be implemented at low cost while maintaining simplicity, efficiency & readability. The primary aim of this project is to lock/unlock a **solenoid lock**  by the 3 authentication methods mentioned above.

The project uses certain hardwares & softwares to achieve the desired outcome.

The project can be splitted into 5 parts :

	- Backend Part (Python)
	- Ardiuno Board Program (Ardiuno Sketch)
	- Web API (Flask Api - Python)
	- Front End Web Application (Nuxt Js or Laravel & Livewire)
	- Android App (sketchware)

### Facial Recognition

The facial recognition feature of the Smart Lock Uno is powered by the **OpenCV Python library**. It trains a machine learning model to recognize faces from images captured and stored in the configured directory. The recommended location to store images of authorized users is the `faces` directory located in the root folder. It is recommended to store images of each authorized user in separate folders with their name as the directory name.

The program utilizes the `haarcascade_frontalface_default.xml` pre-trained classifier which contains a set of features that are used to detect frontal faces in each frame. This helps in detecting faces in real-time while minimizing hardware costs as the program uses your laptop's or external webcam for facial recognition. The program can recognize multiple faces and provide access to authorized users based on the trained data stored at `trainer.yml`. Configurations such as threshold values can be adjusted in the `config.py` file.

The **Local Binary Patterns Histograms (LBPH)** algorithm is used to extract features from images or frames. The algorithm analyzes the texture of an image and identifies local binary patterns that are then used to form a histogram. The histogram is a representation of the distribution of binary patterns in the image/frame and helps identify unique features in a person's face. LBPH is a great choice for facial recognition as it is relatively easy to implement and can achieve good results with minimal computational resources.

In case an unauthorized person stands in front of the camera for too long, they are considered an intruder. The frame from the camera is extracted and stored in the` intruders` folder which can be accessed through the web API. The delay for taking unauthorized person's frames can be adjusted in the `config.py` file.

```
.
├── 📂 faces 👦🏻
│   ├── 📂 John Doe
│   │   ├─── img1.jpg
│   │   ├─── img2.jpg
│   │   └─── ...
│   ├── 📂 Dave
│   │   ├─── img1.jpg
│   │   ├─── img2.jpg
│   │   └─── ...
│   └── ...
├── 📂 intruders 🧛
│   ├── intruder1.jpg
│   ├── intruder2.jpg
│   └── ...
├── 📂 models ⚙️
│   └── trainer.yml
├── haarcascade_frontalface_default.xml
├── config.py
├── main.py
├── train.py
└── ...
```
> PS : The directories mentioned above won't be present soon after installing the project. You may need to create it manually or it will be created upon execution.

## Installation

To use this project, you will need the following components:

- Arduino Uno R3 microcontroller
- 12V solenoid lock
- 3.3V RFID reader
- 5V LCD display
- Laptop with webcam and internet connectivity
- 5V channel relay

### Follow these steps to set up the project:

- Connect the Arduino board to your laptop via USB port
- Connect the 12V solenoid lock to a 5V 4 channel relay, and connect the relay to the - - Arduino board
- Connect the 3.3V RFID reader to the Arduino board
- Connect the 5V LCD display to the Arduino board
- Clone the GitHub repository and open the project in your preferred IDE
- Install the required libraries and dependencies, which are listed in the requirements.txt file
- Run the main.py file to start the authentication programs

## Contributing

This project is open source and contributions are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgments

This project was inspired by various smart lock projects available on the internet
Thanks to OpenCV Python and Flask for providing the tools necessary for facial recognition and web API authentication, respectively
Thanks to the Arduino community for providing helpful resources and support for this project.
