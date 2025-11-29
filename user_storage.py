"""User storage for persisting authorized users."""
import json
import os
from typing import Set


class UserStorage:
    """Handle persistent storage of authorized user IDs."""
    
    def __init__(self, storage_file: str = "authorized_users.json"):
        """
        Initialize user storage.
        
        Args:
            storage_file: Path to the JSON file for storing user IDs
        """
        self.storage_file = storage_file
    
    def load_users(self) -> Set[int]:
        """
        Load authorized user IDs from storage file.
        
        Returns:
            Set of user IDs
        """
        if not os.path.exists(self.storage_file):
            return set()
        
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return set(data.get('authorized_users', []))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading users from storage: {e}")
            return set()
    
    def save_users(self, user_ids: Set[int]) -> None:
        """
        Save authorized user IDs to storage file.
        
        Args:
            user_ids: Set of user IDs to save
        """
        try:
            data = {
                'authorized_users': list(user_ids)
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving users to storage: {e}")
    
    def add_user(self, user_id: int, current_users: Set[int]) -> Set[int]:
        """
        Add a user ID and save to storage.
        
        Args:
            user_id: User ID to add
            current_users: Current set of user IDs
            
        Returns:
            Updated set of user IDs
        """
        current_users.add(user_id)
        self.save_users(current_users)
        return current_users

