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
        # Try to find and configure tesseract
        tesseract_found = False
        
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            tesseract_found = True
        else:
            # Try common paths for cloud deployment
            possible_paths = [
                '/usr/bin/tesseract',
                '/usr/local/bin/tesseract',
                'tesseract',
            ]
            
            for path in possible_paths:
                try:
                    pytesseract.pytesseract.tesseract_cmd = path
                    pytesseract.get_tesseract_version()
                    tesseract_found = True
                    print(f"Tesseract found at: {path}")
                    break
                except Exception:
                    continue
        
        if not tesseract_found:
            print("Warning: Tesseract OCR not found. OCR functionality will not work.")
        
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        self.tesseract_available = tesseract_found
    
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
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Try multiple PSM modes for best results
            configs = [
                r'--oem 3 --psm 6',  # Uniform block of text
                r'--oem 3 --psm 4',  # Single column of text
                r'--oem 3 --psm 3',  # Fully automatic
            ]
            
            best_text = ""
            max_length = 0
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    if len(text.strip()) > max_length:
                        max_length = len(text.strip())
                        best_text = text
                except:
                    continue
            
            return best_text if best_text else pytesseract.image_to_string(processed_image)
            
        except pytesseract.TesseractNotFoundError:
            raise Exception("Tesseract OCR is not installed or not found. Please install Tesseract OCR to use this feature.")
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_text_from_pil(self, pil_image: Image.Image) -> str:
        """
        Extract text from PIL Image object
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            Extracted text string
        """
        if not self.tesseract_available:
            raise Exception("Tesseract OCR is not available on this server. Please install Tesseract OCR or use a local deployment.")
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(pil_image)
            
            # Try multiple PSM modes for best results
            configs = [
                r'--oem 3 --psm 6',  # Uniform block of text
                r'--oem 3 --psm 4',  # Single column of text
                r'--oem 3 --psm 3',  # Fully automatic
            ]
            
            best_text = ""
            max_length = 0
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    if len(text.strip()) > max_length:
                        max_length = len(text.strip())
                        best_text = text
                except:
                    continue
            
            return best_text if best_text else pytesseract.image_to_string(processed_image)
            
        except pytesseract.TesseractNotFoundError:
            raise Exception("Tesseract OCR is not installed. This feature requires Tesseract OCR to be installed on the server.")
        except Exception as e:
            print(f"Error extracting text from PIL image: {e}")
            raise Exception(f"Error extracting text: {str(e)}")
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        try:
            # Resize if too small for better OCR
            width, height = image.size
            if width < 1500:
                scale = 1500 / width
                new_size = (int(width * scale), int(height * scale))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB first (handles all image modes)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to grayscale
            image = image.convert('L')
            
            # Moderate contrast enhancement
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Moderate sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            return image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            # Return original if preprocessing fails
            try:
                return image.convert('L')
            except:
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
