#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dự đoán giới tính từ tên tiếng Việt
Gender prediction script for Vietnamese names
"""

import numpy as np
import tensorflow as tf
import argparse
import sys
import os
from data_preprocessing import VietnameseNamePreprocessor

class VietnameseNamePredictor:
    """Lớp dự đoán giới tính từ tên tiếng Việt"""
    
    def __init__(self, model_path='../models/vietnamese_name_gender_model.h5',
                 preprocessor_path='../models/preprocessor.pkl'):
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path
        self.model = None
        self.preprocessor = None
        
    def load_model(self):
        """Tải mô hình và preprocessor"""
        try:
            # Tải mô hình
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Đã tải mô hình từ {self.model_path}")
            
            # Tải preprocessor
            self.preprocessor = VietnameseNamePreprocessor.load_preprocessor(self.preprocessor_path)
            print(f"Đã tải preprocessor từ {self.preprocessor_path}")
            
            return True
        except Exception as e:
            print(f"Lỗi khi tải mô hình: {e}")
            return False
    
    def predict_single(self, name):
        """Dự đoán giới tính cho một tên"""
        if self.model is None or self.preprocessor is None:
            print("Mô hình chưa được tải!")
            return None, None
        
        try:
            # Tiền xử lý tên
            processed_name = self.preprocessor.predict_preprocess(name)
            
            # Dự đoán
            prediction = self.model.predict(np.array([processed_name]), verbose=0)[0][0]
            
            # Chuyển đổi kết quả
            gender = 'Nam' if prediction > 0.5 else 'Nữ'
            confidence = prediction if prediction > 0.5 else 1 - prediction
            
            return gender, confidence
            
        except Exception as e:
            print(f"Lỗi khi dự đoán: {e}")
            return None, None
    
    def predict_batch(self, names):
        """Dự đoán giới tính cho danh sách tên"""
        if self.model is None or self.preprocessor is None:
            print("Mô hình chưa được tải!")
            return []
        
        results = []
        for name in names:
            gender, confidence = self.predict_single(name)
            if gender is not None:
                results.append({
                    'name': name,
                    'gender': gender,
                    'confidence': confidence
                })
        
        return results
    
    def interactive_predict(self):
        """Chế độ dự đoán tương tác"""
        print("=== DỰ ĐOÁN GIỚI TÍNH TỪ TÊN TIẾNG VIỆT ===")
        print("Nhập tên để dự đoán giới tính (hoặc 'quit' để thoát)")
        print("Ví dụ: Nguyễn Văn Nam, Trần Thị Hoa")
        print("-" * 50)
        
        while True:
            try:
                name = input("\nNhập tên: ").strip()
                
                if name.lower() in ['quit', 'exit', 'thoat']:
                    print("Tạm biệt!")
                    break
                
                if not name:
                    print("Vui lòng nhập tên!")
                    continue
                
                gender, confidence = self.predict_single(name)
                
                if gender is not None:
                    print(f"Kết quả: {name} -> {gender}")
                    print(f"Độ tin cậy: {confidence:.2%}")
                    
                    # Hiển thị thêm thông tin
                    if confidence > 0.9:
                        print("(Rất chắc chắn)")
                    elif confidence > 0.7:
                        print("(Khá chắc chắn)")
                    elif confidence > 0.5:
                        print("(Ít chắc chắn)")
                    else:
                        print("(Không chắc chắn)")
                else:
                    print("Không thể dự đoán cho tên này!")
                    
            except KeyboardInterrupt:
                print("\nTạm biệt!")
                break
            except Exception as e:
                print(f"Lỗi: {e}")

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(description='Dự đoán giới tính từ tên tiếng Việt')
    parser.add_argument('--name', '-n', type=str, help='Tên cần dự đoán')
    parser.add_argument('--file', '-f', type=str, help='File chứa danh sách tên')
    parser.add_argument('--interactive', '-i', action='store_true', 
                        help='Chế độ dự đoán tương tác')
    parser.add_argument('--model', '-m', type=str, 
                        default='../models/vietnamese_name_gender_model.h5',
                        help='Đường dẫn tới mô hình')
    parser.add_argument('--preprocessor', '-p', type=str,
                        default='../models/preprocessor.pkl',
                        help='Đường dẫn tới preprocessor')
    
    args = parser.parse_args()
    
    # Tạo predictor
    predictor = VietnameseNamePredictor(args.model, args.preprocessor)
    
    # Tải mô hình
    if not predictor.load_model():
        print("Không thể tải mô hình. Vui lòng kiểm tra đường dẫn.")
        return
    
    # Xử lý theo tùy chọn
    if args.interactive:
        predictor.interactive_predict()
    elif args.name:
        gender, confidence = predictor.predict_single(args.name)
        if gender is not None:
            print(f"Tên: {args.name}")
            print(f"Giới tính: {gender}")
            print(f"Độ tin cậy: {confidence:.2%}")
        else:
            print("Không thể dự đoán cho tên này!")
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                names = [line.strip() for line in f if line.strip()]
            
            print(f"Đang dự đoán cho {len(names)} tên từ file {args.file}...")
            results = predictor.predict_batch(names)
            
            print("\nKết quả:")
            print("-" * 60)
            for result in results:
                print(f"{result['name']:<30} -> {result['gender']:<5} ({result['confidence']:.2%})")
                
        except FileNotFoundError:
            print(f"Không tìm thấy file {args.file}")
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
    else:
        # Mặc định chạy chế độ tương tác
        predictor.interactive_predict()

if __name__ == "__main__":
    main()