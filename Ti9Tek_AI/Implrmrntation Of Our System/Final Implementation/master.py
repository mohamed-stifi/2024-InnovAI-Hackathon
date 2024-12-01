import socket
import threading
import xmlrpc.server
import base64
import queue
import time
from collections import defaultdict
import cv2
import numpy as np

class UnifiedServer:
    def __init__(self, listen_ip='0.0.0.0', ports=[5001, 5002], chunk_size=8192):
        # Video reception
        self.listen_ip = listen_ip
        self.ports = ports
        self.chunk_size = chunk_size
        self.sockets = []
        self.task_queue = queue.Queue()

        # Task management
        self.tasks = []
        self.task_status = {}  # Maps task_id -> (status, start_time, worker)
        self.workers = set()
        self.results = defaultdict(list)
        self.lock = threading.Lock()

        # Initialize sockets for video reception
        for port in self.ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.listen_ip, port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            self.sockets.append(sock)
            print(f"Socket bound to port {port}")

    # Video Reception
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
                    # print(f"Received data on port {port}: {len(data)} bytes")
                    np_data = np.frombuffer(data, dtype=np.uint8)

                    if np_data.size > 0:
                        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

                        if frame is not None:
                            _, buffer = cv2.imencode('.jpg', frame)
                            encoded_frame = base64.b64encode(buffer).decode('utf-8')
                            task = {'port': port, 'encoded_frame': encoded_frame}
                            self.add_task(task)
                            
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

    # Task Management
    def add_task(self, task):
        with self.lock:
            task_id = len(self.tasks)
            self.tasks.append(task)
            self.task_status[task_id] = ("PENDING", None, None)
            print(f"Task {task_id} added from port {task['port']}")

    def register_worker(self, worker_address):
        with self.lock:
            self.workers.add(worker_address)
            print(f"Worker {worker_address} registered.")
        return True

    def request_task(self, worker_address):
        with self.lock:
            for task_id, (status, _, _) in self.task_status.items():
                if status == "PENDING":
                    self.task_status[task_id] = ("IN_PROGRESS", time.time(), worker_address)
                    return task_id, self.tasks[task_id]
        return None, None

    def complete_task(self, task_id, worker_address, result):
        with self.lock:
            if task_id in self.task_status:
                self.task_status[task_id] = ("COMPLETED", None, worker_address)
                port = result['port']
                encoded_frame = result['encoded_result']
                self.results[port].append(encoded_frame)
                print(f"Task {task_id} completed by {worker_address}")
        return True

    def monitor_tasks(self):
        while True:
            with self.lock:
                for task_id, (status, start_time, worker) in self.task_status.items():
                    if status == "IN_PROGRESS" and time.time() - start_time > 10:
                        self.task_status[task_id] = ("PENDING", None, None)
                        print(f"Task {task_id} timed out. Reassigning...")
            time.sleep(5)

    def get_results(self, port):
        with self.lock:
            return self.results.get(port, [])

    # Unified Server Start
    def start_server(self):
        # Start UDP threads
        for idx, sock in enumerate(self.sockets):
            thread = threading.Thread(target=self.receive_video_from_port, args=(sock, self.ports[idx]))
            thread.daemon = True
            thread.start()

        # Start XML-RPC server
        server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
        server.register_instance(self)
        print("Unified Server started (UDP + XML-RPC)...")

        # Start task monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_tasks)
        monitor_thread.daemon = True
        monitor_thread.start()

        # Serve XML-RPC requests
        server.serve_forever()

# Start the Unified Server
if __name__ == "__main__":
    unified_server = UnifiedServer(ports=[5001])
    unified_server.start_server()
