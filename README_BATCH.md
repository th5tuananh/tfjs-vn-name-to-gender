# Hướng dẫn sử dụng tính năng Batch Predict CSV

## Giới thiệu

Tính năng **Batch Predict CSV** cho phép bạn dự đoán giới tính hàng loạt từ file CSV chứa danh sách tên tiếng Việt. Tính năng này tự động:

- ✅ **Loại bỏ xưng hô**: Tự động nhận diện và loại bỏ các từ xưng hô như "anh", "chị", "bác sĩ", "tiến sĩ", v.v.
- ✅ **Chuẩn hóa tên**: Chuyển đổi về chữ thường, loại bỏ ký tự đặc biệt, chuẩn hóa khoảng trắng
- ✅ **Dự đoán giới tính**: Sử dụng mô hình AI với độ chính xác 97% để dự đoán giới tính
- ✅ **Xuất kết quả CSV**: Tạo file CSV với các cột `raw_name`, `clean_name`, `gender_pred`
- ✅ **Thống kê chi tiết**: Tạo báo cáo thống kê về độ tin cậy và phân bố giới tính

## Cài đặt

### 1. Cài đặt các thư viện cần thiết

```bash
cd python
pip install -r requirements.txt
```

### 2. Kiểm tra mô hình

Đảm bảo mô hình đã được huấn luyện và lưu trong thư mục `models/`:

```bash
ls -la ../models/
# Cần có:
# - vietnamese_name_gender_model.h5
# - preprocessor.pkl (sẽ được tạo tự động nếu chưa có)
```

## Sử dụng cơ bản

### Cú pháp cơ bản

```bash
python batch_csv_predict.py -i <file_input.csv> -o <file_output.csv>
```

### Ví dụ đơn giản

```bash
python batch_csv_predict.py -i danh_sach_ten.csv -o ket_qua.csv
```

## Định dạng file đầu vào

### Định dạng CSV chuẩn

File CSV đầu vào cần có ít nhất 1 cột chứa tên. Ví dụ:

```csv
name
anh Hiếu
Chị Thương
bác sĩ Trần Thị Hoa
Nguyễn Văn Nam
tiến sĩ Lê Minh Tuấn
```

### Định dạng với nhiều cột

```csv
id,ho_ten,tuoi,dia_chi
1,anh Phạm Văn Đức,25,Hà Nội
2,chị Nguyễn Thị Mai,30,TP.HCM
3,Dr. Lê Minh Tuấn,35,Đà Nẵng
```

## Tùy chọn nâng cao

### Chỉ định cột tên

```bash
python batch_csv_predict.py -i data.csv -o results.csv -c "ho_ten"
```

### Chỉ định encoding

```bash
python batch_csv_predict.py -i data.csv -o results.csv -e "utf-8"
```

### Chỉ định đường dẫn mô hình

```bash
python batch_csv_predict.py -i data.csv -o results.csv -m "../models/custom_model.h5"
```

### Tham số đầy đủ

```bash
python batch_csv_predict.py \
  --input danh_sach_ten.csv \
  --output ket_qua.csv \
  --column "Họ tên" \
  --encoding utf-8 \
  --model ../models/vietnamese_name_gender_model.h5 \
  --preprocessor ../models/preprocessor.pkl
```

## Định dạng kết quả

### File CSV kết quả

File kết quả sẽ có các cột sau:

| Cột | Mô tả | Ví dụ |
|-----|-------|-------|
| `raw_name` | Tên gốc từ file đầu vào | "anh Hiếu" |
| `clean_name` | Tên đã chuẩn hóa | "hiếu" |
| `gender_pred` | Giới tính dự đoán | "Nam" hoặc "Nữ" |
| `confidence` | Độ tin cậy (0-1) | 0.9838 |
| `status` | Trạng thái xử lý | "Success" |

### Ví dụ kết quả

```csv
raw_name,clean_name,gender_pred,confidence,status
anh Hiếu,hiếu,Nam,0.8838021,Success
Chị Thương,thương,Nam,0.9196607,Success
bác sĩ Trần Thị Hoa,trần thị hoa,Nữ,1.0,Success
Nguyễn Văn Nam,nguyễn văn nam,Nam,0.9999999,Success
```

### File thống kê

Hệ thống tự động tạo file thống kê `<tên_file_kết_quả>_stats.txt`:

```
=== THỐNG KÊ DỰ ĐOÁN GIỚI TÍNH ===
Ngày thực hiện: 2025-07-11 09:03:58
File kết quả: ket_qua.csv

Tổng quan:
- Tổng số tên: 100
- Dự đoán thành công: 98 (98.0%)
- Dự đoán thất bại: 2 (2.0%)

Phân bố giới tính:
- Nam: 55 (55.0%)
- Nữ: 43 (43.0%)
- Không xác định: 2 (2.0%)

Độ tin cậy:
- Độ tin cậy trung bình: 95.80%
- Độ tin cậy cao (>90%): 85 (86.7%)
- Độ tin cậy trung bình (70-90%): 13 (13.3%)
- Độ tin cậy thấp (<70%): 0 (0.0%)
```

## Xưng hô được hỗ trợ

Hệ thống tự động loại bỏ các xưng hô sau:

### Xưng hô thông thường
- `anh`, `chị`, `em`, `bác`, `cô`, `chú`, `dì`, `thím`
- `ông`, `bà`, `cụ`, `thầy`, `giáo`, `sư`

### Học hàm, học vị
- `tiến sĩ`, `tiến sỹ`, `ts`, `th.s`, `ths`
- `bác sĩ`, `bs`, `kỹ sư`, `ks`, `luật sư`, `ls`

### Chức vụ
- `giám đốc`, `gđ`, `phó giám đốc`, `pgđ`
- `trưởng phòng`, `tp`, `phó trưởng phòng`, `ptp`

### Xưng hô tiếng Anh
- `mr`, `mrs`, `miss`, `ms`, `dr`, `prof`, `professor`

## Ví dụ sử dụng thực tế

### Ví dụ 1: Danh sách nhân viên

**File đầu vào** (`nhan_vien.csv`):
```csv
ma_nv,ho_ten,phong_ban
NV001,anh Nguyễn Văn Nam,IT
NV002,chị Trần Thị Hoa,HR
NV003,bác sĩ Lê Minh Tuấn,Y tế
NV004,kỹ sư Phạm Văn Đức,Kỹ thuật
```

**Lệnh thực thi**:
```bash
python batch_csv_predict.py -i nhan_vien.csv -o nhan_vien_ket_qua.csv -c "ho_ten"
```

**Kết quả**:
```csv
raw_name,clean_name,gender_pred,confidence,status
anh Nguyễn Văn Nam,nguyễn văn nam,Nam,0.9999999,Success
chị Trần Thị Hoa,trần thị hoa,Nữ,1.0,Success
bác sĩ Lê Minh Tuấn,lê minh tuấn,Nam,0.9999838,Success
kỹ sư Phạm Văn Đức,phạm văn đức,Nam,0.9999998,Success
```

### Ví dụ 2: Danh sách khách hàng

**File đầu vào** (`khach_hang.csv`):
```csv
Khách hàng,Số điện thoại,Địa chỉ
Dr. Nguyễn Xuân Sơn,0987654321,Hà Nội
Bà Lê Thị Lan,0976543210,TP.HCM
Giám đốc Hoàng Minh Quân,0965432109,Đà Nẵng
```

**Lệnh thực thi**:
```bash
python batch_csv_predict.py -i khach_hang.csv -o khach_hang_ket_qua.csv -c "Khách hàng"
```

### Ví dụ 3: Xử lý file lớn

Đối với file có hàng ngàn hoặc hàng chục ngàn tên:

```bash
python batch_csv_predict.py -i danh_sach_lon.csv -o ket_qua_lon.csv
```

Hệ thống sẽ hiển thị tiến trình xử lý:
```
2025-07-11 09:03:56 - INFO - Bắt đầu xử lý 5000 tên...
2025-07-11 09:03:58 - INFO - Đã xử lý 100/5000 tên (2.0%)
2025-07-11 09:04:00 - INFO - Đã xử lý 200/5000 tên (4.0%)
...
```

## Xử lý lỗi và khắc phục

### Lỗi encoding

**Lỗi**: `UnicodeDecodeError`

**Khắc phục**: Thử các encoding khác:
```bash
python batch_csv_predict.py -i data.csv -o results.csv -e "utf-8-sig"
python batch_csv_predict.py -i data.csv -o results.csv -e "cp1252"
```

### Lỗi không tìm thấy cột

**Lỗi**: Không tìm thấy cột tên

**Khắc phục**: Chỉ định rõ tên cột:
```bash
python batch_csv_predict.py -i data.csv -o results.csv -c "Họ và tên"
```

### Lỗi không tìm thấy mô hình

**Lỗi**: `FileNotFoundError: vietnamese_name_gender_model.h5`

**Khắc phục**: Tạo lại mô hình:
```bash
python train_model.py
```

### Lỗi dự đoán thất bại

Một số tên có thể không được dự đoán thành công. Kiểm tra:
- Tên có chứa ký tự đặc biệt không hợp lệ
- Tên có độ dài quá ngắn hoặc quá dài
- Tên chỉ chứa số

## Tối ưu hóa hiệu suất

### Đối với file lớn

1. **Tăng RAM**: Đảm bảo máy có đủ RAM (khuyến nghị 8GB+)
2. **Sử dụng SSD**: Lưu file trên ổ SSD để tăng tốc độ đọc/ghi
3. **Chia nhỏ file**: Với file quá lớn (>100k tên), chia thành nhiều file nhỏ

### Ví dụ chia nhỏ file

```bash
# Chia file lớn thành các file 10,000 dòng
split -l 10000 file_lon.csv file_nho_

# Xử lý từng file
python batch_csv_predict.py -i file_nho_aa -o ket_qua_01.csv
python batch_csv_predict.py -i file_nho_ab -o ket_qua_02.csv
```

## Tích hợp với hệ thống khác

### Sử dụng trong Python script

```python
from batch_csv_predict import BatchCSVPredictor

# Tạo processor
processor = BatchCSVPredictor()

# Xử lý file
success = processor.process_csv_file(
    input_file="input.csv",
    output_file="output.csv",
    name_column="ho_ten"
)

if success:
    print("Xử lý thành công!")
else:
    print("Xử lý thất bại!")
```

### Sử dụng trong shell script

```bash
#!/bin/bash

# Xử lý nhiều file cùng lúc
for file in *.csv; do
    output="result_${file}"
    python batch_csv_predict.py -i "$file" -o "$output"
    echo "Đã xử lý: $file -> $output"
done
```

## Câu hỏi thường gặp (FAQ)

### Q: Tại sao một số tên được dự đoán sai?

**A**: Mô hình có độ chính xác 97%, nghĩa là 3% trường hợp có thể dự đoán sai. Điều này xảy ra với:
- Tên hiếm, không có trong dữ liệu huấn luyện
- Tên có thể dùng cho cả nam và nữ
- Tên nước ngoài

### Q: Có thể thêm xưng hô mới không?

**A**: Có, chỉnh sửa file `name_normalizer.py`, thêm xưng hô vào danh sách `self.titles`.

### Q: Tại sao confidence thấp?

**A**: Confidence thấp (<70%) cho biết mô hình không chắc chắn về kết quả. Thường xảy ra với:
- Tên có thể dùng cho cả nam và nữ (như "Quỳnh", "Linh")
- Tên không phổ biến
- Tên có lỗi chính tả

### Q: Có thể xử lý tên nước ngoài không?

**A**: Mô hình được huấn luyện chủ yếu trên tên tiếng Việt. Tên nước ngoài có thể được xử lý nhưng độ chính xác thấp hơn.

### Q: File kết quả quá lớn, có thể nén không?

**A**: Có, sử dụng:
```bash
gzip ket_qua.csv
```

## Hỗ trợ và liên hệ

- **GitHub Issues**: [Báo cáo lỗi](https://github.com/th5tuananh/tfjs-vn-name-to-gender/issues)
- **Email**: contact@ngxson.com
- **Documentation**: [README chính](../README.md)

## Changelog

### v1.0.0 (2025-07-11)
- ✅ Tính năng batch predict từ CSV
- ✅ Loại bỏ xưng hô tự động
- ✅ Chuẩn hóa tên tiếng Việt
- ✅ Xuất kết quả CSV với thống kê
- ✅ Hỗ trợ nhiều encoding
- ✅ Xử lý lỗi và validation

---

*Tài liệu này được cập nhật thường xuyên. Vui lòng kiểm tra phiên bản mới nhất trên GitHub.*