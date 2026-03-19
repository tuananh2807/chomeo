from __future__ import annotations

import json
import os

import tensorflow as tf
from tensorflow.keras import layers, models

from cau_hinh import DUONG_DAN_MO_HINH, KICH_THUOC_ANH, THU_MUC_GOC

THU_MUC_DU_LIEU = os.path.join(THU_MUC_GOC, "du_lieu_huan_luyen")
THU_MUC_HUAN_LUYEN = os.path.join(THU_MUC_DU_LIEU, "train")
THU_MUC_KIEM_TRA = os.path.join(THU_MUC_DU_LIEU, "val")
DUONG_DAN_LICH_SU = os.path.join(THU_MUC_GOC, "mo_hinh", "lich_su_huan_luyen.json")


def tao_mo_hinh() -> tf.keras.Model:
    """Tạo mô hình CNN dựa trên thuật toán Transfer Learning (MobileNetV2) cho phân loại chó mèo."""
    mo_hinh_co_so = tf.keras.applications.MobileNetV2(
        input_shape=(KICH_THUOC_ANH[0], KICH_THUOC_ANH[1], 3),
        include_top=False,
        weights="imagenet"
    )
    # Đóng băng các lớp của mô hình cơ sở để giữ kiến thức đã học từ hàng triệu ảnh
    mo_hinh_co_so.trainable = False

    mo_hinh = models.Sequential([
        # Đầu vào
        layers.Input(shape=(KICH_THUOC_ANH[0], KICH_THUOC_ANH[1], 3)),
        mo_hinh_co_so,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        # Đầu ra sigmoid cho phân loại nhị phân
        layers.Dense(1, activation="sigmoid"),
    ])
    mo_hinh.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return mo_hinh


def huan_luyen() -> None:
    """Huấn luyện mô hình CNN và lưu lịch sử huấn luyện."""

    # --- Data Augmentation cho tập huấn luyện ---
    bo_tao_huan_luyen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
    )
    # Tập validation chỉ rescale, không augmentation
    bo_tao_kiem_tra = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

    du_lieu_huan_luyen = bo_tao_huan_luyen.flow_from_directory(
        THU_MUC_HUAN_LUYEN,
        target_size=KICH_THUOC_ANH,
        batch_size=32,
        class_mode="binary",
        classes=["cho", "meo"],
    )
    du_lieu_kiem_tra = bo_tao_kiem_tra.flow_from_directory(
        THU_MUC_KIEM_TRA,
        target_size=KICH_THUOC_ANH,
        batch_size=32,
        class_mode="binary",
        classes=["cho", "meo"],
    )

    mo_hinh = tao_mo_hinh()

    # In tóm tắt mô hình (cho Chương 3)
    print("=" * 60)
    print("TÓM TẮT MÔ HÌNH CNN")
    print("=" * 60)
    mo_hinh.summary()
    print("=" * 60)

    # Huấn luyện
    lich_su = mo_hinh.fit(
        du_lieu_huan_luyen,
        validation_data=du_lieu_kiem_tra,
        epochs=10,
    )

    # Lưu mô hình
    os.makedirs(os.path.dirname(DUONG_DAN_MO_HINH), exist_ok=True)
    mo_hinh.save(DUONG_DAN_MO_HINH)
    print(f"\nĐã lưu mô hình tại: {DUONG_DAN_MO_HINH}")

    # --- Lưu lịch sử huấn luyện ra file JSON (cho Chương 3 & 4) ---
    du_lieu_lich_su = {}
    for khoa, gia_tri in lich_su.history.items():
        du_lieu_lich_su[khoa] = [float(v) for v in gia_tri]

    # Thêm thông tin siêu tham số
    du_lieu_lich_su["sieu_tham_so"] = {
        "kich_thuoc_anh": list(KICH_THUOC_ANH),
        "batch_size": 32,
        "epochs": 10,
        "optimizer": "Adam",
        "loss_function": "binary_crossentropy",
        "dropout_rate": 0.3,
        "thuat_toan": "Transfer Learning (MobileNetV2 từ ImageNet)",
        "data_augmentation": {
            "rotation_range": 20,
            "zoom_range": 0.2,
            "horizontal_flip": True,
            "width_shift_range": 0.1,
            "height_shift_range": 0.1,
            "shear_range": 0.1,
        },
    }

    with open(DUONG_DAN_LICH_SU, "w", encoding="utf-8") as f:
        json.dump(du_lieu_lich_su, f, indent=2, ensure_ascii=False)
    print(f"Đã lưu lịch sử huấn luyện tại: {DUONG_DAN_LICH_SU}")


if __name__ == "__main__":
    huan_luyen()
