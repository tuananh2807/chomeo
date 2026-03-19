BAN_DO_QUYEN = {
    "khach": {
        "xem_trang_web",
        "xem_gioi_thieu",
        "upload_anh_nhan_dien",
        "xem_ket_qua_nhan_dien",
        "dang_ky",
        "dang_nhap",
    },
    "nguoi_dung": {
        "xem_trang_web",
        "xem_gioi_thieu",
        "upload_anh_nhan_dien",
        "xem_ket_qua_nhan_dien",
        "tai_anh_xuong",
        "luu_ket_qua_nhan_dien",
        "xem_lich_su_ca_nhan",
        "xoa_lich_su_ca_nhan",
        "dang_nhap",
        "dang_xuat",
        "cap_nhat_thong_tin_ca_nhan",
        "doi_mat_khau",
    },
    "admin": {
        "xem_trang_web",
        "xem_gioi_thieu",
        "xem_quan_tri",
        "dang_nhap",
        "dang_xuat",
        "cap_nhat_thong_tin_ca_nhan",
        "doi_mat_khau",
        "quan_ly_nguoi_dung",
        "xem_toan_bo_lich_su",
        "xoa_lich_su_he_thong",
        "duyet_tai_khoan",
        "khoa_tai_khoan",
    },
}


def kiem_tra_quyen(vai_tro: str, chuc_nang: str) -> bool:
    if vai_tro not in BAN_DO_QUYEN:
        return False
    return chuc_nang in BAN_DO_QUYEN[vai_tro]
