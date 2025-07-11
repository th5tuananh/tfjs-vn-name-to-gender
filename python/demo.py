#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ví dụ sử dụng mô hình dự đoán giới tính từ tên tiếng Việt
Example usage of Vietnamese name to gender prediction model
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_preprocessing import VietnameseNamePreprocessor
from train_model import VietnameseNameModel
from predict import VietnameseNamePredictor

def demo_preprocessing():
    """Demo tiền xử lý dữ liệu"""
    print("=== DEMO TIỀN XỬ LÝ DỮ LIỆU ===")
    
    # Tạo preprocessor
    preprocessor = VietnameseNamePreprocessor()
    
    # Test với một số tên
    test_names = [
        "Nguyễn Văn Nam",
        "Trần Thị Hoa", 
        "Lê Minh Tuấn",
        "Phạm Thu Hà",
        "Hoàng Anh"
    ]
    
    print("Chuyển đổi tên thành chuỗi số:")
    for name in test_names:
        sequence = preprocessor.text_to_sequence(name)
        padded = preprocessor.predict_preprocess(name)
        print(f"{name:<20} -> {sequence[:10]}... (length: {len(sequence)})")
        print(f"{'After padding:':<20} -> {padded[:10]}... (length: {len(padded)})")
        print()

def demo_prediction():
    """Demo dự đoán"""
    print("=== DEMO DỰ ĐOÁN ===")
    
    # Kiểm tra xem mô hình có tồn tại không
    model_path = '../models/vietnamese_name_gender_model.h5'
    preprocessor_path = '../models/preprocessor.pkl'
    
    if not os.path.exists(model_path):
        print("Chưa có mô hình được huấn luyện!")
        print("Vui lòng chạy: python train_model.py")
        return
    
    # Tạo predictor
    predictor = VietnameseNamePredictor(model_path, preprocessor_path)
    
    # Tải mô hình
    if not predictor.load_model():
        print("Không thể tải mô hình!")
        return
    
    # Test với một số tên
    test_names = [
        "Nguyễn Văn Nam",
        "Trần Thị Hoa",
        "Lê Minh Tuấn", 
        "Phạm Thu Hà",
        "Hoàng Anh Tuấn",
        "Vũ Thị Lan",
        "Đỗ Minh Hải",
        "Bùi Thu Trang",
        "Phan Văn Đức",
        "Lương Thị Mai"
    ]
    
    print("Kết quả dự đoán:")
    print("-" * 50)
    
    for name in test_names:
        gender, confidence = predictor.predict_single(name)
        if gender is not None:
            print(f"{name:<20} -> {gender:<5} ({confidence:.1%})")
        else:
            print(f"{name:<20} -> Lỗi")

def create_sample_data():
    """Tạo dữ liệu mẫu để test"""
    print("=== TẠO DỮ LIỆU MẪU ===")
    
    sample_names = [
        # Tên nam
        ("Nguyễn Văn Nam", "m"),
        ("Trần Minh Tuấn", "m"),
        ("Lê Hoàng Anh", "m"),
        ("Phạm Văn Đức", "m"),
        ("Vũ Minh Hải", "m"),
        ("Đỗ Thanh Tùng", "m"),
        ("Bùi Quang Huy", "m"),
        ("Phan Văn Thành", "m"),
        ("Lương Minh Khang", "m"),
        ("Hoàng Anh Tuấn", "m"),
        
        # Tên nữ
        ("Nguyễn Thị Hoa", "f"),
        ("Trần Thu Hà", "f"),
        ("Lê Thị Lan", "f"),
        ("Phạm Thu Trang", "f"),
        ("Vũ Thị Mai", "f"),
        ("Đỗ Thị Linh", "f"),
        ("Bùi Thu Hương", "f"),
        ("Phan Thị Nga", "f"),
        ("Lương Thị Hạnh", "f"),
        ("Hoàng Thị Ánh", "f"),
    ]
    
    # Lưu vào file
    with open('../sample_data.csv', 'w', encoding='utf-8') as f:
        for name, gender in sample_names:
            f.write(f"{name},{gender}\n")
    
    print(f"Đã tạo {len(sample_names)} mẫu dữ liệu trong file sample_data.csv")

def main():
    """Hàm chính"""
    print("DỰ ÁN DỰ ĐOÁN GIỚI TÍNH TỪ TÊN TIẾNG VIỆT")
    print("=" * 50)
    
    while True:
        print("\nChọn chức năng:")
        print("1. Demo tiền xử lý dữ liệu")
        print("2. Demo dự đoán")
        print("3. Tạo dữ liệu mẫu")
        print("4. Thoát")
        
        choice = input("\nNhập lựa chọn (1-4): ").strip()
        
        if choice == '1':
            demo_preprocessing()
        elif choice == '2':
            demo_prediction()
        elif choice == '3':
            create_sample_data()
        elif choice == '4':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()