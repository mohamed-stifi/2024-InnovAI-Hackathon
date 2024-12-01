import cv2
import socket
import numpy as np
import threading
import xmlrpc.server
import time
import base64
import queue


class VideoReceiver:
    def __init__(self,master_address, listen_ip='0.0.0.0', ports=[5001, 5002], chunk_size=8192):
        self.master = xmlrpc.client.ServerProxy(master_address)
        self.master_address = master_address
        self.listen_ip = listen_ip
        self.ports = ports
        self.task_queue = queue.Queue()
        
        # self.lock = threading.Lock()
        self.chunk_size = chunk_size
        self.sockets = []  # List to hold the sockets

        # Create and bind sockets for each port
        for port in self.ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.listen_ip, port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)  # Increase buffer size
            self.sockets.append(sock)
            print(f"Socket bound to port {port}")

        self.queue_thread = threading.Thread(target=self.process_queue)
        self.queue_thread.daemon = True
        self.queue_thread.start()


    def process_queue(self):
        print('process_queue')
        while True:
            task_data = self.task_queue.get()
            try:
                with xmlrpc.client.ServerProxy(self.master_address) as master_proxy:
                    task_id = master_proxy.add_task(task_data)
                    print(f"Task {task_id} sent to master")
            except Exception as e:
                print(f"Failed to send task to master: {e}")
            finally:
                self.task_queue.task_done()


    def receive_video_from_port(self, sock, port):
        # print(f"start receiving from port {port}")
        data = b''
        try:
            while True:
                while True:
                    chunk, addr = sock.recvfrom(self.chunk_size)
                    if chunk == b'END':  # End of frame signal
                        break
                    data += chunk

                if data:
                    # print(f"Received data on port {port}: {len(data)} bytes")
                    np_data = np.frombuffer(data, dtype=np.uint8)

                    if np_data.size > 0:
                        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

                        if frame is not None:
                            _, buffer = cv2.imencode('.jpg', frame)
                            encoded_frame = base64.b64encode(buffer).decode('utf-8')
                            task = {'port': port, 'encoded_frame': encoded_frame}
                            self.task_queue.put(task)
                            
                            # img_bgr = procecing(frame)
                            # cv2.imshow(f"Video from Port {port}", img_bgr)  # Display video in a window specific to the port
                            # if cv2.waitKey(1) & 0xFF == ord('q'):
                                # break
                        else:
                            print(f"Error: Could not decode frame on port {port}")
                    else:
                        print(f"Warning: Empty data received on port {port}")
                data = b''
        except Exception as e:
            print(f"Video receiving error on port {port}: {e}")
        finally:
            print(f"Closing socket on port {port}")
            sock.close()

    def display_video_of_port(self, port):
        while True:
            # for port in self.ports:
            # Check if results are empty
            try:
                # Fetch results for the port from the master

                results = self.master.get_results(port)
                for encoded_frame in results:
                    print("rescve results back")
                    decoded_frame = base64.b64decode(encoded_frame)
                    frame_array = np.frombuffer(decoded_frame, dtype=np.uint8)
                    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                    np_data = np.frombuffer(frame, dtype=np.uint8)
                    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
                    print(img)
                    if img is not None:
                        cv2.imshow(f"Video from Port {port}", img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            return
                    
                    results.pop(0)
            
            except Exception as e:
                print(f"Error fetching results for port {port}: {e}")
            time.sleep(1)

    def receive_video(self):
        # Create a thread for each socket to handle multiple ports concurrently
        threads = []
        for idx, sock in enumerate(self.sockets):
            thread = threading.Thread(target=self.receive_video_from_port, args=(sock, self.ports[idx]))
            threads.append(thread)
            thread.start()

        for port in self.ports:
            display_thread = threading.Thread(target=self.display_video_of_port, args=(port,))
            threads.append(display_thread)
            display_thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Cleanup
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    receiver = VideoReceiver(master_address = "http://localhost:8000", listen_ip='0.0.0.0', ports=[5001])  # Listen on both ports
    receiver.receive_video()
    