import tensorflow as tf
import numpy as np
from ultralytics import YOLO
from PIL import Image

cnn_model = tf.keras.models.load_model("./fracture_detection_model.keras")
yolo_model = YOLO("./best.pt")

def preprocess_image(img, img_height=180, img_width=180):
    img = img.convert("RGB") 
    img = img.resize((img_height, img_width))  
    img_array = np.array(img, dtype=np.float32) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)  
    return img_array
    
def predict_fracture(img):
    preprocessed_img = preprocess_image(img)        
    prediction = cnn_model.predict(preprocessed_img)
    class_names = ['fractured', 'not fractured']
    predicted_class = (prediction > 0.5).astype("int32")        
    return class_names[predicted_class[0][0]]

def localize_fracture(img_path):
    results = yolo_model(img_path, conf=0.1)  
    for result in results:
        img_with_boxes = result.plot()  
        return Image.fromarray(img_with_boxes) 
    return None  
