from __future__ import annotations

import os

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

from cau_hinh import DUONG_DAN_MO_HINH, KICH_THUOC_ANH


class MoHinhNhanDienChoMeo:
    def __init__(self, duong_dan_mo_hinh: str = DUONG_DAN_MO_HINH):
        self.duong_dan_mo_hinh = duong_dan_mo_hinh
        self.mo_hinh = None

    def tai_mo_hinh(self) -> None:
        if self.mo_hinh is not None:
            return
        if not os.path.exists(self.duong_dan_mo_hinh):
            raise FileNotFoundError(
                "Chưa có mô hình. Hãy chạy huan_luyen_mo_hinh.py trước."
            )
        self.mo_hinh = load_model(self.duong_dan_mo_hinh)

    def du_doan(self, duong_dan_anh: str) -> tuple[str, float]:
        self.tai_mo_hinh()
        with Image.open(duong_dan_anh) as anh:
            anh = anh.convert("RGB")
            anh = anh.resize(KICH_THUOC_ANH)
            mang_anh = np.array(anh, dtype="float32") / 255.0

        mang_anh = np.expand_dims(mang_anh, axis=0)
        xac_suat_meo = float(self.mo_hinh.predict(mang_anh, verbose=0)[0][0])

        if xac_suat_meo >= 0.5:
            return "Mèo", xac_suat_meo
        return "Chó", 1.0 - xac_suat_meo
