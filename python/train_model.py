#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huấn luyện mô hình LSTM cho dự đoán giới tính từ tên tiếng Việt
LSTM model training for Vietnamese name to gender prediction
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
import os
from data_preprocessing import VietnameseNamePreprocessor

class VietnameseNameModel:
    """Lớp mô hình dự đoán giới tính từ tên tiếng Việt"""
    
    def __init__(self, max_length=28, vocab_size=8218):
        self.max_length = max_length
        self.vocab_size = vocab_size
        self.model = None
        self.history = None
        
    def build_model(self, embedding_dim=64, lstm_units=128, dropout_rate=0.5):
        """Xây dựng mô hình LSTM"""
        model = Sequential([
            Embedding(self.vocab_size, embedding_dim, input_length=self.max_length),
            LSTM(lstm_units, dropout=dropout_rate, recurrent_dropout=dropout_rate),
            Dense(64, activation='relu'),
            Dropout(dropout_rate),
            Dense(32, activation='relu'),
            Dropout(dropout_rate),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_test, y_test, epochs=100, batch_size=32):
        """Huấn luyện mô hình"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        callbacks = [
            ModelCheckpoint('../models/best_model.h5', monitor='val_accuracy', 
                          save_best_only=True, mode='max', verbose=1),
            EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)
        ]
        
        # Huấn luyện
        print("Bắt đầu huấn luyện mô hình...")
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        print("Hoàn thành huấn luyện!")
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Đánh giá mô hình"""
        if self.model is None:
            print("Mô hình chưa được huấn luyện!")
            return
        
        # Dự đoán
        y_pred = self.model.predict(X_test)
        y_pred_binary = (y_pred > 0.5).astype(int).flatten()
        
        # Đánh giá
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\nĐộ chính xác trên tập kiểm tra: {accuracy:.4f}")
        print(f"Loss trên tập kiểm tra: {loss:.4f}")
        
        # Classification report
        print("\nBáo cáo phân loại:")
        print(classification_report(y_test, y_pred_binary, 
                                  target_names=['Nữ', 'Nam']))
        
        # Confusion matrix
        print("\nMa trận nhầm lẫn:")
        cm = confusion_matrix(y_test, y_pred_binary)
        print(cm)
        
        return accuracy, loss
    
    def plot_training_history(self):
        """Vẽ biểu đồ quá trình huấn luyện"""
        if self.history is None:
            print("Chưa có lịch sử huấn luyện!")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Độ chính xác theo epoch')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Loss theo epoch')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('../models/training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self, filepath):
        """Lưu mô hình"""
        if self.model is None:
            print("Mô hình chưa được xây dựng!")
            return
        
        self.model.save(filepath)
        print(f"Đã lưu mô hình vào {filepath}")
    
    def load_model(self, filepath):
        """Tải mô hình"""
        self.model = tf.keras.models.load_model(filepath)
        print(f"Đã tải mô hình từ {filepath}")
    
    def predict_single(self, preprocessor, name):
        """Dự đoán giới tính cho một tên"""
        if self.model is None:
            print("Mô hình chưa được tải!")
            return None
        
        # Tiền xử lý tên
        processed_name = preprocessor.predict_preprocess(name)
        
        # Dự đoán
        prediction = self.model.predict(np.array([processed_name]))[0][0]
        
        # Chuyển đổi kết quả
        gender = 'Nam' if prediction > 0.5 else 'Nữ'
        confidence = prediction if prediction > 0.5 else 1 - prediction
        
        return gender, confidence

def main():
    """Hàm chính để huấn luyện mô hình"""
    # Tạo thư mục models nếu chưa có
    os.makedirs('../models', exist_ok=True)
    
    # Tải dữ liệu đã xử lý
    print("Tải dữ liệu đã xử lý...")
    try:
        data = np.load('../models/dataset_processed.npz')
        X_train, X_test = data['X_train'], data['X_test']
        y_train, y_test = data['y_train'], data['y_test']
        print(f"Đã tải dữ liệu: {X_train.shape[0]} mẫu huấn luyện, {X_test.shape[0]} mẫu kiểm tra")
    except FileNotFoundError:
        print("Không tìm thấy dữ liệu đã xử lý. Chạy data_preprocessing.py trước.")
        return
    
    # Tạo và huấn luyện mô hình
    print("\nTạo mô hình...")
    model = VietnameseNameModel()
    model.build_model()
    print(model.model.summary())
    
    # Huấn luyện
    print("\nBắt đầu huấn luyện...")
    history = model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=64)
    
    # Đánh giá
    print("\nĐánh giá mô hình...")
    accuracy, loss = model.evaluate(X_test, y_test)
    
    # Vẽ biểu đồ
    print("\nVẽ biểu đồ quá trình huấn luyện...")
    model.plot_training_history()
    
    # Lưu mô hình
    print("\nLưu mô hình...")
    model.save_model('../models/vietnamese_name_gender_model.h5')
    
    # Test dự đoán
    print("\nTest dự đoán...")
    preprocessor = VietnameseNamePreprocessor.load_preprocessor('../models/preprocessor.pkl')
    
    test_names = ['Nguyễn Văn Nam', 'Trần Thị Hoa', 'Lê Minh Tuấn', 'Phạm Thu Hà']
    for name in test_names:
        gender, confidence = model.predict_single(preprocessor, name)
        print(f"{name}: {gender} (độ tin cậy: {confidence:.2f})")

if __name__ == "__main__":
    main()