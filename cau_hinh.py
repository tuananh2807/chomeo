import os

THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
THU_MUC_TAP_TIN_TAI_LEN = os.path.join(THU_MUC_GOC, "tap_tin_tai_len")
THU_MUC_MO_HINH = os.path.join(THU_MUC_GOC, "mo_hinh")
DUONG_DAN_MO_HINH = os.path.join(THU_MUC_MO_HINH, "phan_loai_cho_meo.keras")

KHOA_BI_MAT = "khoa_bi_mat_demo_cnn_cho_meo_2026"
KICH_THUOC_ANH = (160, 160)
DINH_DANG_ANH_HOP_LE = {"png", "jpg", "jpeg", "bmp", "webp"}

DUONG_DAN_CO_SO_DU_LIEU = os.path.join(THU_MUC_GOC, "co_so_du_lieu.sqlite")
