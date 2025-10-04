import base64
import io
import numpy as np
from PIL import Image
from app import model  # Import the loaded model from the app context
from config import img_width, img_height

def process_and_predict(base64_string: str) -> tuple[str, float]:
    """
    Decodes a base64 string, preprocesses the image, and returns the prediction.
    
    Args:
        base64_string: The image encoded as a Base64 string.
    
    Returns:
        A tuple containing the predicted label (str) and confidence (float).
    """
    # 1. Decode Base64 String
    # Remove the "data:image/jpeg;base64," prefix if it exists
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    image_bytes = base64.b64decode(base64_string)
    
    # 2. Open Image and Preprocess
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((img_width, img_height))
    img_array = np.array(img) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # 3. Predict with the Model
    prediction = model.predict(img_array)
    confidence = float(prediction[0][0])
    
    # 4. Determine Label
    label = 'male' if confidence > 0.5 else 'female'
    
    # Adjust confidence to be intuitive (e.g., for female, 0.1 -> 90% confidence)
    if label == 'female':
        confidence = 1 - confidence
        
    return label, confidence