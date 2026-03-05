"""
Medicine Database and Interaction Metadata
Manages medicine data, interactions, and database operations
"""

import json
from typing import List, Dict, Optional

class MedicineDatabase:
    """
    Manages medicine database and interaction rules
    """
    
    def __init__(self, medicines_file: str = "data/medicines.json", 
                 interactions_file: str = "data/interactions.json"):
        """
        Initialize medicine database
        
        Args:
            medicines_file: Path to medicines JSON file
            interactions_file: Path to interactions JSON file
        """
        self.medicines_file = medicines_file
        self.interactions_file = interactions_file
        self.medicines = {}
        self.interactions = {}
        
    def load_medicines(self) -> Dict:
        """
        Load medicine database from JSON file
        
        Returns:
            Dictionary of medicines with their properties
        """
        try:
            with open(self.medicines_file, 'r') as f:
                self.medicines = json.load(f)
            return self.medicines
        except FileNotFoundError:
            print(f"Medicine database file not found: {self.medicines_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding medicine database: {self.medicines_file}")
            return {}
    
    def load_interactions(self) -> Dict:
        """
        Load interaction rules from JSON file
        
        Returns:
            Dictionary of interaction rules
        """
        try:
            with open(self.interactions_file, 'r') as f:
                self.interactions = json.load(f)
            return self.interactions
        except FileNotFoundError:
            print(f"Interactions file not found: {self.interactions_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding interactions file: {self.interactions_file}")
            return {}
    
    def get_medicine(self, medicine_name: str) -> Optional[Dict]:
        """
        Get medicine information by name
        
        Args:
            medicine_name: Name of the medicine
            
        Returns:
            Medicine information dictionary or None
        """
        return self.medicines.get(medicine_name.lower())
    
    def check_interactions(self, medicine_list: List[str]) -> List[Dict]:
        """
        Check for interactions between medicines
        
        Args:
            medicine_list: List of medicine names
            
        Returns:
            List of interaction warnings
        """
        # Placeholder for interaction checking logic
        # Will be implemented in Activity 2.1
        interactions_found = []
        return interactions_found
    
    def get_all_medicines(self) -> List[str]:
        """
        Get list of all medicine names in database
        
        Returns:
            List of medicine names
        """
        return list(self.medicines.keys())
    
    def search_medicine(self, query: str) -> List[str]:
        """
        Search for medicines matching query
        
        Args:
            query: Search query
            
        Returns:
            List of matching medicine names
        """
        query_lower = query.lower()
        matches = [name for name in self.medicines.keys() 
                  if query_lower in name.lower()]
        return matches


# Example usage
if __name__ == "__main__":
    db = MedicineDatabase()
    print("Medicine Database Module - Ready for Activity 2.1 implementation")
