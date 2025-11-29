"""Utilities for image processing."""
from PIL import Image
import io


def combine_images_side_by_side(original_bytes: bytes, edited_bytes: bytes) -> bytes:
    """
    Combine two images side by side.
    
    Args:
        original_bytes: Bytes of the original image
        edited_bytes: Bytes of the edited image
        
    Returns:
        Bytes of the combined image
    """
    # Open images
    original = Image.open(io.BytesIO(original_bytes))
    edited = Image.open(io.BytesIO(edited_bytes))
    
    # Convert to RGB if necessary (handles RGBA, etc.)
    if original.mode != 'RGB':
        original = original.convert('RGB')
    if edited.mode != 'RGB':
        edited = edited.convert('RGB')
    
    # Resize images to have the same height
    target_height = min(original.height, edited.height, 1024)  # Cap at 1024px
    
    # Calculate new widths maintaining aspect ratio
    original_width = int(original.width * target_height / original.height)
    edited_width = int(edited.width * target_height / edited.height)
    
    original = original.resize((original_width, target_height), Image.Resampling.LANCZOS)
    edited = edited.resize((edited_width, target_height), Image.Resampling.LANCZOS)
    
    # Create a new image with combined width
    combined_width = original_width + edited_width
    combined = Image.new('RGB', (combined_width, target_height))
    
    # Paste images side by side
    combined.paste(original, (0, 0))
    combined.paste(edited, (original_width, 0))
    
    # Convert to bytes
    output = io.BytesIO()
    combined.save(output, format='JPEG', quality=95)
    output.seek(0)
    
    return output.getvalue()

