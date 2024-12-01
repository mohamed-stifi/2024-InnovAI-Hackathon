import cv2
import socket
import numpy as np
import time

class VideoSender:
    def __init__(self, receiver_ip, port, chunk_size=8192):
        self.receiver_ip = receiver_ip
        self.port = port
        self.chunk_size = chunk_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send_video(self, video_source=0):
        try:
            cap = cv2.VideoCapture(video_source)
            if not cap.isOpened():
                raise IOError("Cannot open video source")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Compress the image with reduced quality
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
                result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
                data = encoded_frame.tobytes()
                
                # Send the image in chunks via UDP
                for i in range(0, len(data), self.chunk_size):
                    chunk = data[i:i+self.chunk_size]
                    self.socket.sendto(chunk, (self.receiver_ip, self.port))
                
                # End of frame marker
                self.socket.sendto(b'END', (self.receiver_ip, self.port))

                # Optionally show the video locally
                cv2.imshow(f'Sending to {self.receiver_ip}:{self.port}...', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting video stream...")
                    break

                time.sleep(2)
        
        except Exception as e:
            print(f"Video streaming error: {e}")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.socket.close()

# Example usage
if __name__ == "__main__":
    ip = '10.1.6.133'
    sender = VideoSender(receiver_ip=ip, port=5001)  # Replace with the receiver's IP
    sender.send_video()