"""Image storage for persisting generated images."""
import os
import json
from datetime import datetime
from typing import Optional


class ImageStorage:
    """Handle persistent storage of generated images."""
    
    def __init__(self, storage_dir: str = "generated_images"):
        """
        Initialize image storage.
        
        Args:
            storage_dir: Directory path for storing images
        """
        self.storage_dir = storage_dir
        self.metadata_file = os.path.join(storage_dir, "metadata.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_image(
        self,
        image_bytes: bytes,
        sender_id: int,
        receiver_id: int,
        style: str,
        image_type: str = "combined"
    ) -> str:
        """
        Save a generated image to storage.
        
        Args:
            image_bytes: The image data as bytes
            sender_id: Telegram user ID of the sender
            receiver_id: Telegram user ID of the receiver
            style: The style that was applied
            image_type: Type of image (combined, original, transformed)
            
        Returns:
            Path to the saved image file
        """
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_sender{sender_id}_receiver{receiver_id}_{image_type}.png"
        filepath = os.path.join(self.storage_dir, filename)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Save metadata
        self._save_metadata(filename, sender_id, receiver_id, style, image_type)
        
        return filepath
    
    def _save_metadata(
        self,
        filename: str,
        sender_id: int,
        receiver_id: int,
        style: str,
        image_type: str
    ) -> None:
        """
        Save metadata about the generated image.
        
        Args:
            filename: Name of the saved image file
            sender_id: Telegram user ID of the sender
            receiver_id: Telegram user ID of the receiver
            style: The style that was applied
            image_type: Type of image
        """
        # Load existing metadata
        metadata = self._load_metadata()
        
        # Add new entry
        entry = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "style": style,
            "image_type": image_type
        }
        
        metadata.append(entry)
        
        # Save updated metadata
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _load_metadata(self) -> list:
        """
        Load metadata from file.
        
        Returns:
            List of metadata entries
        """
        if not os.path.exists(self.metadata_file):
            return []
        
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_stats(self) -> dict:
        """
        Get statistics about stored images.
        
        Returns:
            Dictionary with statistics
        """
        metadata = self._load_metadata()
        
        return {
            "total_images": len(metadata),
            "unique_senders": len(set(entry["sender_id"] for entry in metadata)),
            "unique_receivers": len(set(entry["receiver_id"] for entry in metadata)),
            "styles_used": list(set(entry["style"] for entry in metadata))
        }

