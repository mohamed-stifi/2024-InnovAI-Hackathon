# First Implementation Overview

## Overview

The initial approach involves adapting a single PC to act as a **subscriber**, which receives data from senders (publishers). This architecture allows video frames to be received over the UDP protocol and processed for display and AI analysis.

### Conception of the First Implementation

![Conception of the first implementation](../../images/1%20implementation.jpg)

This diagram illustrates the flow of data within the system. Specifically:

- The **VideoReceiver** class receives data in the form of frames via the UDP protocol.
- Data is received on predefined ports, and each port receives its respective frames.
- AI processing is then applied to the frames, and the processed video is displayed.

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

