import face_recognition
import math
import numpy as np
import base64
from io import BytesIO
from PIL import Image

def get_encoding_base64(base64_str: str):
    try:
        if base64_str.startswith('data:image/jpeg;base64,'):
            base64_str = base64_str.replace('data:image/jpeg;base64,', '')

        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)
        encodings = face_recognition.face_encodings(image_np)
        
        return encodings[0] if encodings else None
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None


def get_encoding(path: str):
    try:
        image = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(image)
        return encoding
    except:
        return None

def euclidean_distance(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must be of same length.")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

def compare(source: str, target: str) -> bool:
    results = face_recognition.compare_faces([source], target)
    return bool(results)

def compare_euclid(source: str, target:str):
    threshold = 0.55
    enc_source = get_encoding(source)
    enc_target = get_encoding(target)
    distance = euclidean_distance(enc_source, enc_target)

    return distance < threshold