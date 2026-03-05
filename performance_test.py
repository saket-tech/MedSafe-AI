"""
MedSafe AI - Performance Testing Script
Measures and documents actual performance metrics for all modules
"""

import time
import psutil
import os
from PIL import Image
import json
from datetime import datetime
import tracemalloc

# Import MedSafe modules
from med_db import MedicineDatabase
from ocr_utils import OCREngine
from symptom import SymptomAnalyzer
from risk_engine import RiskEngine


class PerformanceTestRunner:
    """Runs performance tests and generates results report"""
    
    def __init__(self):
        self.results = {
            'test_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': self.get_system_info(),
            'tests': []
        }
        
        # Initialize components
        self.med_db = MedicineDatabase()
        self.med_db.load_medicines()
        self.med_db.load_interactions()
        
        self.ocr_engine = OCREngine()
        self.symptom_analyzer = SymptomAnalyzer()
        self.risk_engine = RiskEngine()
    
    def get_system_info(self):
        """Get system information"""
        return {
            'cpu_count': psutil.cpu_count(),
            'total_memory_mb': round(psutil.virtual_memory().total / (1024 * 1024), 2),
            'python_version': os.sys.version,
            'platform': os.sys.platform
        }
    
    def measure_performance(self, test_name, func, *args, **kwargs):
        """Measure performance of a function"""
        # Start memory tracking
        tracemalloc.start()
        
        # Get initial memory
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Measure time
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)  # milliseconds
        
        # Get final memory
        mem_after = process.memory_info().rss / (1024 * 1024)  # MB
        mem_used = round(mem_after - mem_before, 2)
        
        # Get peak memory
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = round(peak / (1024 * 1024), 2)
        
        # Record result
        test_result = {
            'test_name': test_name,
            'elapsed_time_ms': elapsed_time,
            'memory_used_mb': mem_used,
            'peak_memory_mb': peak_mb,
            'success': success,
            'error': error,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.results['tests'].append(test_result)
        
        print(f"✓ {test_name}: {elapsed_time}ms (Memory: {mem_used}MB)")
        
        return result, test_result
    
    def test_fuzzy_matching_exact(self):
        """Test exact medicine match"""
        def test():
            return self.med_db.find_medicine("Atorvastatin", threshold=70)
        
        return self.measure_performance("Fuzzy Match - Exact", test)
    
    def test_fuzzy_matching_misspelled(self):
        """Test fuzzy medicine match"""
        def test():
            return self.med_db.find_medicine("Ibuprofin", threshold=70)
        
        return self.measure_performance("Fuzzy Match - Misspelled", test)
    
    def test_fuzzy_matching_multiple(self):
        """Test multiple medicine matches"""
        medicines = ["Atorvastatin", "Ibuprofin", "Metformin", "Asprin", "Warfarin",
                    "Lisinopril", "Amlodipine", "Omeprazol", "Simvastatin", "Losartan"]
        
        def test():
            results = []
            for med in medicines:
                result = self.med_db.find_medicine(med, threshold=70)
                results.append(result)
            return results
        
        return self.measure_performance("Fuzzy Match - 10 Medicines", test)
    
    def test_interaction_check_2_medicines(self):
        """Test interaction check with 2 medicines"""
        def test():
            return self.med_db.check_interactions(["warfarin", "ibuprofen"])
        
        return self.measure_performance("Interaction Check - 2 Medicines", test)
    
    def test_interaction_check_5_medicines(self):
        """Test interaction check with 5 medicines"""
        def test():
            return self.med_db.check_interactions(
                ["warfarin", "ibuprofen", "aspirin", "atorvastatin", "clarithromycin"]
            )
        
        return self.measure_performance("Interaction Check - 5 Medicines", test)
    
    def test_interaction_check_10_medicines(self):
        """Test interaction check with 10 medicines"""
        def test():
            return self.med_db.check_interactions([
                "warfarin", "ibuprofen", "aspirin", "atorvastatin", "clarithromycin",
                "metformin", "lisinopril", "amlodipine", "omeprazole", "simvastatin"
            ])
        
        return self.measure_performance("Interaction Check - 10 Medicines", test)
    
    def test_ocr_processing(self):
        """Test OCR processing if prescription image exists"""
        # Check if test image exists
        test_images = ["prescription.png", "prescription-placeholder.webp"]
        image_path = None
        
        for img in test_images:
            if os.path.exists(img):
                image_path = img
                break
        
        if not image_path:
            print("⚠ Skipping OCR test - No test image found")
            return None, None
        
        def test():
            image = Image.open(image_path)
            return self.ocr_engine.extract_text_from_pil(image)
        
        return self.measure_performance(f"OCR Processing - {image_path}", test)
    
    def test_ai_parsing(self):
        """Test AI parsing of prescription text"""
        sample_text = """
        Rx
        1. Atorvastatin 10mg - 1 tablet daily
        2. Metformin 500mg - 2 tablets twice daily
        3. Lisinopril 5mg - 1 tablet daily
        4. Aspirin 75mg - 1 tablet daily
        """
        
        def test():
            return self.ocr_engine.extract_structured_data(sample_text, use_ai=True)
        
        return self.measure_performance("AI Parsing - Medicine Extraction", test)
    
    def test_symptom_analysis_without_ai(self):
        """Test symptom analysis without AI"""
        symptoms = "I have a severe headache, fever, and dizziness. Started this morning."
        
        def test():
            return self.symptom_analyzer.analyze_symptoms(symptoms, use_ai=False)
        
        return self.measure_performance("Symptom Analysis - Without AI", test)
    
    def test_symptom_analysis_with_ai(self):
        """Test symptom analysis with AI"""
        symptoms = "I have a severe headache, fever, and dizziness. Started this morning."
        
        def test():
            return self.symptom_analyzer.analyze_symptoms(symptoms, use_ai=True)
        
        return self.measure_performance("Symptom Analysis - With AI", test)
    
    def test_symptom_analysis_long_description(self):
        """Test symptom analysis with long description"""
        symptoms = """I have been experiencing severe headaches for the past three days. 
        The pain is concentrated on the right side of my head and feels like a throbbing sensation.
        Along with the headache, I have been feeling dizzy and nauseous. I also have a mild fever
        that comes and goes. The symptoms are worse in the morning and improve slightly in the evening.
        I have tried taking over-the-counter pain medication but it only provides temporary relief.
        I am also experiencing sensitivity to light and sound. The headache is affecting my ability
        to work and concentrate. I have no history of migraines but this feels different from
        regular headaches I have had before."""
        
        def test():
            return self.symptom_analyzer.analyze_symptoms(symptoms, use_ai=False)
        
        return self.measure_performance("Symptom Analysis - Long Description", test)
    
    def test_side_effect_analysis_without_ai(self):
        """Test side effect analysis without AI"""
        def test():
            return self.risk_engine.analyze_side_effects(
                medicine="Ibuprofen",
                dosage="400mg",
                experience="Mild stomach upset and nausea after taking the medicine",
                age=35,
                gender="Male",
                use_ai=False
            )
        
        return self.measure_performance("Side Effect Analysis - Without AI", test)
    
    def test_side_effect_analysis_with_ai(self):
        """Test side effect analysis with AI"""
        def test():
            return self.risk_engine.analyze_side_effects(
                medicine="Ibuprofen",
                dosage="400mg",
                experience="Mild stomach upset and nausea after taking the medicine",
                age=35,
                gender="Male",
                use_ai=True
            )
        
        return self.measure_performance("Side Effect Analysis - With AI", test)
    
    def test_risk_calculation_simple(self):
        """Test risk calculation with simple input"""
        def test():
            return self.risk_engine.calculate_risk_score(
                symptoms="Mild headache and fatigue",
                severity=3,
                age=30,
                gender="Male",
                medical_history=None,
                use_ai=False
            )
        
        return self.measure_performance("Risk Calculation - Simple", test)
    
    def test_risk_calculation_complex(self):
        """Test risk calculation with complex input"""
        def test():
            return self.risk_engine.calculate_risk_score(
                symptoms="Severe chest pain, difficulty breathing, sweating, radiating to left arm",
                severity=9,
                age=65,
                gender="Male",
                medical_history=["Heart Disease", "Diabetes", "Hypertension"],
                use_ai=False
            )
        
        return self.measure_performance("Risk Calculation - Complex", test)
    
    def test_risk_calculation_with_ai(self):
        """Test risk calculation with AI safety note"""
        def test():
            return self.risk_engine.calculate_risk_score(
                symptoms="Severe chest pain, difficulty breathing",
                severity=8,
                age=60,
                gender="Male",
                medical_history=["Heart Disease"],
                use_ai=True
            )
        
        return self.measure_performance("Risk Calculation - With AI", test)
    
    def test_sequential_requests(self, count=10):
        """Test multiple sequential requests"""
        print(f"\n--- Testing {count} Sequential Requests ---")
        
        times = []
        for i in range(count):
            start = time.time()
            self.med_db.find_medicine("Atorvastatin", threshold=70)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        avg_time = round(sum(times) / len(times), 2)
        min_time = round(min(times), 2)
        max_time = round(max(times), 2)
        
        result = {
            'test_name': f'Sequential Requests - {count}x',
            'average_time_ms': avg_time,
            'min_time_ms': min_time,
            'max_time_ms': max_time,
            'times': times
        }
        
        self.results['tests'].append(result)
        print(f"✓ Sequential {count}x: Avg={avg_time}ms, Min={min_time}ms, Max={max_time}ms")
        
        return result
    
    def run_all_tests(self):
        """Run all performance tests"""
        print("=" * 60)
        print("MedSafe AI - Performance Testing")
        print("=" * 60)
        print(f"Date: {self.results['test_date']}")
        print(f"CPU Cores: {self.results['system_info']['cpu_count']}")
        print(f"Total Memory: {self.results['system_info']['total_memory_mb']} MB")
        print("=" * 60)
        
        print("\n--- Medicine Interaction Checker Tests ---")
        self.test_fuzzy_matching_exact()
        self.test_fuzzy_matching_misspelled()
        self.test_fuzzy_matching_multiple()
        self.test_interaction_check_2_medicines()
        self.test_interaction_check_5_medicines()
        self.test_interaction_check_10_medicines()
        
        print("\n--- Prescription OCR Tests ---")
        self.test_ocr_processing()
        self.test_ai_parsing()
        
        print("\n--- Symptom Analysis Tests ---")
        self.test_symptom_analysis_without_ai()
        self.test_symptom_analysis_long_description()
        self.test_symptom_analysis_with_ai()
        
        print("\n--- Side Effect Analysis Tests ---")
        self.test_side_effect_analysis_without_ai()
        self.test_side_effect_analysis_with_ai()
        
        print("\n--- Risk Calculation Tests ---")
        self.test_risk_calculation_simple()
        self.test_risk_calculation_complex()
        self.test_risk_calculation_with_ai()
        
        print("\n--- Sequential Request Tests ---")
        self.test_sequential_requests(10)
        
        print("\n" + "=" * 60)
        print("Performance Testing Complete")
        print("=" * 60)
        
        return self.results
    
    def generate_report(self, filename='performance_test_results.json'):
        """Generate JSON report of test results"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✓ Results saved to: {filename}")
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate human-readable summary"""
        print("\n" + "=" * 60)
        print("PERFORMANCE TEST SUMMARY")
        print("=" * 60)
        
        # Group tests by category
        categories = {
            'Fuzzy Match': [],
            'Interaction Check': [],
            'OCR': [],
            'AI Parsing': [],
            'Symptom Analysis': [],
            'Side Effect': [],
            'Risk Calculation': []
        }
        
        for test in self.results['tests']:
            if 'elapsed_time_ms' not in test:
                continue
            
            for category in categories.keys():
                if category in test['test_name']:
                    categories[category].append(test)
                    break
        
        # Print summary by category
        for category, tests in categories.items():
            if not tests:
                continue
            
            print(f"\n{category}:")
            for test in tests:
                status = "✓" if test['success'] else "✗"
                time_str = f"{test['elapsed_time_ms']}ms"
                mem_str = f"{test['memory_used_mb']}MB"
                print(f"  {status} {test['test_name']}: {time_str} (Memory: {mem_str})")
        
        # Calculate overall statistics
        successful_tests = [t for t in self.results['tests'] if t.get('success', False) and 'elapsed_time_ms' in t]
        
        if successful_tests:
            total_tests = len(successful_tests)
            avg_time = round(sum(t['elapsed_time_ms'] for t in successful_tests) / total_tests, 2)
            total_memory = round(sum(t['memory_used_mb'] for t in successful_tests), 2)
            
            print(f"\n{'=' * 60}")
            print(f"Total Tests: {total_tests}")
            print(f"Average Time: {avg_time}ms")
            print(f"Total Memory Used: {total_memory}MB")
            print(f"{'=' * 60}")


def main():
    """Main function to run performance tests"""
    runner = PerformanceTestRunner()
    results = runner.run_all_tests()
    runner.generate_report()
    
    print("\n✓ Performance testing complete!")
    print("✓ Review 'performance_test_results.json' for detailed results")


if __name__ == "__main__":
    main()
