"""Save/load game state."""

import json
from pathlib import Path
from typing import Optional

from ..models.pet import Pet


class SaveManager:
    """Manages saving and loading game state."""
    
    def __init__(self, save_dir: Optional[Path] = None):
        """Initialize save manager."""
        if save_dir is None:
            save_dir = Path.home() / ".tamagocli"
        
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "save.json"
    
    def save(self, pet: Pet) -> bool:
        """
        Save pet state to file.
        
        Args:
            pet: Pet to save
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = pet.to_dict()
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def load(self) -> Optional[Pet]:
        """
        Load pet state from file.
        
        Returns:
            Pet if successful, None otherwise
        """
        try:
            if not self.save_file.exists():
                return None
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return Pet.from_dict(data)
        except Exception as e:
            print(f"Error loading: {e}")
            return None
    
    def has_save(self) -> bool:
        """Check if a save file exists."""
        return self.save_file.exists()
    
    def delete_save(self) -> bool:
        """Delete save file."""
        try:
            if self.save_file.exists():
                self.save_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

