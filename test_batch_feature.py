#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-end test for batch CSV prediction feature
"""

import os
import sys
import tempfile
import pandas as pd

# Add the python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

from python.name_normalizer import VietnameseNameNormalizer

def test_name_normalizer():
    """Test the name normalizer functionality"""
    print("Testing name normalizer...")
    
    normalizer = VietnameseNameNormalizer()
    
    test_cases = [
        ("anh Hiếu", "hiếu"),
        ("chị Trần Thị Hoa", "trần thị hoa"),
        ("bác sĩ Lê Minh Tuấn", "lê minh tuấn"),
        ("Dr. Nguyễn Xuân Sơn", "nguyễn xuân sơn"),
        ("Giám đốc Hoàng Minh Quân", "hoàng minh quân"),
        ("   em   Nguyễn   Thị   Mai   ", "nguyễn thị mai")
    ]
    
    passed = 0
    for raw_name, expected in test_cases:
        result = normalizer.clean_name(raw_name)
        if result == expected:
            print(f"✓ '{raw_name}' -> '{result}'")
            passed += 1
        else:
            print(f"✗ '{raw_name}' -> '{result}' (expected: '{expected}')")
    
    print(f"Name normalizer: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)

def test_batch_prediction():
    """Test batch prediction with a simple CSV"""
    print("\nTesting batch prediction...")
    
    # Create test CSV
    test_data = pd.DataFrame({
        'name': [
            'anh Hiếu',
            'chị Thương',
            'Nguyễn Văn Nam',
            'bác sĩ Trần Thị Hoa'
        ]
    })
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        test_data.to_csv(f.name, index=False)
        input_file = f.name
    
    output_file = input_file.replace('.csv', '_output.csv')
    
    try:
        # Run batch prediction
        import subprocess
        result = subprocess.run([
            sys.executable, 
            'python/batch_csv_predict.py', 
            '-i', input_file, 
            '-o', output_file,
            '-m', './models/vietnamese_name_gender_model.h5',
            '-p', './models/preprocessor.pkl'
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Batch prediction completed successfully")
            
            # Check output
            if os.path.exists(output_file):
                output_data = pd.read_csv(output_file)
                required_columns = ['raw_name', 'clean_name', 'gender_pred']
                
                if all(col in output_data.columns for col in required_columns):
                    print("✓ Output CSV has required columns")
                    
                    # Check title removal
                    if 'hiếu' in output_data['clean_name'].values:
                        print("✓ Title removal working correctly")
                        return True
                    else:
                        print("✗ Title removal not working correctly")
                else:
                    print("✗ Output CSV missing required columns")
            else:
                print("✗ Output file not created")
        else:
            print(f"✗ Batch prediction failed: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Error testing batch prediction: {e}")
    
    finally:
        # Cleanup
        for file in [input_file, output_file]:
            if os.path.exists(file):
                os.unlink(file)
    
    return False

def main():
    """Run all tests"""
    print("🧪 RUNNING END-TO-END TESTS FOR BATCH CSV PREDICTION")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Name normalizer
    if test_name_normalizer():
        tests_passed += 1
    
    # Test 2: Batch prediction
    if test_batch_prediction():
        tests_passed += 1
    
    print(f"\n📊 RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The batch CSV prediction feature is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())