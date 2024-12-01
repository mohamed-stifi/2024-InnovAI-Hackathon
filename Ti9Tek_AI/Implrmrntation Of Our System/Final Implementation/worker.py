import xmlrpc.client
import time
import cv2
import torch
import base64
import numpy as np
from utils import *
from PIL import Image
from whatsapp_send import *
from transformers import DetrImageProcessor, DetrForObjectDetection  # Hugging Face library

# Load DETR model from Hugging Face's transformers library
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
model.eval()

class WorkerClient:
    def __init__(self, master_address):
        self.master = xmlrpc.client.ServerProxy(master_address, allow_none=True)
        self.worker_address = f"Worker-{time.time()}"
        self.master.register_worker(self.worker_address)

    def perform_task(self, task):
        encoded_frame = task['encoded_frame']
        port = task['port']

        decoded_bytes = base64.b64decode(encoded_frame)

        # Decode the bytes into an image
        frame = cv2.imdecode(np.frombuffer(decoded_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        frame_resized = cv2.resize(frame, (640, 480))  # Ensure consistent resolution
        img_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        # Convert the OpenCV image (numpy array) to a PIL Image
        img_pil = Image.fromarray(img_rgb)

        # Apply the processor to the PIL image to get model input
        inputs = processor(images=img_pil, return_tensors="pt")
        outputs = model(**inputs)

        # Post-processing to get predicted boxes
        target_sizes = torch.tensor([frame_resized.shape[:2]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        # Draw bounding boxes
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            # Convert box to proper coordinates
            x_min, y_min, x_max, y_max = box
            label = CLASSES[int(label)]
            confidence = float(score)

            text = f"Class {label} ({confidence:.2f})"
            print(text)

            # Optional: You can draw the boxes on the image
            # cv2.rectangle(frame_resized, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            # cv2.putText(frame_resized, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            numero_telephone = "+212644054404"
            if label in interessingClass:
                print(f"we shold send to whatsApp {label} to number {numero_telephone}")
                send_message_via_whatsapp(numero_telephone, f"Class {label} ({confidence:.2f})")

        return {
            'port': port,
            'encoded_result': None,  # Return None for encoded result
        }

    def start(self):
        while True:
            task_id, task = self.master.request_task(self.worker_address)
            if task_id is not None:
                print(f"{self.worker_address} received task {task_id}")
                result = self.perform_task(task)
                self.master.complete_task(task_id, self.worker_address, result)
            else:
                print(f"{self.worker_address} has no tasks, sleeping...")
                time.sleep(2)  # Sleep before checking again

# Start Worker
def start_worker():
    worker = WorkerClient("http://localhost:8000")
    worker.start()

# XML-RPC Server to handle the worker tasks
def start_server():
    # Enable allow_none=True to handle None values on the server side
    server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
    print("Server started on port 8000")
    
    # Register the task-handling methods and other necessary functions
    server.register_instance(WorkerClient("http://localhost:8000"))
    
    # Start the server
    server.serve_forever()

if __name__ == "__main__":
    # You can choose to run the server or worker depending on your needs
    # start_server()  # Uncomment to run the server
    start_worker()  # Uncomment to run the worker
