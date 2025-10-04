"""
Script untuk mengkonversi gambar ke base64
Untuk testing API Gender Detection
"""

import base64
import os
import sys
from pathlib import Path

def image_to_base64(image_path):
    """
    Convert image file to base64 string
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        str: Base64 encoded string
    """
    try:
        with open(image_path, 'rb') as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_string
    except FileNotFoundError:
        print(f"Error: File not found - {image_path}")
        return None
    except Exception as e:
        print(f"Error converting image: {e}")
        return None

def save_base64_to_file(base64_string, output_file):
    """
    Save base64 string to text file
    
    Args:
        base64_string (str): Base64 encoded string
        output_file (str): Output file path
    """
    try:
        with open(output_file, 'w') as f:
            f.write(base64_string)
        print(f"Base64 saved to: {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

def generate_postman_json(base64_string, output_file):
    """
    Generate JSON file for Postman testing
    
    Args:
        base64_string (str): Base64 encoded string
        output_file (str): Output JSON file path
    """
    import json
    
    postman_data = {
        "image_data": base64_string
    }
    
    try:
        with open(output_file, 'w') as f:
            json.dump(postman_data, f, indent=2)
        print(f"Postman JSON saved to: {output_file}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def display_sample_curl_command(base64_string):
    """
    Display sample cURL command for testing
    
    Args:
        base64_string (str): Base64 encoded string
    """
    # Truncate base64 for display
    display_base64 = base64_string[:50] + "..." if len(base64_string) > 50 else base64_string
    
    curl_command = f'''
Sample cURL Command:
------------------------
curl -X POST http://localhost:5000/api/predict \\
  -H "Content-Type: application/json" \\
  -d '{{
    "image_data": "{display_base64}"
  }}'

Full cURL Command (copy this):
curl -X POST http://localhost:5000/api/predict -H "Content-Type: application/json" -d '{{"image_data": "{base64_string}"}}'
'''
    print(curl_command)

def main():
    print("="*60)
    print("Image to Base64 Converter for API Testing")
    print("="*60)
    
    # Get image path from user
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to image file: ").strip().strip('"')
    
    if not image_path:
        print("No image path provided")
        return
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return
    
    print(f"Processing image: {image_path}")
    
    # Convert to base64
    base64_string = image_to_base64(image_path)
    
    if not base64_string:
        return
    
    print(f"Image converted successfully!")
    print(f"Base64 length: {len(base64_string)} characters")
    
    # Create output directory
    output_dir = "test_outputs"
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate filename based on input image
    image_name = Path(image_path).stem
    
    # Save outputs
    base64_file = f"{output_dir}/{image_name}_base64.txt"
    json_file = f"{output_dir}/{image_name}.json"
    
    save_base64_to_file(base64_string, base64_file)
    generate_postman_json(base64_string, json_file)
    
    # Display sample commands
    display_sample_curl_command(base64_string)
    
    # Show first 100 characters of base64
    print(f"\nFirst 100 characters of base64:")
    print(f"   {base64_string[:100]}...")
    
    print("\nTesting Options:")
    print(f"   1. Copy base64 from: {base64_file}")
    print(f"   2. Import JSON in Postman: {json_file}")
    print(f"   3. Use cURL command shown above")
    
    print("\nHappy Testing!")

if __name__ == "__main__":
    main()