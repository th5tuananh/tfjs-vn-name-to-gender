#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tiền xử lý dữ liệu cho mô hình dự đoán giới tính từ tên tiếng Việt
Data preprocessing for Vietnamese name to gender prediction model
"""

import csv
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

class VietnameseNamePreprocessor:
    """Lớp tiền xử lý dữ liệu tên tiếng Việt"""
    
    def __init__(self, max_length=28):
        self.max_length = max_length
        self.label_encoder = LabelEncoder()
        
    def load_data(self, csv_file_path):
        """Tải dữ liệu từ file CSV"""
        try:
            data = pd.read_csv(csv_file_path, header=None, names=['name', 'gender'])
            print(f"Đã tải {len(data)} mẫu dữ liệu")
            return data
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            return None
    
    def text_to_sequence(self, name):
        """Chuyển đổi tên thành chuỗi số (character encoding)"""
        name = name.lower().strip()
        sequence = [ord(char) for char in name]
        return sequence
    
    def preprocess_names(self, names):
        """Tiền xử lý danh sách tên"""
        sequences = []
        for name in names:
            seq = self.text_to_sequence(name)
            sequences.append(seq)
        
        # Padding sequences to max_length
        padded_sequences = pad_sequences(sequences, maxlen=self.max_length, padding='pre')
        return padded_sequences
    
    def preprocess_labels(self, labels):
        """Tiền xử lý nhãn giới tính"""
        # Chuyển đổi f/m thành 0/1
        encoded_labels = self.label_encoder.fit_transform(labels)
        return encoded_labels
    
    def prepare_dataset(self, csv_file_path, test_size=0.2, random_state=42):
        """Chuẩn bị dataset hoàn chỉnh"""
        # Tải dữ liệu
        data = self.load_data(csv_file_path)
        if data is None:
            return None
        
        # Tiền xử lý
        X = self.preprocess_names(data['name'].values)
        y = self.preprocess_labels(data['gender'].values)
        
        # Chia train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Dữ liệu huấn luyện: {len(X_train)} mẫu")
        print(f"Dữ liệu kiểm tra: {len(X_test)} mẫu")
        print(f"Tỷ lệ giới tính trong dữ liệu huấn luyện:")
        print(f"  - Nam (1): {np.sum(y_train == 1)} mẫu")
        print(f"  - Nữ (0): {np.sum(y_train == 0)} mẫu")
        
        return X_train, X_test, y_train, y_test
    
    def save_preprocessor(self, file_path):
        """Lưu preprocessor để sử dụng sau"""
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_preprocessor(file_path):
        """Tải preprocessor đã lưu"""
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    def predict_preprocess(self, name):
        """Tiền xử lý một tên để dự đoán"""
        sequence = self.text_to_sequence(name)
        padded_sequence = pad_sequences([sequence], maxlen=self.max_length, padding='pre')
        return padded_sequence[0]

if __name__ == "__main__":
    # Ví dụ sử dụng
    preprocessor = VietnameseNamePreprocessor()
    
    # Chuẩn bị dataset
    X_train, X_test, y_train, y_test = preprocessor.prepare_dataset('../dataset.csv')
    
    if X_train is not None:
        print(f"\nKích thước dữ liệu:")
        print(f"X_train shape: {X_train.shape}")
        print(f"X_test shape: {X_test.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"y_test shape: {y_test.shape}")
        
        # Lưu preprocessor
        preprocessor.save_preprocessor('../models/preprocessor.pkl')
        print("\nĐã lưu preprocessor vào models/preprocessor.pkl")
        
        # Lưu dữ liệu đã xử lý
        np.savez('../models/dataset_processed.npz', 
                X_train=X_train, X_test=X_test, 
                y_train=y_train, y_test=y_test)
        print("Đã lưu dữ liệu đã xử lý vào models/dataset_processed.npz")