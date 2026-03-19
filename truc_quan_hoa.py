"""
Trực quan hóa kết quả huấn luyện và đánh giá mô hình CNN.
Tạo biểu đồ cho Chương 3 (Methodology) và Chương 4 (Results).

Cách chạy:
    python truc_quan_hoa.py

Biểu đồ được lưu vào thư mục: mo_hinh/bieu_do/
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")  # Không cần GUI
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from cau_hinh import THU_MUC_GOC

THU_MUC_BIEU_DO = os.path.join(THU_MUC_GOC, "mo_hinh", "bieu_do")
DUONG_DAN_LICH_SU = os.path.join(THU_MUC_GOC, "mo_hinh", "lich_su_huan_luyen.json")
DUONG_DAN_KET_QUA = os.path.join(THU_MUC_GOC, "mo_hinh", "ket_qua_danh_gia.json")


def doc_lich_su() -> dict | None:
    if not os.path.exists(DUONG_DAN_LICH_SU):
        print(f"Không tìm thấy: {DUONG_DAN_LICH_SU}")
        print("Hãy chạy: python huan_luyen_mo_hinh.py trước.")
        return None
    with open(DUONG_DAN_LICH_SU, "r", encoding="utf-8") as f:
        return json.load(f)


def doc_ket_qua() -> dict | None:
    if not os.path.exists(DUONG_DAN_KET_QUA):
        print(f"Không tìm thấy: {DUONG_DAN_KET_QUA}")
        print("Hãy chạy: python danh_gia_mo_hinh.py trước.")
        return None
    with open(DUONG_DAN_KET_QUA, "r", encoding="utf-8") as f:
        return json.load(f)


def ve_learning_curves(lich_su: dict) -> None:
    """Vẽ biểu đồ Loss và Accuracy theo epoch (Chương 4 - Learning Curves)."""
    epochs = range(1, len(lich_su["loss"]) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Learning Curves - Mô hình CNN phân loại Chó Mèo", fontsize=14, fontweight="bold")

    # --- Loss ---
    ax1.plot(epochs, lich_su["loss"], "o-", color="#6366f1", label="Training Loss", linewidth=2, markersize=6)
    if "val_loss" in lich_su:
        ax1.plot(epochs, lich_su["val_loss"], "s--", color="#ef4444", label="Validation Loss", linewidth=2, markersize=6)
    ax1.set_title("Hàm mất mát (Loss) theo Epoch", fontsize=12)
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss (Binary Crossentropy)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(list(epochs))

    # --- Accuracy ---
    ax2.plot(epochs, lich_su["accuracy"], "o-", color="#10b981", label="Training Accuracy", linewidth=2, markersize=6)
    if "val_accuracy" in lich_su:
        ax2.plot(epochs, lich_su["val_accuracy"], "s--", color="#f59e0b", label="Validation Accuracy", linewidth=2, markersize=6)
    ax2.set_title("Độ chính xác (Accuracy) theo Epoch", fontsize=12)
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(list(epochs))
    ax2.set_ylim(0, 1.05)

    plt.tight_layout()
    duong_dan = os.path.join(THU_MUC_BIEU_DO, "learning_curves.png")
    plt.savefig(duong_dan, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Đã lưu: {duong_dan}")


def ve_loss_rieng(lich_su: dict) -> None:
    """Vẽ biểu đồ Loss riêng."""
    epochs = range(1, len(lich_su["loss"]) + 1)
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, lich_su["loss"], "o-", color="#6366f1", label="Training Loss", linewidth=2)
    if "val_loss" in lich_su:
        plt.plot(epochs, lich_su["val_loss"], "s--", color="#ef4444", label="Validation Loss", linewidth=2)
    plt.title("Hàm mất mát (Loss) theo Epoch", fontsize=13, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Binary Crossentropy Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(list(epochs))
    plt.tight_layout()
    duong_dan = os.path.join(THU_MUC_BIEU_DO, "loss_chart.png")
    plt.savefig(duong_dan, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Đã lưu: {duong_dan}")


def ve_accuracy_rieng(lich_su: dict) -> None:
    """Vẽ biểu đồ Accuracy riêng."""
    epochs = range(1, len(lich_su["accuracy"]) + 1)
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, lich_su["accuracy"], "o-", color="#10b981", label="Training Accuracy", linewidth=2)
    if "val_accuracy" in lich_su:
        plt.plot(epochs, lich_su["val_accuracy"], "s--", color="#f59e0b", label="Validation Accuracy", linewidth=2)
    plt.title("Độ chính xác (Accuracy) theo Epoch", fontsize=13, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(list(epochs))
    plt.ylim(0, 1.05)
    plt.tight_layout()
    duong_dan = os.path.join(THU_MUC_BIEU_DO, "accuracy_chart.png")
    plt.savefig(duong_dan, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Đã lưu: {duong_dan}")


def ve_confusion_matrix(ket_qua: dict) -> None:
    """Vẽ Confusion Matrix heatmap (Chương 4)."""
    cm = np.array(ket_qua["confusion_matrix"])
    plt.figure(figsize=(7, 6))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Chó", "Mèo"],
        yticklabels=["Chó", "Mèo"],
        annot_kws={"size": 18, "fontweight": "bold"},
        linewidths=1,
        linecolor="white",
    )
    plt.title("Confusion Matrix (Ma trận nhầm lẫn)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Dự đoán (Predicted)", fontsize=12)
    plt.ylabel("Thực tế (Actual)", fontsize=12)

    plt.tight_layout()
    duong_dan = os.path.join(THU_MUC_BIEU_DO, "confusion_matrix.png")
    plt.savefig(duong_dan, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Đã lưu: {duong_dan}")


def ve_bang_so_lieu(ket_qua: dict) -> None:
    """Tạo bảng so sánh kết quả (cho báo cáo)."""
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis("off")

    du_lieu = [
        ["Accuracy (Độ chính xác)", f"{ket_qua['accuracy']*100:.2f}%"],
        ["Precision (Độ chính xác dương)", f"{ket_qua['precision']*100:.2f}%"],
        ["Recall (Độ nhạy)", f"{ket_qua['recall']*100:.2f}%"],
        ["F1-Score", f"{ket_qua['f1_score']*100:.2f}%"],
    ]

    bang = ax.table(
        cellText=du_lieu,
        colLabels=["Tiêu chí đánh giá", "Kết quả"],
        loc="center",
        cellLoc="center",
    )
    bang.auto_set_font_size(False)
    bang.set_fontsize(12)
    bang.scale(1, 1.8)

    # Style header
    for j in range(2):
        bang[0, j].set_facecolor("#6366f1")
        bang[0, j].set_text_props(color="white", fontweight="bold")

    # Style cells
    for i in range(1, 5):
        for j in range(2):
            bang[i, j].set_facecolor("#f0f0ff" if i % 2 == 0 else "white")

    plt.title("Bảng kết quả đánh giá mô hình CNN", fontsize=13, fontweight="bold", pad=20)
    plt.tight_layout()
    duong_dan = os.path.join(THU_MUC_BIEU_DO, "bang_ket_qua.png")
    plt.savefig(duong_dan, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Đã lưu: {duong_dan}")


def main() -> None:
    os.makedirs(THU_MUC_BIEU_DO, exist_ok=True)

    print("=" * 60)
    print("TRỰC QUAN HÓA KẾT QUẢ MÔ HÌNH CNN")
    print("=" * 60)

    # 1. Learning curves (cần file lịch sử huấn luyện)
    lich_su = doc_lich_su()
    if lich_su is not None:
        ve_learning_curves(lich_su)
        ve_loss_rieng(lich_su)
        ve_accuracy_rieng(lich_su)

    # 2. Confusion matrix & bảng kết quả (cần file đánh giá)
    ket_qua = doc_ket_qua()
    if ket_qua is not None:
        ve_confusion_matrix(ket_qua)
        ve_bang_so_lieu(ket_qua)

    print("\n" + "=" * 60)
    print(f"Tất cả biểu đồ đã lưu tại: {THU_MUC_BIEU_DO}")
    print("Bạn có thể chèn các ảnh này vào Chương 3 & 4 của báo cáo.")
    print("=" * 60)


if __name__ == "__main__":
    main()
