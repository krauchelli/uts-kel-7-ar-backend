from flask import request, jsonify
from . import services

def handle_prediction():
    """
    Controller function to handle the prediction request.
    It orchestrates the process and includes error handling.
    """
    try:
        # 1. Validate incoming data
        data = request.get_json()
        if not data or 'image_data' not in data:
            # This will be caught by our 400 error handler
            raise ValueError("Missing 'image_data' in request body")
            
        image_data = data['image_data']

        # 2. Call the service to perform the core logic
        label, confidence = services.process_and_predict(image_data)
        
        # 3. Format the successful response
        response = {
            "success": True,
            "prediction": label,
            "confidence": confidence
        }
        return jsonify(response), 200

    except ValueError as e:
        # Re-raise as a generic exception to be caught by the 400 handler
        # In a real app, you might have custom exceptions
        raise e
    except Exception as e:
        # This will be caught by our 500 error handler
        # Log the detailed error for debugging
        print(f"An unexpected error occurred: {e}") 
        raise e