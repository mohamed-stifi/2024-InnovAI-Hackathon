
# IoT-AI in a Distributed System

## Overview 
First, you will see a series of cameras placed in the area to monitor the environment. These cameras act as video transmitters. to capture live video feed Video frames are sent to a central component called UnifiedServer

UnifiedServer plays an important role, taking incoming video data and distributing it as tasks to Multiple WorkerClients Each WorkerClient has AI processing capabilities.

Now WorkerClients These analyze video frames using AI algorithms to detect specific targeted behaviors. For example, if a system is designed to detect suspicious activities, AI will identify those activities during processing.

Once a target behavior is detected, the relevant WorkerClient sends an alert via a platform such as WhatsApp to alert the relevant team or individual in real time.

This distributed system leverages multiple workers to ensure efficient video processing. and provide immediate notification for better investigation and quick response.

# Conception of the Final Implementation

![Conception of the Final implementation](../../images/final%20implementation.jpg)

This project implements a distributed system for real-time video streaming, processing, and object detection using IoT and AI technologies. The architecture integrates three main components: a **Master Server**, a **Video Publisher**, and multiple **Worker Nodes**. These components work together seamlessly to capture, distribute, and analyze video data in a scalable, distributed manner. 

The system also includes an automation feature to send alerts via WhatsApp when specific objects are detected in the video stream.

---

## Folder Structure
```
Final Implementation/
│
├── master.py           # Core server script managing tasks and video streams.
├── publisher.py        # Publishes video streams to the server.
├── worker_fc.py        # Worker script to process tasks from the server.
├── whatsapp_send.py    # Automates WhatsApp messaging for detected objects.
└── README.txt          # Detailed project description and setup guide.
```

---

## Components Description

### 1. **Master Server (`master.py`)**  
- **Purpose**: Acts as the central server responsible for receiving video streams, assigning tasks to workers, and collecting results.  
- **Key Features**:  
   - Receives video frames via UDP on specified ports.  
   - Implements task scheduling and load balancing for workers using a queue.  
   - Monitors worker status and task progress, reassigning tasks if necessary.  
   - Provides an XML-RPC interface for workers to request tasks and send results.  
   
- **How it Works**:  
   - The server listens on designated ports for incoming video frames, decodes them, and creates tasks.  
   - Workers request tasks from the server, process video frames (e.g., object detection), and return the results.  
   - Results are stored and can be retrieved for further analysis.

---

### 2. **Video Publisher (`publisher.py`)**  
- **Purpose**: Captures video from a source (e.g., webcam or file) and sends it to the Master Server via UDP.  
- **Key Features**:  
   - Captures video frames in real-time using OpenCV.  
   - Compresses frames for efficient transmission.  
   - Sends frames in chunks to the Master Server.  
   
- **How it Works**:  
   - The script captures frames, compresses them to reduce size, and sends them to the server over UDP.  
   - It includes an optional local display of the video stream for debugging purposes.  

---

### 3. **Worker Nodes (`worker_fc.py`)**  
- **Purpose**: Processes tasks from the Master Server (e.g., performs object detection using AI models).  
- **Key Features**:  
   - Implements an XML-RPC client to communicate with the Master Server.  
   - Performs AI-based object detection using a pre-trained DETR (DEtection TRansformer) model from Hugging Face.  
   - Sends alerts via WhatsApp when specific objects of interest are detected.  
   
- **How it Works**:  
   - The worker requests tasks from the server, processes the video frames, and identifies objects.  
   - Alerts are sent using the `whatsapp_send.py` script for predefined objects of interest.  

---

### 4. **WhatsApp Messaging (`whatsapp_send.py`)**  
- **Purpose**: Automates the sending of WhatsApp messages for alerts.  
- **Key Features**:  
   - Uses the `pywhatkit` library for WhatsApp Web integration.  
   - Automates mouse and keyboard interactions using `pynput` to ensure message delivery.  
   
- **How it Works**:  
   - A detected object of interest triggers the `send_message_via_whatsapp` function, which schedules a message via WhatsApp Web.  
   - The message is sent to a predefined phone number with object details.

---

## Setup and Installation

### Prerequisites  
1. **Python 3.8+**  
2. Required libraries:  
   - `opencv-python`  
   - `numpy`  
   - `xmlrpc`  
   - `torch`  
   - `transformers`  
   - `pywhatkit`  
   - `pynput`  

   Install them using:  
   ```bash
   pip install opencv-python numpy torch transformers pywhatkit pynput
   ```

3. **Hugging Face Model**: Ensure you have an internet connection to download the DETR model the first time it runs.  

### Setup Steps  
1. Clone the repository:  
   ```bash
   git clone copy_repo_url
   cd repo_name
   ```

2. Start the Master Server:  
   ```bash
   python master.py
   ```

3. Start the Video Publisher:  
   ```bash
   python publisher.py
   ```

4. Start one or more Worker Nodes (multiple worker in multi terminals or computers):  
   ```bash
   python worker_fc.py
   ```

---

## How to Run the Project
1. Start the **Master Server** (`master.py`) to initialize task management and video reception.  
2. Run the **Video Publisher** (`publisher.py`) to stream video to the server.  
3. Execute one or more **Worker Nodes** (`worker_fc.py`) to process tasks.  
4. Monitor the output on the console to see task assignments and detection results.  
5. Observe WhatsApp alerts triggered by specific object detections.

---

## Example Workflow

### Scenario: Detecting a person and sending an alert  
1. A video is streamed from `publisher.py` to the Master Server.  
2. The server creates tasks for each frame and assigns them to available workers.  
3. Workers process the frames using the DETR model and identify objects.  
4. If a "person" is detected, the worker triggers a WhatsApp message alert to a predefined phone number.  
5. The message includes the detected object’s label and confidence score.

---

## Output Samples

### Console Outputs
- **Master Server**:  
   ```
   Task 0 added from port 5001
   Received data on port 5001: 32042 bytes
   Task 1 added from port 5001
   ```

- **Worker Node**:  
   ```
   Worker-12345 received task 0
   Class: person (0.98)
   Sending WhatsApp alert: "Person detected with confidence 0.98"
   ```

- **WhatsApp Message**:  
   ```
   "ALERT: Detected 'Person' with confidence 0.98"
   ```

---

## Future Improvements
1. Add support for additional video sources and protocols (e.g., RTSP, HTTP).  
2. Enhance the task scheduling mechanism for dynamic load balancing.  
3. Expand AI models to detect a wider variety of objects.  
4. Implement a GUI to visualize results in real-time.

---