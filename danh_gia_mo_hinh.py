
"""
Đánh giá mô hình CNN phân loại chó mèo.
Chạy sau khi huấn luyện để lấy số liệu cho Chương 4 (Kết quả thực nghiệm).

Cách chạy:
    python danh_gia_mo_hinh.py

Kết quả sẽ in ra:
    - Accuracy, Precision, Recall, F1-Score
    - Confusion Matrix
    - Lưu kết quả vào mo_hinh/ket_qua_danh_gia.json
"""
from __future__ import annotations

import json
import os

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from cau_hinh import DUONG_DAN_MO_HINH, KICH_THUOC_ANH, THU_MUC_GOC

THU_MUC_KIEM_TRA = os.path.join(THU_MUC_GOC, "du_lieu_huan_luyen", "val")
DUONG_DAN_KET_QUA = os.path.join(THU_MUC_GOC, "mo_hinh", "ket_qua_danh_gia.json")


def danh_gia() -> None:
    # 1. Tải mô hình
    print("=" * 60)
    print("ĐÁNH GIÁ MÔ HÌNH CNN - PHÂN LOẠI CHÓ MÈO")
    print("=" * 60)

    if not os.path.exists(DUONG_DAN_MO_HINH):
        print(f"Lỗi: Không tìm thấy mô hình tại {DUONG_DAN_MO_HINH}")
        print("Hãy chạy: python huan_luyen_mo_hinh.py trước.")
        return

    mo_hinh = load_model(DUONG_DAN_MO_HINH)
    print(f"Đã tải mô hình từ: {DUONG_DAN_MO_HINH}")

    # 2. Tải dữ liệu kiểm tra
    bo_tao = ImageDataGenerator(rescale=1.0 / 255)
    du_lieu_kiem_tra = bo_tao.flow_from_directory(
        THU_MUC_KIEM_TRA,
        target_size=KICH_THUOC_ANH,
        batch_size=32,
        class_mode="binary",
        classes=["cho", "meo"],
        shuffle=False,
    )

    print(f"Số lượng ảnh kiểm tra: {du_lieu_kiem_tra.samples}")
    print(f"Nhãn lớp: {du_lieu_kiem_tra.class_indices}")

    # 3. Dự đoán
    xac_suat = mo_hinh.predict(du_lieu_kiem_tra, verbose=1)
    du_doan = (xac_suat >= 0.5).astype(int).flatten()
    thuc_te = du_lieu_kiem_tra.classes

    # 4. Tính các chỉ số đánh giá
    do_chinh_xac = accuracy_score(thuc_te, du_doan)
    do_chinh_xac_duong = precision_score(thuc_te, du_doan, average="binary")
    do_nhay = recall_score(thuc_te, du_doan, average="binary")
    f1 = f1_score(thuc_te, du_doan, average="binary")
    ma_tran_nham_lan = confusion_matrix(thuc_te, du_doan)

    # 5. In kết quả
    print("\n" + "=" * 60)
    print("KẾT QUẢ ĐÁNH GIÁ")
    print("=" * 60)
    print(f"{'Accuracy (Độ chính xác):':<35} {do_chinh_xac:.4f} ({do_chinh_xac*100:.2f}%)")
    print(f"{'Precision (Độ chính xác dương):':<35} {do_chinh_xac_duong:.4f} ({do_chinh_xac_duong*100:.2f}%)")
    print(f"{'Recall (Độ nhạy):':<35} {do_nhay:.4f} ({do_nhay*100:.2f}%)")
    print(f"{'F1-Score:':<35} {f1:.4f} ({f1*100:.2f}%)")

    print(f"\nConfusion Matrix (Ma trận nhầm lẫn):")
    print(f"  Nhãn: 0 = Chó, 1 = Mèo")
    print(f"  {ma_tran_nham_lan}")

    print(f"\nBáo cáo chi tiết:")
    print(classification_report(thuc_te, du_doan, target_names=["Chó", "Mèo"]))

    # 6. Lưu kết quả ra JSON
    ket_qua = {
        "accuracy": float(do_chinh_xac),
        "precision": float(do_chinh_xac_duong),
        "recall": float(do_nhay),
        "f1_score": float(f1),
        "confusion_matrix": ma_tran_nham_lan.tolist(),
        "so_luong_anh_test": int(du_lieu_kiem_tra.samples),
        "nhan_lop": {"cho": 0, "meo": 1},
    }

    os.makedirs(os.path.dirname(DUONG_DAN_KET_QUA), exist_ok=True)
    with open(DUONG_DAN_KET_QUA, "w", encoding="utf-8") as f:
        json.dump(ket_qua, f, indent=2, ensure_ascii=False)
    print(f"\nĐã lưu kết quả tại: {DUONG_DAN_KET_QUA}")


if __name__ == "__main__":
    danh_gia()
