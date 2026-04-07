"""
OCR Utilities Module
Prescription OCR and text extraction utilities
"""

import json
import re
from typing import Dict, List, Optional

import ollama
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from backend.services.med_db import MedicineDatabase


class OCREngine:
    """Handles OCR processing and text extraction from prescription images."""

    def __init__(self, tesseract_path: Optional[str] = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        self.supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        self.medicine_db = MedicineDatabase()
        self.medicine_db.load_medicines()

    def extract_text(self, image_path: str) -> str:
        try:
            image = Image.open(image_path)
            return self.extract_text_from_pil(image)
        except Exception as exc:
            print(f"Error extracting text: {exc}")
            return ""

    def extract_text_from_pil(self, pil_image: Image.Image) -> str:
        try:
            configs = [
                r"--oem 3 --psm 6",
                r"--oem 3 --psm 4",
                r"--oem 3 --psm 11",
                r"--oem 3 --psm 3",
                r"--oem 1 --psm 6",
            ]

            results = []
            for image_variant in self._generate_image_variants(pil_image):
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(image_variant, config=config, lang="eng")
                        if text and text.strip():
                            results.append((text, self._score_extracted_text(text)))
                    except Exception as exc:
                        print(f"Config {config} failed: {exc}")

            if results:
                results.sort(key=lambda item: item[1], reverse=True)
                return results[0][0]

            return ""
        except Exception as exc:
            print(f"Error extracting text from PIL image: {exc}")
            return ""

    def _generate_image_variants(self, image: Image.Image) -> List[Image.Image]:
        variants = []

        base = image.copy()
        if base.mode not in ("RGB", "L"):
            base = base.convert("RGB")
        variants.append(base)

        processed = self.preprocess_image(base.copy())
        variants.append(processed)

        grayscale = ImageOps.autocontrast(base.convert("L"), cutoff=2)
        variants.append(grayscale)

        sharp = grayscale.filter(ImageFilter.SHARPEN)
        sharp = ImageEnhance.Contrast(sharp).enhance(1.8)
        variants.append(sharp)

        return variants

    def _find_medicine_candidates(self, text: str) -> List[Dict]:
        candidates: List[Dict] = []
        seen = set()
        medicine_names = self.medicine_db.get_all_medicines()
        if not medicine_names:
            return candidates

        clean_text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text.lower())
        tokens = [token for token in clean_text.split() if len(token) > 2]

        for size in [3, 2, 1]:
            for index in range(len(tokens) - size + 1):
                phrase = " ".join(tokens[index:index + size]).strip()
                if not phrase or phrase in seen:
                    continue

                match = self.medicine_db.find_medicine(phrase, threshold=78)
                if match and match["name"] not in seen:
                    seen.add(match["name"])
                    candidates.append(match)

        return candidates

    def _score_extracted_text(self, text: str) -> int:
        alnum_count = len(re.findall(r"[A-Za-z0-9]", text))
        medicine_bonus = len(self._find_medicine_candidates(text)) * 120
        dosage_bonus = len(re.findall(r"\b\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g)\b", text, flags=re.I)) * 40
        return alnum_count + medicine_bonus + dosage_bonus

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        try:
            width, height = image.size
            min_dimension = 2000
            if width < min_dimension or height < min_dimension:
                scale = max(min_dimension / width, min_dimension / height)
                new_size = (int(width * scale), int(height * scale))
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            image = image.convert("L")

            import numpy as np
            from PIL import ImageOps
            from scipy.ndimage import median_filter
            from skimage.filters import threshold_local

            image = ImageOps.autocontrast(image, cutoff=2)

            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.8)

            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)

            img_array = np.array(image)
            img_array = median_filter(img_array, size=2)

            block_size = 35
            if img_array.shape[0] > block_size and img_array.shape[1] > block_size:
                local_thresh = threshold_local(img_array, block_size, offset=10, method="gaussian")
                binary = img_array > local_thresh
                img_array = (binary * 255).astype(np.uint8)

            return Image.fromarray(img_array)
        except Exception as exc:
            print(f"Error in advanced preprocessing: {exc}, falling back to basic")
            try:
                if image.mode != "L":
                    image = image.convert("L")
                enhancer = ImageEnhance.Contrast(image)
                return enhancer.enhance(1.5)
            except Exception:
                return image

    def parse_medicines_from_text(self, text: str) -> List[str]:
        medicines = []
        lines = text.split("\n")

        for line in lines:
            line = line.strip()
            if len(line) < 3:
                continue

            if any(keyword in line.upper() for keyword in ["TAB", "CAP", "SYR", "INJ", "TABLET", "CAPSULE"]):
                parts = re.split(r"[,\s]+", line)
                for part in parts:
                    if len(part) > 3 and part.isalpha():
                        medicines.append(part)

        return medicines

    def extract_structured_data(self, text: str, use_ai: bool = True) -> Dict:
        if not text or text.strip() == "":
            return {
                "medicines": [],
                "active_salts": [],
                "dosages": [],
                "raw_text": text,
                "error": "No text extracted from image",
            }

        if use_ai:
            try:
                return self._extract_with_ai(text)
            except Exception as exc:
                print(f"AI extraction failed: {exc}")
                return self._extract_basic(text)

        return self._extract_basic(text)

    def _extract_with_ai(self, text: str) -> Dict:
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
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            response_text = response["message"]["content"].strip()
            if response_text.startswith("```"):
                response_text = re.sub(r"```json\n?", "", response_text)
                response_text = re.sub(r"```\n?", "", response_text)

            structured_data = json.loads(response_text)
            structured_data["raw_text"] = text
            structured_data["extraction_method"] = "AI (LLaMA 3)"
            return structured_data
        except Exception as exc:
            print(f"Error in AI extraction: {exc}")
            return self._extract_basic(text)

    def _extract_basic(self, text: str) -> Dict:
        medicines = []
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        candidates = self._find_medicine_candidates(text)

        for candidate in candidates:
            matched_line = next(
                (line for line in lines if candidate["data"]["name"].lower() in line.lower() or candidate["name"] in line.lower()),
                "",
            )
            dosage_match = re.search(r"\b\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g)\b", matched_line, flags=re.I)

            form = "Unknown"
            upper_line = matched_line.upper()
            if any(keyword in upper_line for keyword in ["TAB", "TABLET"]):
                form = "Tablet"
            elif any(keyword in upper_line for keyword in ["CAP", "CAPSULE"]):
                form = "Capsule"
            elif any(keyword in upper_line for keyword in ["SYR", "SYRUP"]):
                form = "Syrup"
            elif any(keyword in upper_line for keyword in ["INJ", "INJECTION"]):
                form = "Injection"

            medicines.append(
                {
                    "name": candidate["data"].get("name", candidate["name"].title()),
                    "active_salt": candidate["data"].get("active_salt", candidate["data"].get("name", "Unknown")),
                    "dosage": dosage_match.group(0) if dosage_match else "Unknown",
                    "form": form,
                }
            )

        if not medicines:
            for line in lines:
                if any(keyword in line.upper() for keyword in ["TAB", "CAP", "SYR", "INJ"]):
                    medicine_info = {
                        "name": "Unknown",
                        "active_salt": "Unknown",
                        "dosage": "Unknown",
                        "form": "Unknown",
                    }

                    if "TAB" in line.upper():
                        medicine_info["form"] = "Tablet"
                    elif "CAP" in line.upper():
                        medicine_info["form"] = "Capsule"
                    elif "SYR" in line.upper():
                        medicine_info["form"] = "Syrup"
                    elif "INJ" in line.upper():
                        medicine_info["form"] = "Injection"

                    dosage_match = re.search(r"\b\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g)\b", line, flags=re.I)
                    if dosage_match:
                        medicine_info["dosage"] = dosage_match.group(0)

                    parts = re.split(r"[,\s]+", line)
                    for part in parts:
                        if len(part) > 3 and part[0].isalpha():
                            medicine_info["name"] = part
                            break

                    medicines.append(medicine_info)

        return {
            "medicines": medicines,
            "raw_text": text,
            "extraction_method": "Basic Pattern Matching",
        }

    def validate_extraction(self, extracted_data: Dict) -> bool:
        return bool(extracted_data and "medicines" in extracted_data and extracted_data["medicines"])
