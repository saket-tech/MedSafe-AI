"""
OCR Utilities Module
Prescription OCR and text extraction utilities
"""

import pytesseract
from PIL import Image
from typing import Dict, List, Optional
import json

class OCREngine:
    """
    Handles OCR processing and text extraction from prescription images
    """
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize OCR engine
        
        Args:
            tesseract_path: Path to Tesseract executable (optional)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from prescription image using OCR
        
        Args:
            image_path: Path to prescription image
            
        Returns:
            Extracted text string
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Preprocess image if needed
            processed_image = self.preprocess_image(image)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_image)
            
            return text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def extract_text_from_pil(self, pil_image: Image.Image) -> str:
        """
        Extract text from PIL Image object
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            Extracted text string
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(pil_image)
            
            # Extract text
            text = pytesseract.image_to_string(processed_image)
            
            return text
        except Exception as e:
            print(f"Error extracting text from PIL image: {e}")
            return ""
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        # Placeholder for image preprocessing
        # Can add: grayscale conversion, contrast enhancement, noise reduction
        # Will be enhanced in Activity 2.2
        return image
    
    def parse_medicines_from_text(self, text: str) -> List[str]:
        """
        Parse medicine names from extracted text
        
        Args:
            text: Extracted text from prescription
            
        Returns:
            List of medicine names
        """
        # Placeholder for medicine parsing logic
        # Will be implemented in Activity 2.2 with AI assistance
        medicines = []
        return medicines
    
    def extract_structured_data(self, text: str) -> Dict:
        """
        Extract structured medicine data from text using AI
        
        Args:
            text: Extracted text from prescription
            
        Returns:
            Structured data with medicines and active salts
        """
        # Placeholder for AI-based structured extraction
        # Will be implemented in Activity 2.2 using LLaMA 3
        structured_data = {
            "medicines": [],
            "active_salts": [],
            "dosages": [],
            "raw_text": text
        }
        return structured_data
    
    def validate_extraction(self, extracted_data: Dict) -> bool:
        """
        Validate extracted medicine data
        
        Args:
            extracted_data: Extracted structured data
            
        Returns:
            True if valid, False otherwise
        """
        # Placeholder for validation logic
        return True


# Example usage
if __name__ == "__main__":
    ocr = OCREngine()
    print("OCR Engine Module - Ready for Activity 2.2 implementation")
