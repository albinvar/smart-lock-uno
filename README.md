# Smart Lock with Facial Recognition, RFID Authentication, and Web API

This project is an open source smart lock that allows users to unlock a door using three different authentication methods: 
- facial recognition
- RFID authentication 
- authentication through a web API 

The project uses an Arduino Uno R3 microcontroller and various electronic components to control a 12V solenoid lock and a 3.3V RFID reader.

## Features

Three different authentication methods: facial recognition, RFID authentication, and authentication through a web API

- Uses a laptop's webcam for facial recognition to cut down on costs
- Trains facial recognition model using OpenCV Python
- Handles all processing tasks directly from the laptop to minimize the load on the Arduino board
- Uses Flask framework to connect the Arduino to the internet for web API authentication
- Three authentication programs are split into separate threads to achieve concurrency
- Sends signals to the Arduino board to unlock the solenoid lock for 10 seconds upon successful identification/authentication
- Uses a 5V relay to power the 12V solenoid lock


## Installation

To use this project, you will need the following components:

- Arduino Uno R3 microcontroller
- 12V solenoid lock
- 3.3V RFID reader
- 5V LCD display
- Laptop with webcam and internet connectivity
- 5V channel relay

Follow these steps to set up the project:

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