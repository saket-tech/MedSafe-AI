"""
Medicine Database and Interaction Metadata
Manages medicine data, interactions, and database operations
"""

import json
from typing import List, Dict, Optional, Tuple
from rapidfuzz import fuzz, process

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
    
    def search_medicine(self, query: str, threshold: int = 70) -> List[Tuple[str, int]]:
        """
        Search for medicines using fuzzy string matching
        
        Args:
            query: Search query (medicine name with possible typos)
            threshold: Minimum similarity score (0-100)
            
        Returns:
            List of tuples (medicine_name, similarity_score)
        """
        if not query or not self.medicines:
            return []
        
        # Get all medicine names
        medicine_names = list(self.medicines.keys())
        
        # Use fuzzy matching to find similar medicines
        matches = process.extract(
            query.lower(),
            medicine_names,
            scorer=fuzz.ratio,
            limit=5
        )
        
        # Filter by threshold and return
        filtered_matches = [(name, score) for name, score, _ in matches if score >= threshold]
        return filtered_matches
    
    def find_medicine(self, query: str, threshold: int = 70) -> Optional[Dict]:
        """
        Find best matching medicine using fuzzy matching
        
        Args:
            query: Medicine name (possibly with typos)
            threshold: Minimum similarity score
            
        Returns:
            Medicine information dictionary or None
        """
        matches = self.search_medicine(query, threshold)
        
        if matches:
            # Return the best match
            best_match_name = matches[0][0]
            return {
                "name": best_match_name,
                "data": self.medicines[best_match_name],
                "confidence": matches[0][1]
            }
        
        return None
    
    def check_interactions(self, medicine_list: List[str]) -> List[Dict]:
        """
        Check for interactions between medicines
        
        Args:
            medicine_list: List of medicine names
            
        Returns:
            List of interaction warnings with details
        """
        if not medicine_list or len(medicine_list) < 2:
            return []
        
        interactions_found = []
        
        # Normalize medicine names to lowercase
        normalized_medicines = [med.lower() for med in medicine_list]
        
        # Check each pair of medicines
        for i in range(len(normalized_medicines)):
            for j in range(i + 1, len(normalized_medicines)):
                med1 = normalized_medicines[i]
                med2 = normalized_medicines[j]
                
                # Check both orderings in interactions database
                interaction_key1 = f"{med1}_{med2}"
                interaction_key2 = f"{med2}_{med1}"
                
                interaction = None
                if interaction_key1 in self.interactions:
                    interaction = self.interactions[interaction_key1]
                elif interaction_key2 in self.interactions:
                    interaction = self.interactions[interaction_key2]
                
                if interaction:
                    interactions_found.append({
                        "medicine1": med1,
                        "medicine2": med2,
                        "severity": interaction.get("severity", "unknown"),
                        "description": interaction.get("description", "No description available"),
                        "warning": f"⚠️ {interaction.get('severity', 'unknown').upper()} interaction detected"
                    })
        
        return interactions_found
    
    def get_medicine_warnings(self, medicine_name: str) -> List[str]:
        """
        Get all warnings for a specific medicine
        
        Args:
            medicine_name: Name of the medicine
            
        Returns:
            List of warning messages
        """
        warnings = []
        medicine = self.get_medicine(medicine_name)
        
        if medicine:
            # Check for grapefruit interactions
            if medicine.get("grapefruit") and medicine["grapefruit"] != "None":
                warnings.append(f"🍊 Grapefruit Warning: {medicine['grapefruit']}")
            
            # Check for known interactions
            if medicine.get("interactions"):
                interacting_meds = ", ".join(medicine["interactions"])
                warnings.append(f"💊 Known Interactions: {interacting_meds}")
        
        return warnings


# Example usage
if __name__ == "__main__":
    db = MedicineDatabase()
    print("Medicine Database Module - Ready for Activity 2.1 implementation")
