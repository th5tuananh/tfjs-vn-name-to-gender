#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script demo đơn giản cho việc dự đoán giới tính từ tên tiếng Việt
Simple demo script for Vietnamese name to gender prediction
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_preprocessing import VietnameseNamePreprocessor
from predict import VietnameseNamePredictor

def main():
    print("🎯 DEMO DỰ ĐOÁN GIỚI TÍNH TỪ TÊN TIẾNG VIỆT")
    print("=" * 50)
    
    # Khởi tạo predictor
    predictor = VietnameseNamePredictor()
    
    # Tải mô hình
    print("📥 Đang tải mô hình...")
    if not predictor.load_model():
        print("❌ Không thể tải mô hình!")
        print("💡 Hãy chạy: python train_model.py")
        return
    
    print("✅ Mô hình đã sẵn sàng!")
    print()
    
    # Danh sách tên demo
    demo_names = [
        "Nguyễn Văn Nam",
        "Trần Thị Hoa",
        "Lê Minh Tuấn",
        "Phạm Thu Hà",
        "Vũ Hoàng Anh",
        "Đỗ Thị Linh",
        "Bùi Quang Huy",
        "Phan Thu Trang",
        "Lương Minh Khang",
        "Hoàng Thị Ánh",
        "Đinh Văn Hùng",
        "Võ Thị Lan",
        "Cao Minh Đức",
        "Nông Thị Mai",
        "Tạ Hoàng Long"
    ]
    
    print("🧪 KẾT QUẢ DỰ ĐOÁN DEMO:")
    print("-" * 50)
    print(f"{'Tên':<25} {'Giới tính':<10} {'Độ tin cậy':<12}")
    print("-" * 50)
    
    correct_predictions = 0
    total_predictions = len(demo_names)
    
    for name in demo_names:
        gender, confidence = predictor.predict_single(name)
        
        if gender is not None:
            # Xác định giới tính thật (dựa vào tên)
            is_male = any(word in name.lower() for word in ['văn', 'minh', 'hoàng', 'quang', 'đức', 'hùng', 'long'])
            is_female = any(word in name.lower() for word in ['thị', 'thu', 'hoa', 'linh', 'trang', 'ánh', 'lan', 'mai'])
            
            # Emoji cho kết quả
            emoji = "🔵" if gender == "Nam" else "🟠"
            
            print(f"{name:<25} {emoji} {gender:<8} {confidence:.1%}")
            
            # Tính độ chính xác (đơn giản)
            if (gender == "Nam" and is_male) or (gender == "Nữ" and is_female):
                correct_predictions += 1
    
    print("-" * 50)
    accuracy = (correct_predictions / total_predictions) * 100
    print(f"📊 Độ chính xác ước tính: {accuracy:.1f}%")
    print()
    
    # Hướng dẫn sử dụng
    print("🎮 HƯỚNG DẪN SỬ DỤNG:")
    print("• Dự đoán một tên: python predict.py --name 'Tên của bạn'")
    print("• Chế độ tương tác: python predict.py --interactive")
    print("• Dự đoán từ file: python predict.py --file danh_sach.txt")
    print("• Demo đầy đủ: python demo.py")
    print()
    
    print("🌟 Cảm ơn bạn đã sử dụng!")

if __name__ == "__main__":
    main()