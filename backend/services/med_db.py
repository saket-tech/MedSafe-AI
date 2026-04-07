"""
Medicine Database and Interaction Metadata
Manages medicine data, interactions, and database operations
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rapidfuzz import fuzz, process

from backend.config import DATA_DIR


class MedicineDatabase:
    """Manages medicine database and interaction rules."""

    def __init__(
        self,
        medicines_file: Optional[str] = None,
        interactions_file: Optional[str] = None,
    ):
        self.medicines_file = Path(medicines_file) if medicines_file else DATA_DIR / "medicines.json"
        self.interactions_file = (
            Path(interactions_file) if interactions_file else DATA_DIR / "interactions.json"
        )
        self.medicines: Dict = {}
        self.interactions: Dict = {}

    def load_medicines(self) -> Dict:
        try:
            with open(self.medicines_file, "r", encoding="utf-8") as file:
                self.medicines = json.load(file)
            return self.medicines
        except FileNotFoundError:
            print(f"Medicine database file not found: {self.medicines_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding medicine database: {self.medicines_file}")
            return {}

    def load_interactions(self) -> Dict:
        try:
            with open(self.interactions_file, "r", encoding="utf-8") as file:
                self.interactions = json.load(file)
            return self.interactions
        except FileNotFoundError:
            print(f"Interactions file not found: {self.interactions_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding interactions file: {self.interactions_file}")
            return {}

    def get_medicine(self, medicine_name: str) -> Optional[Dict]:
        return self.medicines.get(medicine_name.lower())

    def get_all_medicines(self) -> List[str]:
        return list(self.medicines.keys())

    def search_medicine(self, query: str, threshold: int = 70) -> List[Tuple[str, int]]:
        if not query or not self.medicines:
            return []

        if re.search(r"[^a-zA-Z0-9\s\-]", query):
            return []

        medicine_names = list(self.medicines.keys())
        matches = process.extract(query.lower(), medicine_names, scorer=fuzz.ratio, limit=5)
        return [(name, score) for name, score, _ in matches if score >= threshold]

    def find_medicine(self, query: str, threshold: int = 70) -> Optional[Dict]:
        matches = self.search_medicine(query, threshold)
        if not matches:
            return None

        best_match_name = matches[0][0]
        return {
            "name": best_match_name,
            "data": self.medicines[best_match_name],
            "confidence": matches[0][1],
        }

    def check_interactions(self, medicine_list: List[str]) -> List[Dict]:
        if not medicine_list or len(medicine_list) < 2:
            return []

        interactions_found = []
        normalized_medicines = [medicine.lower() for medicine in medicine_list]

        for i in range(len(normalized_medicines)):
            for j in range(i + 1, len(normalized_medicines)):
                med1 = normalized_medicines[i]
                med2 = normalized_medicines[j]

                interaction_key1 = f"{med1}_{med2}"
                interaction_key2 = f"{med2}_{med1}"

                interaction = None
                if interaction_key1 in self.interactions:
                    interaction = self.interactions[interaction_key1]
                elif interaction_key2 in self.interactions:
                    interaction = self.interactions[interaction_key2]

                if interaction:
                    interactions_found.append(
                        {
                            "medicine1": med1,
                            "medicine2": med2,
                            "severity": interaction.get("severity", "unknown"),
                            "description": interaction.get(
                                "description", "No description available"
                            ),
                            "warning": (
                                f"{interaction.get('severity', 'unknown').upper()} interaction detected"
                            ),
                        }
                    )

        return interactions_found

    def get_medicine_warnings(self, medicine_name: str) -> List[str]:
        warnings = []
        medicine = self.get_medicine(medicine_name)

        if medicine:
            if medicine.get("grapefruit") and medicine["grapefruit"] != "None":
                warnings.append(f"Grapefruit Warning: {medicine['grapefruit']}")

            if medicine.get("interactions"):
                interacting_meds = ", ".join(medicine["interactions"])
                warnings.append(f"Known Interactions: {interacting_meds}")

        return warnings
