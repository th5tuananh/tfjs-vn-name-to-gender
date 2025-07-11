#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch CSV processing for Vietnamese name gender prediction
Xử lý batch dự đoán giới tính từ file CSV
"""

import pandas as pd
import numpy as np
import argparse
import sys
import os
from pathlib import Path
import csv
from datetime import datetime
import logging

# Import các module cần thiết
from predict import VietnameseNamePredictor
from name_normalizer import VietnameseNameNormalizer

class BatchCSVPredictor:
    """Lớp xử lý batch dự đoán giới tính từ file CSV"""
    
    def __init__(self, model_path='../models/vietnamese_name_gender_model.h5',
                 preprocessor_path='../models/preprocessor.pkl'):
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path
        self.model = None
        self.preprocessor = None
        self.normalizer = VietnameseNameNormalizer()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Thiết lập logger"""
        logger = logging.getLogger('BatchCSVPredictor')
        logger.setLevel(logging.INFO)
        
        # Tạo handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_model(self):
        """Tải mô hình và preprocessor"""
        try:
            # Tải mô hình
            import tensorflow as tf
            self.model = tf.keras.models.load_model(self.model_path)
            self.logger.info(f"Đã tải mô hình từ {self.model_path}")
            
            # Tạo preprocessor mới thay vì load từ file
            from data_preprocessing import VietnameseNamePreprocessor
            self.preprocessor = VietnameseNamePreprocessor()
            
            # Tải dữ liệu để fit preprocessor
            import pandas as pd
            # Try different possible paths for dataset
            dataset_paths = ['../dataset.csv', './dataset.csv', 'dataset.csv']
            data = None
            
            for path in dataset_paths:
                try:
                    data = pd.read_csv(path, header=None, names=['name', 'gender'])
                    break
                except FileNotFoundError:
                    continue
            
            if data is None:
                raise FileNotFoundError("Could not find dataset.csv in any of the expected locations")
            
            self.preprocessor.preprocess_labels(data['gender'].values)
            
            self.logger.info("Đã tạo preprocessor mới")
            
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi tải mô hình: {e}")
            return False
    
    def predict_single(self, name):
        """Dự đoán giới tính cho một tên"""
        if self.model is None or self.preprocessor is None:
            self.logger.error("Mô hình chưa được tải!")
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
            self.logger.error(f"Lỗi khi dự đoán: {e}")
            return None, None
    
    def load_csv_data(self, csv_file_path, name_column=None, encoding='utf-8'):
        """Tải dữ liệu từ file CSV"""
        try:
            # Thử đọc file với encoding được chỉ định
            df = pd.read_csv(csv_file_path, encoding=encoding)
            
            # Nếu không chỉ định cột tên, tự động tìm
            if name_column is None:
                # Tìm cột có thể chứa tên
                possible_name_columns = [
                    'name', 'tên', 'ten', 'full_name', 'fullname', 'họ_tên', 'ho_ten',
                    'Name', 'Tên', 'Ten', 'Full_Name', 'FullName', 'Họ_Tên', 'Ho_Ten'
                ]
                
                name_column = None
                for col in possible_name_columns:
                    if col in df.columns:
                        name_column = col
                        break
                
                # Nếu không tìm thấy, sử dụng cột đầu tiên
                if name_column is None:
                    name_column = df.columns[0]
                    
            self.logger.info(f"Đã tải {len(df)} dòng dữ liệu từ {csv_file_path}")
            self.logger.info(f"Sử dụng cột '{name_column}' làm cột tên")
            
            return df, name_column
            
        except UnicodeDecodeError:
            # Thử với encoding khác
            try:
                df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
                self.logger.info(f"Đã đọc file với encoding utf-8-sig")
                return df, name_column
            except:
                try:
                    df = pd.read_csv(csv_file_path, encoding='cp1252')
                    self.logger.info(f"Đã đọc file với encoding cp1252")
                    return df, name_column
                except:
                    self.logger.error(f"Không thể đọc file {csv_file_path}")
                    return None, None
                    
        except Exception as e:
            self.logger.error(f"Lỗi khi tải dữ liệu: {e}")
            return None, None
    
    def process_names(self, names, show_progress=True):
        """Xử lý danh sách tên"""
        results = []
        total = len(names)
        
        self.logger.info(f"Bắt đầu xử lý {total} tên...")
        
        for i, raw_name in enumerate(names):
            if show_progress and (i + 1) % 100 == 0:
                self.logger.info(f"Đã xử lý {i + 1}/{total} tên ({(i + 1)/total*100:.1f}%)")
            
            # Bước 1: Chuẩn hóa tên
            clean_name = self.normalizer.clean_name(raw_name) if raw_name else ""
            
            # Bước 2: Kiểm tra tên có hợp lệ không
            if not self.normalizer.validate_name(clean_name):
                results.append({
                    'raw_name': raw_name,
                    'clean_name': clean_name,
                    'gender_pred': 'Unknown',
                    'confidence': 0.0,
                    'status': 'Invalid name'
                })
                continue
            
            # Bước 3: Dự đoán giới tính
            gender, confidence = self.predict_single(clean_name)
            
            if gender is None:
                results.append({
                    'raw_name': raw_name,
                    'clean_name': clean_name,
                    'gender_pred': 'Unknown',
                    'confidence': 0.0,
                    'status': 'Prediction failed'
                })
            else:
                # Chuyển đổi giới tính sang tiếng Việt
                gender_vn = 'Nam' if gender == 'Nam' else 'Nữ'
                
                results.append({
                    'raw_name': raw_name,
                    'clean_name': clean_name,
                    'gender_pred': gender_vn,
                    'confidence': confidence,
                    'status': 'Success'
                })
        
        self.logger.info(f"Hoàn thành xử lý {total} tên")
        return results
    
    def save_results(self, results, output_file_path, include_stats=True):
        """Lưu kết quả vào file CSV"""
        try:
            # Tạo DataFrame
            df = pd.DataFrame(results)
            
            # Sắp xếp cột theo thứ tự mong muốn
            columns_order = ['raw_name', 'clean_name', 'gender_pred']
            if 'confidence' in df.columns:
                columns_order.append('confidence')
            if 'status' in df.columns:
                columns_order.append('status')
            
            df = df[columns_order]
            
            # Lưu file
            df.to_csv(output_file_path, index=False, encoding='utf-8')
            self.logger.info(f"Đã lưu kết quả vào {output_file_path}")
            
            if include_stats:
                self._save_statistics(results, output_file_path)
                
        except Exception as e:
            self.logger.error(f"Lỗi khi lưu kết quả: {e}")
    
    def _save_statistics(self, results, output_file_path):
        """Lưu thống kê vào file txt"""
        try:
            stats_file = output_file_path.replace('.csv', '_stats.txt')
            
            total = len(results)
            successful = sum(1 for r in results if r['status'] == 'Success')
            failed = total - successful
            
            male_count = sum(1 for r in results if r['gender_pred'] == 'Nam')
            female_count = sum(1 for r in results if r['gender_pred'] == 'Nữ')
            unknown_count = sum(1 for r in results if r['gender_pred'] == 'Unknown')
            
            # Tính confidence trung bình
            confidences = [r['confidence'] for r in results if r['status'] == 'Success']
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            stats_text = f"""
=== THỐNG KÊ DỰ ĐOÁN GIỚI TÍNH ===
Ngày thực hiện: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
File kết quả: {output_file_path}

Tổng quan:
- Tổng số tên: {total}
- Dự đoán thành công: {successful} ({successful/total*100:.1f}%)
- Dự đoán thất bại: {failed} ({failed/total*100:.1f}%)

Phân bố giới tính:
- Nam: {male_count} ({male_count/total*100:.1f}%)
- Nữ: {female_count} ({female_count/total*100:.1f}%)
- Không xác định: {unknown_count} ({unknown_count/total*100:.1f}%)

Độ tin cậy:
- Độ tin cậy trung bình: {avg_confidence:.2%}
- Độ tin cậy cao (>90%): {sum(1 for c in confidences if c > 0.9)} ({sum(1 for c in confidences if c > 0.9)/len(confidences)*100:.1f}% trong các dự đoán thành công)
- Độ tin cậy trung bình (70-90%): {sum(1 for c in confidences if 0.7 <= c <= 0.9)} ({sum(1 for c in confidences if 0.7 <= c <= 0.9)/len(confidences)*100:.1f}% trong các dự đoán thành công)
- Độ tin cậy thấp (<70%): {sum(1 for c in confidences if c < 0.7)} ({sum(1 for c in confidences if c < 0.7)/len(confidences)*100:.1f}% trong các dự đoán thành công)
""".strip()
            
            with open(stats_file, 'w', encoding='utf-8') as f:
                f.write(stats_text)
            
            self.logger.info(f"Đã lưu thống kê vào {stats_file}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lưu thống kê: {e}")
    
    def process_csv_file(self, input_file, output_file, name_column=None, encoding='utf-8'):
        """Xử lý file CSV hoàn chỉnh"""
        # Tải mô hình
        if not self.load_model():
            self.logger.error("Không thể tải mô hình!")
            return False
        
        # Tải dữ liệu
        df, name_column = self.load_csv_data(input_file, name_column, encoding)
        if df is None:
            return False
        
        # Lấy danh sách tên
        names = df[name_column].fillna('').astype(str).tolist()
        
        # Xử lý tên
        results = self.process_names(names)
        
        # Lưu kết quả
        self.save_results(results, output_file)
        
        return True

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(
        description='Dự đoán giới tính batch từ file CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python batch_csv_predict.py -i names.csv -o results.csv
  python batch_csv_predict.py -i names.csv -o results.csv -c "Họ tên"
  python batch_csv_predict.py -i names.csv -o results.csv -e cp1252
        """
    )
    
    parser.add_argument('-i', '--input', required=True, 
                        help='File CSV đầu vào chứa danh sách tên')
    parser.add_argument('-o', '--output', required=True,
                        help='File CSV đầu ra để lưu kết quả')
    parser.add_argument('-c', '--column', default=None,
                        help='Tên cột chứa tên (tự động tìm nếu không chỉ định)')
    parser.add_argument('-e', '--encoding', default='utf-8',
                        help='Encoding của file CSV (mặc định: utf-8)')
    parser.add_argument('-m', '--model', default='../models/vietnamese_name_gender_model.h5',
                        help='Đường dẫn tới mô hình')
    parser.add_argument('-p', '--preprocessor', default='../models/preprocessor.pkl',
                        help='Đường dẫn tới preprocessor')
    
    args = parser.parse_args()
    
    # Kiểm tra file đầu vào
    if not Path(args.input).exists():
        print(f"Lỗi: File đầu vào '{args.input}' không tồn tại!")
        return 1
    
    # Tạo thư mục đầu ra nếu cần
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Tạo processor
    processor = BatchCSVPredictor(args.model, args.preprocessor)
    
    # Xử lý file
    print(f"Bắt đầu xử lý file: {args.input}")
    success = processor.process_csv_file(
        args.input, 
        args.output, 
        args.column, 
        args.encoding
    )
    
    if success:
        print(f"Hoàn thành! Kết quả đã được lưu vào: {args.output}")
        return 0
    else:
        print("Xử lý thất bại!")
        return 1

if __name__ == "__main__":
    sys.exit(main())