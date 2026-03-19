from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from werkzeug.security import generate_password_hash

from cau_hinh import DUONG_DAN_CO_SO_DU_LIEU


def ket_noi() -> sqlite3.Connection:
    conn = sqlite3.connect(DUONG_DAN_CO_SO_DU_LIEU)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def _dong_sang_dict(cursor: sqlite3.Cursor) -> list[dict[str, Any]]:
    if not cursor.description:
        return []
    cot = [cot[0] for cot in cursor.description]
    du_lieu = []
    for dong in cursor.fetchall():
        ban_ghi = {}
        for i, ten_cot in enumerate(cot):
            gia_tri = dong[i]
            if ten_cot in ('thoi_gian', 'ngay_tao') and isinstance(gia_tri, str):
                try:
                    gia_tri = datetime.strptime(gia_tri, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            ban_ghi[ten_cot] = gia_tri
        du_lieu.append(ban_ghi)
    return du_lieu


def khoi_tao_co_so_du_lieu() -> None:
    truy_van_tao_bang_nguoi_dung = """
    CREATE TABLE IF NOT EXISTS NguoiDung (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten_dang_nhap TEXT UNIQUE NOT NULL,
        mat_khau_hash TEXT NOT NULL,
        vai_tro TEXT NOT NULL,
        ho_ten TEXT NULL,
        email TEXT NULL,
        ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        trang_thai TEXT NOT NULL DEFAULT 'cho_duyet'
    );
    """

    truy_van_tao_bang_lich_su = """
    CREATE TABLE IF NOT EXISTS LichSuNhanDien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nguoi_dung_id INTEGER NOT NULL,
        ten_tap_tin TEXT NOT NULL,
        duong_dan_tap_tin TEXT NOT NULL,
        ket_qua TEXT NOT NULL,
        do_tin_cay REAL NOT NULL,
        thoi_gian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (nguoi_dung_id) REFERENCES NguoiDung(id)
    );
    """

    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(truy_van_tao_bang_nguoi_dung)
        cursor.execute(truy_van_tao_bang_lich_su)
        conn.commit()

    nguoi_dung_admin = tim_nguoi_dung_theo_ten_dang_nhap("admin")
    if nguoi_dung_admin is None:
        tao_nguoi_dung(
            ten_dang_nhap="admin",
            mat_khau_goc="admin123",
            vai_tro="admin",
            ho_ten="Quản trị hệ thống",
            email="admin@localhost",
        )


def tim_nguoi_dung_theo_ten_dang_nhap(ten_dang_nhap: str) -> dict[str, Any] | None:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM NguoiDung WHERE ten_dang_nhap = ? LIMIT 1",
            (ten_dang_nhap,),
        )
        ket_qua = _dong_sang_dict(cursor)
    return ket_qua[0] if ket_qua else None


def tim_nguoi_dung_theo_id(nguoi_dung_id: int) -> dict[str, Any] | None:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM NguoiDung WHERE id = ? LIMIT 1",
            (nguoi_dung_id,),
        )
        ket_qua = _dong_sang_dict(cursor)
    return ket_qua[0] if ket_qua else None


def tao_nguoi_dung(
    ten_dang_nhap: str,
    mat_khau_goc: str,
    vai_tro: str = "nguoi_dung",
    ho_ten: str | None = None,
    email: str | None = None,
) -> None:
    mat_khau_hash = generate_password_hash(mat_khau_goc)
    trang_thai = "hoat_dong" if vai_tro == "admin" else "cho_duyet"
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO NguoiDung (ten_dang_nhap, mat_khau_hash, vai_tro, ho_ten, email, trang_thai)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ten_dang_nhap, mat_khau_hash, vai_tro, ho_ten, email, trang_thai),
        )
        conn.commit()


def cap_nhat_thong_tin(nguoi_dung_id: int, ho_ten: str, email: str) -> None:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE NguoiDung SET ho_ten = ?, email = ? WHERE id = ?",
            (ho_ten, email, nguoi_dung_id),
        )
        conn.commit()


def doi_mat_khau(nguoi_dung_id: int, mat_khau_moi: str) -> None:
    mat_khau_hash = generate_password_hash(mat_khau_moi)
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE NguoiDung SET mat_khau_hash = ? WHERE id = ?",
            (mat_khau_hash, nguoi_dung_id),
        )
        conn.commit()


def luu_lich_su(
    nguoi_dung_id: int,
    ten_tap_tin: str,
    duong_dan_tap_tin: str,
    ket_qua: str,
    do_tin_cay: float,
) -> int:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO LichSuNhanDien (nguoi_dung_id, ten_tap_tin, duong_dan_tap_tin, ket_qua, do_tin_cay)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nguoi_dung_id, ten_tap_tin, duong_dan_tap_tin, ket_qua, do_tin_cay),
        )
        ma_moi = cursor.lastrowid
        conn.commit()
    return int(ma_moi) if ma_moi else 0


def lay_lich_su_ca_nhan(nguoi_dung_id: int) -> list[dict[str, Any]]:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nguoi_dung_id, ten_tap_tin, duong_dan_tap_tin, ket_qua, do_tin_cay, thoi_gian
            FROM LichSuNhanDien
            WHERE nguoi_dung_id = ?
            ORDER BY thoi_gian DESC
            """,
            (nguoi_dung_id,),
        )
        return _dong_sang_dict(cursor)


def lay_lich_su_theo_id(ma_lich_su: int) -> dict[str, Any] | None:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM LichSuNhanDien WHERE id = ? LIMIT 1",
            (ma_lich_su,),
        )
        du_lieu = _dong_sang_dict(cursor)
    return du_lieu[0] if du_lieu else None


def xoa_lich_su(ma_lich_su: int, nguoi_dung_id: int) -> None:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM LichSuNhanDien WHERE id = ? AND nguoi_dung_id = ?",
            (ma_lich_su, nguoi_dung_id),
        )
        conn.commit()


def lay_tat_ca_nguoi_dung() -> list[dict[str, Any]]:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NguoiDung ORDER BY ngay_tao DESC")
        return _dong_sang_dict(cursor)


def lay_tat_ca_lich_su() -> list[dict[str, Any]]:
    with ket_noi() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT L.*, N.ten_dang_nhap 
            FROM LichSuNhanDien L 
            JOIN NguoiDung N ON L.nguoi_dung_id = N.id 
            ORDER BY L.thoi_gian DESC LIMIT 100
            """
        )
        return _dong_sang_dict(cursor)


def cap_nhat_trang_thai_nguoi_dung(nguoi_dung_id: int, trang_thai_moi: str) -> None:
    with ket_noi() as conn:
        conn.execute("UPDATE NguoiDung SET trang_thai = ? WHERE id = ?", (trang_thai_moi, nguoi_dung_id))
        conn.commit()


def xoa_lich_su_he_thong(ma_lich_su: int) -> None:
    with ket_noi() as conn:
        conn.execute("DELETE FROM LichSuNhanDien WHERE id = ?", (ma_lich_su,))
        conn.commit()


