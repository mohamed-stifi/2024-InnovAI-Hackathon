import cv2
import socket
import numpy as np
import threading
import torch
from master import MasterServer

# Load YOLOv5 model on CPU
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device='cpu')
model.conf = 0.4  # Increase confidence threshold


def procecing(frame):
    # Convert the image from BGR to RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Inference (detect objects)
    results = model(img_rgb)

    # Results: Draw bounding boxes on the image
    results.render()  # Adds bounding boxes to the image

    # Display the image with detections
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_bgr

class VideoReceiverV1:
    def __init__(self, listen_ip='0.0.0.0', ports=[5001, 5002], chunk_size=8192):
        self.listen_ip = listen_ip
        self.ports = ports
        self.chunk_size = chunk_size
        self.sockets = []  # List to hold the sockets

        # Create and bind sockets for each port
        for port in self.ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.listen_ip, port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)  # Increase buffer size
            self.sockets.append(sock)
            print(f"Socket bound to port {port}")

    def receive_video_from_port(self, sock, port):
        data = b''
        try:
            while True:
                while True:
                    chunk, addr = sock.recvfrom(self.chunk_size)
                    if chunk == b'END':  # End of frame signal
                        break
                    data += chunk

                if data:
                    print(f"Received data on port {port}: {len(data)} bytes")
                    np_data = np.frombuffer(data, dtype=np.uint8)

                    if np_data.size > 0:
                        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

                        if frame is not None:
                            img_bgr = procecing(frame)
                            cv2.imshow(f"Video from Port {port}", img_bgr)  # Display video in a window specific to the port
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        else:
                            print(f"Error: Could not decode frame on port {port}")
                    else:
                        print(f"Warning: Empty data received on port {port}")

                # Reset data for the next frame
                data = b''
        except Exception as e:
            print(f"Video receiving error on port {port}: {e}")
        finally:
            print(f"Closing socket on port {port}")
            sock.close()

    def receive_video(self):
        # Create a thread for each socket to handle multiple ports concurrently
        threads = []
        for idx, sock in enumerate(self.sockets):
            thread = threading.Thread(target=self.receive_video_from_port, args=(sock, self.ports[idx]))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Cleanup
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    receiver = VideoReceiverV1(listen_ip='0.0.0.0', ports=[5001, 5002, 5003])  # Listen on both ports
    receiver.receive_video()