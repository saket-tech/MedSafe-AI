"""
OCR Utilities Module
Prescription OCR and text extraction utilities
"""

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from typing import Dict, List, Optional
import json
import re
from langchain_community.llms import Ollama

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
        try:
            # Convert to grayscale
            image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return image
    
    def parse_medicines_from_text(self, text: str) -> List[str]:
        """
        Parse medicine names from extracted text using basic pattern matching
        
        Args:
            text: Extracted text from prescription
            
        Returns:
            List of medicine names
        """
        medicines = []
        
        # Split text into lines
        lines = text.split('\n')
        
        # Common medicine patterns
        for line in lines:
            line = line.strip()
            
            # Skip empty lines or very short lines
            if len(line) < 3:
                continue
            
            # Look for lines that might contain medicine names
            # Typically: TAB, CAP, SYR, INJ followed by medicine name
            if any(keyword in line.upper() for keyword in ['TAB', 'CAP', 'SYR', 'INJ', 'TABLET', 'CAPSULE']):
                # Extract medicine name (usually after the dosage form)
                parts = re.split(r'[,\s]+', line)
                for part in parts:
                    if len(part) > 3 and part.isalpha():
                        medicines.append(part)
        
        return medicines
    
    def extract_structured_data(self, text: str, use_ai: bool = True) -> Dict:
        """
        Extract structured medicine data from text using AI
        
        Args:
            text: Extracted text from prescription
            use_ai: Whether to use AI for extraction (default: True)
            
        Returns:
            Structured data with medicines and active salts
        """
        if not text or text.strip() == "":
            return {
                "medicines": [],
                "active_salts": [],
                "dosages": [],
                "raw_text": text,
                "error": "No text extracted from image"
            }
        
        if use_ai:
            try:
                return self._extract_with_ai(text)
            except Exception as e:
                print(f"AI extraction failed: {e}")
                return self._extract_basic(text)
        else:
            return self._extract_basic(text)
    
    def _extract_with_ai(self, text: str) -> Dict:
        """
        Extract structured data using LLaMA 3 via Ollama
        
        Args:
            text: Extracted text from prescription
            
        Returns:
            Structured data dictionary
        """
        prompt = f"""You are a medical prescription parser. Extract medicine information from the following prescription text and return ONLY a valid JSON object with this exact structure:

{{
  "medicines": [
    {{
      "name": "medicine name",
      "active_salt": "active ingredient",
      "dosage": "dosage information",
      "form": "tablet/capsule/syrup/injection"
    }}
  ]
}}

Prescription text:
{text}

Return ONLY the JSON object, no additional text or explanation."""

        try:
            # Call LLaMA 3 via LangChain Ollama
            llm = Ollama(model='llama3')
            response_text = llm.invoke(prompt)
            
            # Try to parse JSON from response
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = re.sub(r'```json\n?', '', response_text)
                response_text = re.sub(r'```\n?', '', response_text)
            
            # Parse JSON
            structured_data = json.loads(response_text)
            
            # Add raw text
            structured_data['raw_text'] = text
            structured_data['extraction_method'] = 'AI (LLaMA 3)'
            
            return structured_data
            
        except Exception as e:
            print(f"Error in AI extraction: {e}")
            return self._extract_basic(text)
    
    def _extract_basic(self, text: str) -> Dict:
        """
        Basic extraction without AI (fallback method)
        
        Args:
            text: Extracted text from prescription
            
        Returns:
            Structured data dictionary
        """
        medicines = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if len(line) < 3:
                continue
            
            # Look for medicine patterns
            if any(keyword in line.upper() for keyword in ['TAB', 'CAP', 'SYR', 'INJ']):
                # Try to extract medicine info
                medicine_info = {
                    "name": "Unknown",
                    "active_salt": "Unknown",
                    "dosage": "Unknown",
                    "form": "Unknown"
                }
                
                # Extract form
                if 'TAB' in line.upper():
                    medicine_info['form'] = 'Tablet'
                elif 'CAP' in line.upper():
                    medicine_info['form'] = 'Capsule'
                elif 'SYR' in line.upper():
                    medicine_info['form'] = 'Syrup'
                elif 'INJ' in line.upper():
                    medicine_info['form'] = 'Injection'
                
                # Extract name (simplified)
                parts = re.split(r'[,\s]+', line)
                for part in parts:
                    if len(part) > 3 and part[0].isupper():
                        medicine_info['name'] = part
                        break
                
                medicines.append(medicine_info)
        
        return {
            "medicines": medicines,
            "raw_text": text,
            "extraction_method": "Basic Pattern Matching"
        }
    
    def validate_extraction(self, extracted_data: Dict) -> bool:
        """
        Validate extracted medicine data
        
        Args:
            extracted_data: Extracted structured data
            
        Returns:
            True if valid, False otherwise
        """
        if not extracted_data:
            return False
        
        if 'medicines' not in extracted_data:
            return False
        
        if len(extracted_data['medicines']) == 0:
            return False
        
        return True


# Example usage
if __name__ == "__main__":
    ocr = OCREngine()
    print("OCR Engine Module - Activity 2.2 implementation complete")
