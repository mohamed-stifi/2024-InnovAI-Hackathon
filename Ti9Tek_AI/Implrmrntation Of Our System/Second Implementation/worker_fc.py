import xmlrpc.client
import time
import cv2
import torch
import xmlrpc.server
import time
import base64
import numpy as np
from PIL import Image
from utils import *
from whatsapp_send import send_message_via_whatsapp


# Load DETR model
model = torch.hub.load('facebookresearch/detr:main', 'detr_resnet50', pretrained=True)
model.eval()

class WorkerClient:
    def __init__(self, master_address):
        self.master = xmlrpc.client.ServerProxy(master_address)
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

        # Apply the transformation pipeline
        img = transform(img_pil).unsqueeze(0)  # Add batch dimension

        # Run inference
        outputs = model(img)
        probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > 0.9

        # Scale bounding boxes
        bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], frame_resized.shape[:2])


        # Draw bounding boxes
        for box, cls_prob in zip(bboxes_scaled, probas[keep]):
            # x_min, y_min, x_max, y_max = box.int().tolist()
            label = CLASSES[cls_prob.argmax().item()]
            confidence = cls_prob.max().item()

            # Draw box and label
            # cv2.rectangle(frame_resized, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            text = f"Class {label} ({confidence:.2f})"
            # cv2.putText(frame_resized, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            print(text)
            numero_telephone = "+212644054404"
            send_message_via_whatsapp(numero_telephone, text)

        return {
            'port': port,
            'encoded_result': None,  
        }
        # Display the image with detections
        # img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        # cv2.imshow(f"Video from Port {port} from worker", img_bgr)  # Display video in a window specific to the port
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     return img_bgr
        # return img_bgr


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

if __name__ == "__main__":
    start_worker()
