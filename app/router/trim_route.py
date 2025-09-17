from fastapi import APIRouter, File, UploadFile, Form, HTTPException
import os
import uuid
from typing import Optional
import base64
from app.services import ImageProcessorService

# Create router for trim endpoint
trim_route = APIRouter()

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

# '/image/trim' route
@trim_route.post("/trim")
async def trim(
    file: UploadFile = File(...),
    resize_width: Optional[int] = Form(None),
    resize_height: Optional[int] = Form(None),
    quality: Optional[int] = Form(0)
):
    """
    Trim whitespace from image and optionally resize.
    
    Parameters:
    - file: Image file to process
    - resize_width: Target width (height auto-calculated to maintain aspect ratio)
    - resize_height: Target height (width auto-calculated to maintain aspect ratio)
    - quality: Quality level (1-100)
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.png', '.jpg', '.jpeg', '.webp']:
        raise HTTPException(status_code=400, detail="Unsupported image format")
    
    unique_id = str(uuid.uuid4())
    input_filename = f"{unique_id}_input{file_extension}"
    output_filename = f"{unique_id}_trimmed{file_extension}"
    
    input_path = os.path.join(STORAGE_DIR, input_filename)
    output_path = os.path.join(STORAGE_DIR, output_filename)
    
    try:
        # Save uploaded file
        with open(input_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process image using reusable service
        processing_result = ImageProcessorService.process_image(
            input_path=input_path,
            output_path=output_path,
            trim=True,
            resize_width=resize_width,
            resize_height=resize_height,
            quality=quality
        )
        
        # Read processed image and convert to base64
        with open(output_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        # Clean up files
        os.remove(input_path)
        os.remove(output_path)
        
        # Return response
        return {
            "file_format": processing_result['file_format'],
            "img_base64": img_base64,
        }
        
    except Exception as e:
        # Clean up files on error
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
            
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")
