# Hướng dẫn Nhanh - Vietnamese Name to Gender Prediction

## 🚀 Sử dụng ngay lập tức

### 1. Phiên bản Web (Không cần cài đặt)
```bash
# Mở trực tiếp file index.html trong trình duyệt
open index.html  # macOS
# hoặc double-click file index.html
```

### 2. Phiên bản Python (Cần cài đặt)

#### Cài đặt nhanh:
```bash
# Bước 1: Vào thư mục python
cd python

# Bước 2: Cài đặt thư viện
pip install -r requirements.txt

# Bước 3: Dự đoán ngay
python predict.py --name "Nguyễn Văn Nam"
```

#### Chế độ tương tác:
```bash
python predict.py --interactive
```

#### Dự đoán nhiều tên:
```bash
# Tạo file names.txt chứa danh sách tên
python predict.py --file names.txt
```

## 🔧 Huấn luyện mô hình mới

```bash
# Bước 1: Tiền xử lý dữ liệu
python data_preprocessing.py

# Bước 2: Huấn luyện (mất 10-30 phút)
python train_model.py

# Bước 3: Test mô hình
python predict.py --name "Tên của bạn"
```

## 📊 Kết quả mẫu

```
Tên: Nguyễn Văn Nam
Giới tính: Nam
Độ tin cậy: 100.00%

Tên: Trần Thị Hoa  
Giới tính: Nữ
Độ tin cậy: 100.00%
```

## ❓ Xử lý lỗi

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `ModuleNotFoundError` | Thiếu thư viện | `pip install -r requirements.txt` |
| `FileNotFoundError` | Thiếu mô hình | `python train_model.py` |
| `UnicodeDecodeError` | Sai encoding | Đảm bảo file UTF-8 |

## 💡 Mẹo sử dụng

1. **Tên càng đầy đủ, dự đoán càng chính xác**
2. **Hỗ trợ tên có dấu**: Nguyễn, Trần, Phạm, ...
3. **Phân biệt hoa/thường**: Không quan trọng
4. **Tên kép**: Hoạt động tốt với tên 2-3 từ

---

📖 **Hướng dẫn chi tiết**: [README-VI.md](README-VI.md)
🌐 **Demo trực tuyến**: Mở `index.html`
💻 **Source code**: [GitHub](https://github.com/th5tuananh/tfjs-vn-name-to-gender)