"""
MedSafe AI - Performance Testing Script
Measures and documents actual performance metrics for all modules.
"""

from pathlib import Path
import sys
import os
import time
import tracemalloc
import json
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import psutil
from PIL import Image

from backend.services.med_db import MedicineDatabase
from backend.services.ocr_utils import OCREngine
from backend.services.risk_engine import RiskEngine
from backend.services.symptom import SymptomAnalyzer

SAMPLES_DIR = ROOT_DIR / "assets" / "samples"


class PerformanceTestRunner:
    """Runs performance tests and generates results report."""

    def __init__(self):
        self.results = {
            "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": self.get_system_info(),
            "tests": [],
        }

        self.med_db = MedicineDatabase()
        self.med_db.load_medicines()
        self.med_db.load_interactions()
        self.ocr_engine = OCREngine()
        self.symptom_analyzer = SymptomAnalyzer()
        self.risk_engine = RiskEngine()

    def get_system_info(self):
        return {
            "cpu_count": psutil.cpu_count(),
            "total_memory_mb": round(psutil.virtual_memory().total / (1024 * 1024), 2),
            "python_version": os.sys.version,
            "platform": os.sys.platform,
        }

    def measure_performance(self, test_name, func, *args, **kwargs):
        tracemalloc.start()
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024 * 1024)
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as exc:
            result = None
            success = False
            error = str(exc)

        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)
        mem_after = process.memory_info().rss / (1024 * 1024)
        mem_used = round(mem_after - mem_before, 2)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = round(peak / (1024 * 1024), 2)

        test_result = {
            "test_name": test_name,
            "elapsed_time_ms": elapsed_time,
            "memory_used_mb": mem_used,
            "peak_memory_mb": peak_mb,
            "success": success,
            "error": error,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.results["tests"].append(test_result)
        print(f"[OK] {test_name}: {elapsed_time}ms (Memory: {mem_used}MB)")
        return result, test_result

    def test_fuzzy_matching_exact(self):
        return self.measure_performance(
            "Fuzzy Match - Exact",
            lambda: self.med_db.find_medicine("Atorvastatin", threshold=70),
        )

    def test_fuzzy_matching_misspelled(self):
        return self.measure_performance(
            "Fuzzy Match - Misspelled",
            lambda: self.med_db.find_medicine("Ibuprofin", threshold=70),
        )

    def test_interaction_check_5_medicines(self):
        return self.measure_performance(
            "Interaction Check - 5 Medicines",
            lambda: self.med_db.check_interactions(
                ["warfarin", "ibuprofen", "aspirin", "atorvastatin", "clarithromycin"]
            ),
        )

    def test_ocr_processing(self):
        candidates = list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.jpeg")) + list(SAMPLES_DIR.glob("*.png"))
        if not candidates:
            print("[SKIP] OCR test - No sample image found")
            return None, None

        image_path = candidates[0]
        return self.measure_performance(
            f"OCR Processing - {image_path.name}",
            lambda: self.ocr_engine.extract_text_from_pil(Image.open(image_path)),
        )

    def test_symptom_analysis_without_ai(self):
        symptoms = "I have a severe headache, fever, and dizziness. Started this morning."
        return self.measure_performance(
            "Symptom Analysis - Without AI",
            lambda: self.symptom_analyzer.analyze_symptoms(symptoms, use_ai=False),
        )

    def test_risk_score_without_ai(self):
        return self.measure_performance(
            "Risk Score - Without AI",
            lambda: self.risk_engine.calculate_risk_score(
                symptoms="chest pain and difficulty breathing",
                severity=8,
                age=65,
                use_ai=False,
            ),
        )

    def run_all(self):
        self.test_fuzzy_matching_exact()
        self.test_fuzzy_matching_misspelled()
        self.test_interaction_check_5_medicines()
        self.test_ocr_processing()
        self.test_symptom_analysis_without_ai()
        self.test_risk_score_without_ai()

        report_path = ROOT_DIR / "docs" / "performance_results.json"
        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(self.results, file, indent=2)
        print(f"Saved performance report to {report_path}")


if __name__ == "__main__":
    PerformanceTestRunner().run_all()
