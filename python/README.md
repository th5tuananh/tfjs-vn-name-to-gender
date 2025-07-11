# Dự đoán Giới tính từ Tên Tiếng Việt - Phiên bản Python

## Giới thiệu

Đây là phiên bản Python của dự án dự đoán giới tính từ tên tiếng Việt sử dụng TensorFlow/Keras. Dự án này sử dụng mô hình LSTM (Long Short-Term Memory) để phân loại giới tính dựa trên tên tiếng Việt với độ chính xác lên đến 97%.

## Tính năng chính

- **Tiền xử lý dữ liệu**: Chuyển đổi tên tiếng Việt thành chuỗi số để đưa vào mô hình
- **Mô hình LSTM**: Sử dụng mạng nơ-ron LSTM để học patterns trong tên tiếng Việt
- **Dự đoán tương tác**: Giao diện dòng lệnh thân thiện cho việc dự đoán
- **Xử lý hàng loạt**: Hỗ trợ dự đoán cho nhiều tên cùng lúc
- **Dễ mở rộng**: Cấu trúc code rõ ràng, dễ dàng thêm dữ liệu hoặc cải tiến mô hình

## Cấu trúc dự án

```
python/
├── data_preprocessing.py    # Tiền xử lý dữ liệu
├── train_model.py          # Huấn luyện mô hình
├── predict.py              # Dự đoán giới tính
├── requirements.txt        # Danh sách thư viện cần thiết
└── README.md              # Hướng dẫn sử dụng

models/                    # Thư mục chứa mô hình đã huấn luyện
├── vietnamese_name_gender_model.h5  # Mô hình TensorFlow
├── preprocessor.pkl                 # Preprocessor đã lưu
├── dataset_processed.npz            # Dữ liệu đã xử lý
└── training_history.png             # Biểu đồ quá trình huấn luyện

dataset.csv               # Dữ liệu gốc (63,773 tên tiếng Việt)
```

## Cài đặt

### 1. Cài đặt Python

Đảm bảo bạn đã cài đặt Python 3.7 trở lên:

```bash
python --version
```

### 2. Cài đặt thư viện

```bash
cd python
pip install -r requirements.txt
```

### 3. Chuẩn bị dữ liệu

Dữ liệu đã có sẵn trong file `dataset.csv` với 63,773 tên tiếng Việt. Nếu bạn muốn sử dụng dữ liệu khác, hãy đảm bảo định dạng CSV như sau:

```csv
tên,giới_tính
nguyễn văn nam,m
trần thị hoa,f
```

## Sử dụng

### 1. Tiền xử lý dữ liệu

```bash
cd python
python data_preprocessing.py
```

Lệnh này sẽ:
- Tải dữ liệu từ `dataset.csv`
- Chuyển đổi tên thành chuỗi số
- Chia dữ liệu thành tập huấn luyện và kiểm tra
- Lưu dữ liệu đã xử lý vào `models/`

### 2. Huấn luyện mô hình

```bash
python train_model.py
```

Quá trình huấn luyện bao gồm:
- Xây dựng mô hình LSTM
- Huấn luyện với callbacks (Early Stopping, Model Checkpoint)
- Đánh giá mô hình trên tập kiểm tra
- Lưu mô hình tốt nhất
- Tạo biểu đồ quá trình huấn luyện

### 3. Dự đoán giới tính

#### Dự đoán một tên:
```bash
python predict.py --name "Nguyễn Văn Nam"
```

#### Dự đoán từ file:
```bash
python predict.py --file danh_sach_ten.txt
```

#### Chế độ tương tác:
```bash
python predict.py --interactive
```

## Ví dụ sử dụng

### Dự đoán đơn lẻ:
```bash
$ python predict.py --name "Trần Thị Hoa"
Tên: Trần Thị Hoa
Giới tính: Nữ
Độ tin cậy: 95.67%
```

### Chế độ tương tác:
```bash
$ python predict.py --interactive
=== DỰ ĐOÁN GIỚI TÍNH TỪ TÊN TIẾNG VIỆT ===
Nhập tên để dự đoán giới tính (hoặc 'quit' để thoát)
Ví dụ: Nguyễn Văn Nam, Trần Thị Hoa
--------------------------------------------------

Nhập tên: Lê Minh Tuấn
Kết quả: Lê Minh Tuấn -> Nam
Độ tin cậy: 92.34%
(Rất chắc chắn)

Nhập tên: Phạm Thu Hà
Kết quả: Phạm Thu Hà -> Nữ
Độ tin cậy: 88.91%
(Khá chắc chắn)
```

## Tùy chỉnh và mở rộng

### Thêm dữ liệu mới

1. Thêm tên mới vào `dataset.csv` theo định dạng:
   ```csv
   tên_mới,giới_tính
   ```

2. Chạy lại tiền xử lý và huấn luyện:
   ```bash
   python data_preprocessing.py
   python train_model.py
   ```

### Tùy chỉnh mô hình

Bạn có thể tùy chỉnh các tham số trong `train_model.py`:

```python
# Tùy chỉnh kiến trúc mô hình
model.build_model(
    embedding_dim=64,    # Kích thước embedding
    lstm_units=128,      # Số units LSTM
    dropout_rate=0.5     # Tỷ lệ dropout
)

# Tùy chỉnh huấn luyện
model.train(
    X_train, y_train, X_test, y_test,
    epochs=50,      # Số epoch
    batch_size=64   # Kích thước batch
)
```

### Tăng cường dữ liệu

Để cải thiện độ chính xác, bạn có thể:

1. **Thêm nhiều dữ liệu hơn**: Thu thập thêm tên tiếng Việt từ các nguồn khác
2. **Cân bằng dữ liệu**: Đảm bảo tỷ lệ nam/nữ cân bằng
3. **Làm sạch dữ liệu**: Loại bỏ các tên có lỗi chính tả hoặc không phù hợp
4. **Tăng cường dữ liệu**: Tạo các biến thể của tên (có dấu/không dấu, viết hoa/thường)

## Yêu cầu hệ thống

- **Python**: 3.7+
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB)
- **Ổ cứng**: 1GB trống
- **GPU**: Tùy chọn (để tăng tốc huấn luyện)

## Xử lý lỗi thường gặp

### 1. Lỗi không tìm thấy mô hình
```bash
FileNotFoundError: [Errno 2] No such file or directory: '../models/vietnamese_name_gender_model.h5'
```

**Giải pháp**: Chạy `python train_model.py` để tạo mô hình trước.

### 2. Lỗi encoding
```bash
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**Giải pháp**: Đảm bảo file CSV được lưu với encoding UTF-8.

### 3. Lỗi thiếu thư viện
```bash
ModuleNotFoundError: No module named 'tensorflow'
```

**Giải pháp**: Cài đặt thư viện: `pip install -r requirements.txt`

## Đóng góp

Chúng tôi rất hoan nghênh các đóng góp từ cộng đồng! Bạn có thể:

1. **Báo cáo lỗi**: Tạo issue trên GitHub
2. **Đề xuất tính năng**: Chia sẻ ý tưởng cải tiến
3. **Đóng góp code**: Tạo pull request
4. **Chia sẻ dữ liệu**: Cung cấp thêm tên tiếng Việt

## Licen

Dự án này được phát hành dưới [MIT License](LICENSE).

## Tác giả

- **Nguyễn Xuân Sơn (ngxson)**
- Email: contact@ngxson.com
- Website: https://ngxson.com

## Tham khảo

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras LSTM Guide](https://keras.io/api/layers/recurrent_layers/lstm/)
- [Vietnamese Name Dataset](https://github.com/th5tuananh/tfjs-vn-name-to-gender)

---

*Dự án này được tạo ra với mục đích học tập và nghiên cứu. Kết quả dự đoán chỉ mang tính chất tham khảo.*