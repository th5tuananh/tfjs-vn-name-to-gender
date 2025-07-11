#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese name normalization and title removal
Chuẩn hóa tên tiếng Việt và loại bỏ xưng hô
"""

import re
import unicodedata

class VietnameseNameNormalizer:
    """Lớp chuẩn hóa tên tiếng Việt"""
    
    def __init__(self):
        # Danh sách các xưng hô tiếng Việt
        self.titles = [
            'anh', 'chị', 'em', 'bác', 'cô', 'chú', 'dì', 'thím', 
            'ông', 'bà', 'cụ', 'thầy', 'cô', 'thầy', 'giáo', 'sư',
            'tiến sĩ', 'tiến sỹ', 'ts', 'th.s', 'ths', 'bs', 'bác sĩ',
            'kỹ sư', 'ks', 'luật sư', 'ls', 'giám đốc', 'gđ',
            'phó giám đốc', 'pgđ', 'trưởng phòng', 'tp', 'phó trưởng phòng', 'ptp',
            'mr', 'mrs', 'miss', 'ms', 'dr', 'prof', 'professor'
        ]
        
        # Tạo pattern regex để match các xưng hô
        # Sắp xếp theo độ dài giảm dần để tránh match sai
        sorted_titles = sorted(self.titles, key=len, reverse=True)
        self.title_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(title) for title in sorted_titles) + r')\b\s*',
            re.IGNORECASE
        )
    
    def remove_titles(self, name):
        """Loại bỏ xưng hô từ tên"""
        if not name:
            return ""
        
        # Chuyển về chữ thường để so sánh
        name_lower = name.lower().strip()
        
        # Loại bỏ xưng hô
        cleaned_name = self.title_pattern.sub('', name_lower)
        
        # Loại bỏ khoảng trắng thừa
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
        
        return cleaned_name
    
    def normalize_vietnamese_text(self, text):
        """Chuẩn hóa văn bản tiếng Việt"""
        if not text:
            return ""
        
        # Chuẩn hóa Unicode (NFC)
        text = unicodedata.normalize('NFC', text)
        
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Chuyển về chữ thường
        text = text.lower()
        
        return text
    
    def clean_name(self, raw_name):
        """Làm sạch tên hoàn chỉnh"""
        if not raw_name:
            return ""
        
        # Bước 1: Loại bỏ xưng hô
        name_without_titles = self.remove_titles(raw_name)
        
        # Bước 2: Chuẩn hóa văn bản
        normalized_name = self.normalize_vietnamese_text(name_without_titles)
        
        # Bước 3: Loại bỏ các ký tự đặc biệt không cần thiết
        clean_name = re.sub(r'[^\w\s\u00C0-\u024F\u1E00-\u1EFF]', '', normalized_name)
        
        # Bước 4: Loại bỏ khoảng trắng thừa cuối cùng
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        
        return clean_name
    
    def extract_first_name(self, full_name):
        """Trích xuất tên (từ cuối cùng) từ họ tên đầy đủ"""
        if not full_name:
            return ""
        
        # Tách các từ
        parts = full_name.strip().split()
        
        if not parts:
            return ""
        
        # Tên thường là từ cuối cùng
        return parts[-1]
    
    def validate_name(self, name):
        """Kiểm tra tên có hợp lệ không"""
        if not name:
            return False
        
        # Tên phải có ít nhất 1 ký tự
        if len(name.strip()) < 1:
            return False
        
        # Tên không được chỉ chứa số
        if name.strip().isdigit():
            return False
        
        return True

# Ví dụ sử dụng
if __name__ == "__main__":
    normalizer = VietnameseNameNormalizer()
    
    # Test cases
    test_names = [
        "anh Hiếu",
        "Chị Thương",
        "Nguyễn Văn Nam",
        "bác sĩ Trần Thị Hoa",
        "tiến sĩ Lê Minh Tuấn",
        "cô Phạm Thu Hà",
        "Mr. John Smith",
        "Dr. Nguyễn Xuân Sơn",
        "   anh   Phạm   Văn   Đức   ",
        "chị em Nguyễn Thị Mai",
        "Bà Lê Thị Lan",
        "Giám đốc Hoàng Minh Quân"
    ]
    
    print("=== TEST VIETNAMESE NAME NORMALIZER ===")
    print(f"{'Raw Name':<30} | {'Clean Name':<25} | {'First Name':<15}")
    print("-" * 75)
    
    for name in test_names:
        clean_name = normalizer.clean_name(name)
        first_name = normalizer.extract_first_name(clean_name)
        is_valid = normalizer.validate_name(clean_name)
        
        print(f"{name:<30} | {clean_name:<25} | {first_name:<15} | {'✓' if is_valid else '✗'}")