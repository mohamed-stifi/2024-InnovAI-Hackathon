# First Implementation Overview

## Overview

The initial approach involves adapting a single PC to act as a **subscriber**, which receives data from senders (publishers). This architecture allows video frames to be received over the UDP protocol and processed for display and AI analysis.

### Conception of the First Implementation

![Conception of the first implementation](../../images/1%20implementation.jpg)

This diagram illustrates the flow of data within the system. Specifically:

- The **VideoReceiver** class receives data in the form of frames via the UDP protocol.
- Data is received on predefined ports, and each port receives its respective frames.
- AI processing is then applied to the frames, and the processed video is displayed.

### How To Use This:
This part demonstrates how to stream video from a **publisher** (sending video frames over UDP) to a **subscriber** (receiving and processing the video). The publisher sends video data over multiple ports, and the subscriber receives and processes the video on those ports using the YOLOv5 model for object detection.

#### Requirements

Before running the code, ensure that you have the following Python libraries installed:

- OpenCV: `opencv-python`
- Numpy: `numpy`
- PyTorch: `torch`
- YOLOv5 model from `ultralytics`
- Optionally, `master.py` (if part of a larger application)

You can install the required packages with:

```bash
pip install opencv-python numpy torch
```

#### How to Run

##### 1. Running the Publisher

The **publisher** will be run on multiple terminals, each sending video data to the **subscriber** over a different UDP port. In each terminal, use the following steps:

###### Step 1: Open Multiple Terminals

You can run the **publisher** in as many terminals as you want. For example, if you want to stream video on three different ports (5001, 5002, and 5003), you need to open three separate terminals.

###### Step 2: Run the Publisher on Each Terminal

In each terminal, run the `publisherUDP.py` script with the desired port:

```bash
python publisherUDP.py
```

The publisher will send the video data from the default webcam (or another video source) to the specified receiver's IP address and port.

- In the example, the receiver is set to `localhost`, but you can change this to the IP address of the **subscriber**.
- The default port for the publisher is 5001, but you can adjust it in the `sender.py` script as needed.

Example for running the publisher on three terminals:

- **Terminal 1**:
  ```bash
  python publisherUDP.py
  ```

- **Terminal 2**:
  ```bash
  python publisherUDP.py
  ```

- **Terminal 3**:
  ```bash
  python publisherUDP.py
  ```

Each terminal will be sending video data to the **subscriber** on different ports (`5001`, `5002`, and `5003` in this case).

##### 2. Running the Subscriber

The **subscriber** will receive the video data sent from the **publisher** and process it using YOLOv5 for object detection.

###### Step 1: Open a Terminal for the Subscriber

You only need one terminal to run the **subscriber**.

###### Step 2: Run the Subscriber Script

In the subscriber terminal, run the `subscriberUDP.py` script:

```bash
python subscriberUDP.py
```

The **subscriber** will listen on multiple ports (e.g., `5001`, `5002`, and `5003` in this case), receive video frames sent by the **publisher**, and process the frames for object detection.

##### Customizing the IP and Ports

- You can change the IP and port configurations in both the **publisher** and **subscriber** scripts. By default, the **subscriber** listens on `localhost` (`0.0.0.0`) on ports `5001`, `5002`, and `5003`.
- The **publisher** sends video to the **subscriber** at the configured `receiver_ip` (by default `localhost`) and port (`5001` by default).

### Diagram: UML Diagram of VideoReceiver Architecture

![UML Diagram of VideoReceiver Architecture](../../images/video%20receiver%20v1.jpg)

This UML diagram provides a detailed overview of the architecture of the **VideoReceiverV1** class. It showcases the key relationships and methods that make the class functional.

### `VideoReceiverV1` Class Breakdown

The `VideoReceiverV1` class is the heart of the implementation. It interacts with several external modules, such as `uml_fiddle` (`SubscriberUDP.py`) and external package (like: `cv2',..), to achieve its functionality.

#### Attributes:
- `chunk_size`: Specifies the size of data chunks to be received in video transmission.
- `listen_ip`: The IP address on which the video data will be received.
- `ports`: A list of port numbers where the video data will be received.
- `sockets`: A list of socket objects used for network communication.

#### Methods:
- `__init__()`: The constructor method initializes the `VideoReceiverV1` object. It sets up the necessary parameters, such as `chunk_size`, `listen_ip`, and `ports`.
- `receive_video()`: This method is responsible for receiving video data from the specified `listen_ip` and `ports`. It uses the sockets to establish connections and retrieve video data in chunks.
- `receive_video_from_port()`: A helper function used by `receive_video()` to receive video data from a specific port.


### Diagram: UML Diagram of VideoSender Architecture

![UML Diagram of VideoSender Architecture](../../images/uml%20video%20sender.jpg)

This diagram further explains the architecture of the **VideoSender** class and its components, providing a detailed view of how the class interacts with the socket and manages the video data transmission.

The **VideoSender** class is designed to send video data to a recipient over a network connection.

#### Attributes:
- `chunk_size`: Specifies the size of the data chunks that will be sent during the video transmission.
- `port`: The port number on which the video data will be sent.
- `receiver_ip`: The IP address of the recipient (the subscriber or **VideoReceiver**).
- `socket`: This attribute holds a reference to a `socket` object, which is responsible for the network communication between the publisher and the receiver.

#### Methods:
- `__init__()`: The constructor method initializes the **VideoSender** object and sets up necessary parameters such as `chunk_size`, `port`, and `receiver_ip`.
- `send_video()`: This method sends the video data to the specified `receiver_ip` and `port`. It uses the `socket` object to establish the connection and transmit the video data in chunks.

