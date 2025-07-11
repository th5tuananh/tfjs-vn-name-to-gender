# Dự đoán Giới tính từ Tên Tiếng Việt

## Giới thiệu

Dự án này sử dụng AI để dự đoán giới tính từ tên tiếng Việt với độ chính xác lên đến 97%. Dự án cung cấp cả phiên bản **JavaScript (TensorFlow.js)** và **Python (TensorFlow/Keras)** để phù hợp với nhu cầu sử dụng khác nhau.

## Tính năng chính

- ✅ **Độ chính xác cao**: Đạt 97% trên tập dữ liệu 63,773 tên tiếng Việt
- ✅ **Hai phiên bản**: JavaScript (web) và Python (backend/research)
- ✅ **Dễ sử dụng**: Giao diện web và command line thân thiện
- ✅ **Mã nguồn mở**: Code rõ ràng, dễ hiểu và mở rộng
- ✅ **Hỗ trợ tiếng Việt**: Xử lý đầy đủ các ký tự có dấu

## Cấu trúc dự án

```
📁 tfjs-vn-name-to-gender/
├── 📁 python/                      # Phiên bản Python
│   ├── data_preprocessing.py       # Tiền xử lý dữ liệu
│   ├── train_model.py             # Huấn luyện mô hình
│   ├── predict.py                 # Dự đoán giới tính
│   ├── demo.py                    # Demo các tính năng
│   ├── requirements.txt           # Thư viện Python
│   └── README.md                  # Hướng dẫn Python
├── 📁 models/                      # Mô hình đã huấn luyện
│   ├── vietnamese_name_gender_model.h5  # Mô hình Python
│   ├── preprocessor.pkl                 # Preprocessor
│   └── dataset_processed.npz            # Dữ liệu đã xử lý
├── 📁 js/                          # JavaScript cho web
│   ├── main.js                     # Giao diện web
│   └── nui.js                      # Logic dự đoán
├── 📁 model/ & model_v2/          # Mô hình TensorFlow.js
├── 📄 dataset.csv                  # Dữ liệu gốc (63,773 tên)
├── 📄 index.html                   # Giao diện web
├── 📄 LSTM.ipynb                   # Notebook huấn luyện gốc
└── 📄 README-VI.md                 # Hướng dẫn này
```

## Cách sử dụng

### 🌐 Phiên bản Web (JavaScript)

1. **Mở trực tiếp**: Mở file `index.html` trong trình duyệt
2. **Nhập tên**: Gõ tên tiếng Việt vào ô input
3. **Xem kết quả**: Nhấn "Dự đoán" để xem giới tính

### 🐍 Phiên bản Python

#### Cài đặt nhanh:
```bash
# Clone repository
git clone https://github.com/th5tuananh/tfjs-vn-name-to-gender.git
cd tfjs-vn-name-to-gender

# Cài đặt Python packages
cd python
pip install -r requirements.txt

# Dự đoán một tên
python predict.py --name "Nguyễn Văn Nam"

# Chế độ tương tác
python predict.py --interactive
```

#### Kết quả mẫu:
```
Tên: Nguyễn Văn Nam
Giới tính: Nam
Độ tin cậy: 100.00%
```

### 📊 Huấn luyện mô hình mới

```bash
# Tiền xử lý dữ liệu
python data_preprocessing.py

# Huấn luyện mô hình
python train_model.py

# Test mô hình
python predict.py --name "Tên của bạn"
```

## Ví dụ sử dụng

### 🎯 Dự đoán đơn lẻ
```bash
python predict.py --name "Trần Thị Hoa"
# Kết quả: Nữ (100.00%)
```

### 📝 Dự đoán hàng loạt
```bash
# Tạo file danh_sach.txt với các tên
python predict.py --file danh_sach.txt
```

### 🔄 Chế độ tương tác
```bash
python predict.py --interactive
# Nhập tên liên tục để dự đoán
```

## Kết quả thực tế

| Tên | Giới tính dự đoán | Độ tin cậy |
|-----|-------------------|------------|
| Nguyễn Văn Nam | Nam | 100.00% |
| Trần Thị Hoa | Nữ | 100.00% |
| Lê Minh Tuấn | Nam | 100.00% |
| Phạm Thu Hà | Nữ | 99.99% |
| Vũ Hoàng Anh | Nam | 88.95% |
| Đỗ Thị Linh | Nữ | 100.00% |

## Công nghệ sử dụng

### 🔧 Phiên bản JavaScript
- **TensorFlow.js**: Chạy AI trên trình duyệt
- **HTML/CSS/JS**: Giao diện web đơn giản
- **Character-level LSTM**: Phân tích từng ký tự

### 🔧 Phiên bản Python
- **TensorFlow/Keras**: Framework deep learning
- **LSTM**: Mạng nơ-ron nhớ dài hạn
- **Scikit-learn**: Xử lý dữ liệu
- **Pandas**: Phân tích dữ liệu

## Mở rộng và tùy chỉnh

### 📈 Cải thiện độ chính xác

1. **Thêm dữ liệu**: Bổ sung tên từ các nguồn khác
2. **Cân bằng dữ liệu**: Đảm bảo tỷ lệ nam/nữ phù hợp
3. **Tăng cường dữ liệu**: Tạo biến thể của tên
4. **Tinh chỉnh mô hình**: Thay đổi architecture và hyperparameters

### 🛠️ Tùy chỉnh mô hình

```python
# Trong train_model.py
model.build_model(
    embedding_dim=64,    # Tăng để học đặc trưng phức tạp hơn
    lstm_units=128,      # Tăng để tăng sức mạnh mô hình
    dropout_rate=0.3     # Giảm để tăng khả năng học
)
```

### 📊 Tích hợp vào ứng dụng

```python
# Sử dụng trong code Python
from predict import VietnameseNamePredictor

predictor = VietnameseNamePredictor()
predictor.load_model()

gender, confidence = predictor.predict_single("Nguyễn Văn A")
print(f"Giới tính: {gender}, Độ tin cậy: {confidence:.2%}")
```

## Yêu cầu hệ thống

### 🌐 Phiên bản Web
- **Trình duyệt**: Chrome/Firefox/Safari/Edge hiện đại
- **Kết nối**: Không cần internet (chạy offline)

### 🐍 Phiên bản Python
- **Python**: 3.7+
- **RAM**: 4GB+ (khuyến nghị 8GB)
- **Ổ cứng**: 1GB trống
- **GPU**: Tùy chọn (tăng tốc huấn luyện)

## Xử lý lỗi

### ❌ Lỗi thường gặp và giải pháp

1. **Không tìm thấy mô hình**
   ```bash
   python train_model.py  # Tạo mô hình mới
   ```

2. **Lỗi encoding**
   ```bash
   # Đảm bảo file CSV có encoding UTF-8
   ```

3. **Thiếu thư viện**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lỗi CUDA** (chỉ cảnh báo)
   ```
   # Mô hình vẫn chạy bình thường trên CPU
   ```

## Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! 🤝

- 🐛 **Báo cáo lỗi**: Tạo issue trên GitHub
- 💡 **Đề xuất tính năng**: Chia sẻ ý tưởng
- 🔧 **Đóng góp code**: Tạo pull request  
- 📊 **Chia sẻ dữ liệu**: Cung cấp thêm tên tiếng Việt

## Tác giả

👨‍💻 **Nguyễn Xuân Sơn (ngxson)**
- 📧 Email: contact@ngxson.com
- 🌐 Website: https://ngxson.com
- 🐙 GitHub: @ngxson

## Giấy phép

Dự án này được phát hành dưới [MIT License](LICENSE).

## Tham khảo

- [TensorFlow.js Documentation](https://www.tensorflow.org/js)
- [TensorFlow/Keras Documentation](https://www.tensorflow.org/)
- [LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Vietnamese NLP](https://github.com/undertheseanlp/underthesea)

---

⭐ **Nếu dự án hữu ích, hãy cho chúng tôi 1 star trên GitHub!**

*Dự án này được tạo ra với mục đích học tập và nghiên cứu. Kết quả dự đoán chỉ mang tính chất tham khảo.*