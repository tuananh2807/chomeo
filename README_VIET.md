# Web nhận diện chó mèo (CNN + Flask + SQL Server)

## 1) Chức năng chính
- Tải ảnh chó/mèo từ máy tính (Drag & Drop hoặc click chọn).
- Dự đoán kết quả: **Chó** hoặc **Mèo** bằng mô hình CNN.
- Hiển thị ảnh đã upload + độ tin cậy trực quan (thanh progress bar).
- Phân quyền theo đúng bảng vai trò: Khách / Người dùng / Admin.
- Lưu lịch sử nhận diện cho Người dùng.
- Giao diện **Premium Dark Mode** với Glassmorphism.

## 2) Công nghệ
- **Backend:** Python Flask
- **AI/ML:** TensorFlow/Keras (CNN)
- **Database:** SQL Server + pyodbc
- **Frontend:** HTML5, CSS3 (Dark Glassmorphism), JavaScript (Drag-Drop, Preview)
- **Đánh giá:** scikit-learn, Matplotlib, Seaborn

## 3) Cấu hình SQL Server
Mặc định trong `cau_hinh.py`:
- Tài khoản: `sa`
- Mật khẩu: `1234`
- CSDL: `NhanDienChoMeo`
- Server: `localhost`

Bạn có thể sửa qua biến môi trường:
- `MAY_CHU_SQL`
- `TEN_CO_SO_DU_LIEU`
- `TAI_KHOAN_SQL`
- `MAT_KHAU_SQL`

## 4) Cài đặt
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r yeu_cau.txt
```

## 5) Chuẩn bị dữ liệu huấn luyện
Tạo thư mục theo cấu trúc:

```
du_lieu_huan_luyen/
  train/
    cho/     ← ảnh chó train
    meo/     ← ảnh mèo train
  val/
    cho/     ← ảnh chó validation
    meo/     ← ảnh mèo validation
```

## 6) Huấn luyện mô hình CNN
```bash
python huan_luyen_mo_hinh.py
```
Kết quả:
- Mô hình: `mo_hinh/phan_loai_cho_meo.keras`
- Lịch sử: `mo_hinh/lich_su_huan_luyen.json`

## 7) Đánh giá mô hình (Chương 4)
```bash
python danh_gia_mo_hinh.py
```
Tính: Accuracy, Precision, Recall, F1-Score, Confusion Matrix.
Kết quả lưu tại: `mo_hinh/ket_qua_danh_gia.json`

## 8) Trực quan hóa (Chương 3 & 4)
```bash
python truc_quan_hoa.py
```
Tạo biểu đồ tại `mo_hinh/bieu_do/`:
- `learning_curves.png` — Loss & Accuracy theo epoch
- `loss_chart.png` — Biểu đồ Loss riêng
- `accuracy_chart.png` — Biểu đồ Accuracy riêng
- `confusion_matrix.png` — Ma trận nhầm lẫn
- `bang_ket_qua.png` — Bảng tổng hợp kết quả

## 9) Chạy web
```bash
python ung_dung.py
```
Mở trình duyệt: `http://127.0.0.1:5000`

## 10) Tài khoản mặc định
Khi chạy lần đầu, hệ thống tự tạo:
- Tên đăng nhập: `admin`
- Mật khẩu: `admin123`
- Vai trò: `admin`

## 11) Quy trình viết báo cáo
### Chương 3 (Methodology):
1. Mô tả dữ liệu: nguồn Kaggle, cấu trúc train/val
2. Tiền xử lý: resize 160×160, normalize /255, data augmentation
3. Kiến trúc CNN: 3 Conv2D + MaxPooling → Flatten → Dense → Sigmoid
4. Loss: Binary Crossentropy, Optimizer: Adam

### Chương 4 (Results):
1. Chạy `python huan_luyen_mo_hinh.py` → huấn luyện + lưu history
2. Chạy `python danh_gia_mo_hinh.py` → lấy metrics
3. Chạy `python truc_quan_hoa.py` → tạo biểu đồ
4. Chèn biểu đồ từ `mo_hinh/bieu_do/` vào báo cáo

## 12) Lưu ý quyền theo bảng
- Admin **không** được upload/nhận diện/lưu lịch sử theo đúng yêu cầu bảng phân quyền.
- Người dùng có đầy đủ quyền nghiệp vụ nhận diện và quản lý lịch sử cá nhân.
- Khách chỉ được nhận diện nhanh, không lưu lịch sử.
