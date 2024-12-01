# Second Implementation Overview

## Overview

This architecture provides a scalable and efficient solution for distributed video processing. The master server coordinates task distribution, while worker clients handle the actual processing. The video receiver acts as a central hub for video data, and the video sender captures and transmits video streams.

# Conception of the Second Implementation
We aimed to make the process more efficient and avoid unnecessary delays by restructuring the server system.

![Conception of the Second implementation](../../images/2%20implementation.jpg)

Components:

- **VideoSender**: Captures video frames and transmits them to the VideoReceiver using UDP.
![UML Diagram of VideoSender Architecture](../../images/uml%20video%20sender.jpg)

Attributes:

chunk_size: Defines the size of data chunks.
listen_ip: The IP address for incoming connections.
master_ip: The IP address of the master server.
master_address: The address of the master server.
ports: A list of listening ports.
sockets: A list of socket objects.
queue_thread: A thread for managing the task queue.
task_queue: A queue for storing tasks or video frames.
Methods:

__init__(): Initializes attributes and sets up the receiver.
process_queue(): Processes tasks from the queue.
receive_video(): Receives video data from the network.
receive_video_from_port(): Receives video data from a specific port.



- **VideoReceiver**: Receives video frames from the VideoSender and distributes them to multiple worker clients via XML-RPC.

![UML Diagram of VideoReceiver Architecture](../../images/video%20receiver.jpg)

Attributes:
- **chunk_size:** Likely defines the size of data chunks to be received.
- **listen_ip:** The IP address on which the receiver listens for incoming connections.
- **master_ip:** The IP address of the master server (possibly for coordination or control).
- **master_address:** The address of the master server (likely a combination of IP and port).
- **ports:** A list of ports on which the receiver listens.
- **sockets:** A list of socket objects used for network communication.
- **queue_thread:** A reference to a thread responsible for managing a queue.
- **task_queue:** A reference to a queue used to store tasks or video frames to be processed.

Methods:
- **init():** The constructor, likely initializes the attributes and sets up the receiver.
- **process_queue():** Processes tasks or video frames from the task queue.
- **receive_video():** Receives video data from the network.



- **Worker Clients**: Process received video frames using AI algorithms to detect target behaviors and trigger notifications.
![UML Diagram of WorkerClient Architecture](../../images/uml%20worker%20client.jpg)

This class diagram suggests a distributed system where multiple worker
clients are managed by a master server. The WorkerClient class represents an individual
worker that can receive tasks from the master server via XML-RPC. The ServerProxy object
is used to communicate with the master server and send/receive data. The time class might
be used for various purposes, such as measuring task execution time or synchronizing with the
master server.

Attributes:
- **master:** A reference to the master server (likely an XML-RPC server).
- **worker address:** The address of the worker client itself (IP address and port number).

Methods:
- **init():** The constructor, likely initializes the attributes and sets up the worker client.
- **perform task():** Performs a task assigned by the master server.
- **start():** Starts the worker client, possibly by creating a thread to handle tasks.


- **Master Server**: Oversees the entire system, coordinates communication, and distributes tasks among worker clients.
![UML Diagram of MasterServer Architecture](../../images/uml%20master.jpg)

1. Initialization:
- **Data structures** to manage tasks, their statuses, worker addresses, and results.
- **A lock** for thread safety to ensure concurrent access to shared resources.

2. Task Management:
- **add task:** Adds a new task to the task queue, assigns a unique ID, and marks its status as "PENDING".
- **add tasks:** Adds multiple tasks to the queue.
- **request task:** Retrieves a pending task from the queue and assigns it to a worker, marking its status as "IN PROGRESS". If no pending tasks are available, it returns None.
- **complete task:** Marks a task as completed, stores the result, and prints a completion message.
- **monitor tasks:** Periodically checks for tasks that have been in progress for too long and reassigns them as pending.

3. Worker Management:
- **register worker:** Registers the address of a worker client with the master server.

4. Result Retrieval:
- **get results:** Retrieves a list of completed tasks and their results for a specific worker port.

5. Server Setup:
- **start master:**
  - Creates an XML-RPC server on port 8000.
  - Initializes a `MasterServer` object.
  - Registers the `MasterServer`’s methods with the XML-RPC server, making them accessible to remote calls.
  - Starts a monitoring thread to periodically check the task queue.
  - Starts the server to listen for incoming RPC requests.

6. Overall Functionality:
- The `MasterServer` acts as a central coordinator for a distributed system. It receives tasks, distributes them to worker clients, monitors their progress, and collects results.
- The XML-RPC interface allows worker clients to communicate with the master server and request tasks.
- The `monitor tasks` function ensures that tasks are not stuck in the "IN PROGRESS" state for too long, preventing potential deadlocks or resource leaks.
- In essence, this code provides a framework for managing distributed tasks, ensuring efficient resource utilization and timely task completion.



# How To Use This:
## 1. Setting Up the System

### Multiple Publishers:
- On each computer where you want to run a publisher, start the `publisher.py` script, specifying the IP address or hostname of the video receiver and the port to use for communication.

### Video Receiver:
- On the machine designated as the video receiver, start the `video_receiver.py` script. This script can run on the same machine as the master server or a separate one.

### Master Server:
- On the machine designated as the master server, start the `master.py` script.

### Multiple Worker Clients:
- On each computer where you want to run a worker client, start the `worker.py` script, specifying the IP address or hostname of the master server.

## 2. Running the System

1. Start the publishers on their respective machines.
2. Start the video receiver on its designated machine.
3. Start the master server on its designated machine.
4. Start the worker clients on their respective machines.

## 3. Video Streaming

1. The publishers will start capturing video streams and sending them to the video receiver.
2. The video receiver will receive the video streams from multiple publishers on different ports.
3. The video receiver will queue the video frames for processing.
4. The master server will distribute processing tasks (e.g., video frames) to available worker clients.
5. Each worker client will receive a task, process the video frame (e.g., object detection in this example), and send the results back to the master server.
6. The master server will store the results for each port and potentially send them back to the video receiver for display or further processing (not implemented in this example).

## 4. Customization

### Video Processing:
- You can modify the `worker.py` script to implement different video processing algorithms or tasks.

### Communication Protocol:
- The current implementation uses UDP for communication. You can explore alternative protocols like TCP or a message queueing system for different network requirements or reliability needs.

### Scalability:
- The architecture can be scaled by adding additional publishers, video receivers, worker clients, or master servers as needed.
