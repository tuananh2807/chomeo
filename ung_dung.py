from __future__ import annotations

import os
import uuid
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from cau_hinh import DINH_DANG_ANH_HOP_LE, KHOA_BI_MAT, THU_MUC_TAP_TIN_TAI_LEN
from co_so_du_lieu import (
    cap_nhat_thong_tin,
    doi_mat_khau,
    khoi_tao_co_so_du_lieu,
    lay_lich_su_ca_nhan,
    lay_lich_su_theo_id,
    luu_lich_su,
    tim_nguoi_dung_theo_id,
    tim_nguoi_dung_theo_ten_dang_nhap,
    tao_nguoi_dung,
    xoa_lich_su,
    lay_tat_ca_nguoi_dung,
    lay_tat_ca_lich_su,
    cap_nhat_trang_thai_nguoi_dung,
    xoa_lich_su_he_thong,
)
from mo_hinh_cnn import MoHinhNhanDienChoMeo
from phan_quyen import kiem_tra_quyen

ung_dung = Flask(
    __name__,
    template_folder="mau_giao_dien",
    static_folder="tai_nguyen_tinh",
)
ung_dung.secret_key = KHOA_BI_MAT
bo_nhan_dien = MoHinhNhanDienChoMeo()


os.makedirs(THU_MUC_TAP_TIN_TAI_LEN, exist_ok=True)


def lay_vai_tro_hien_tai() -> str:
    return session.get("vai_tro", "khach")


def da_dang_nhap() -> bool:
    return "nguoi_dung_id" in session


def ten_tap_tin_hop_le(ten_tap_tin: str) -> bool:
    if "." not in ten_tap_tin:
        return False
    duoi = ten_tap_tin.rsplit(".", 1)[1].lower()
    return duoi in DINH_DANG_ANH_HOP_LE


def yeu_cau_quyen(chuc_nang: str):
    def bo_boc(ham):
        @wraps(ham)
        def ham_trang_tri(*args, **kwargs):
            vai_tro = lay_vai_tro_hien_tai()
            if not kiem_tra_quyen(vai_tro, chuc_nang):
                flash("Bạn không có quyền truy cập chức năng này.", "loi")
                return redirect(url_for("trang_chu"))
            return ham(*args, **kwargs)

        return ham_trang_tri

    return bo_boc


@ung_dung.context_processor
def chen_thong_tin_nguoi_dung():
    return {
        "vai_tro_hien_tai": lay_vai_tro_hien_tai(),
        "ten_dang_nhap_hien_tai": session.get("ten_dang_nhap"),
    }


@ung_dung.route("/")
@yeu_cau_quyen("xem_trang_web")
def trang_chu():
    return render_template("trang_chu.html")


@ung_dung.route("/gioi-thieu")
@yeu_cau_quyen("xem_gioi_thieu")
def gioi_thieu():
    return render_template("gioi_thieu.html")


@ung_dung.route("/dang-ky", methods=["GET", "POST"])
@yeu_cau_quyen("dang_ky")
def dang_ky():
    if request.method == "POST":
        ten_dang_nhap = request.form.get("ten_dang_nhap", "").strip()
        mat_khau = request.form.get("mat_khau", "").strip()
        ho_ten = request.form.get("ho_ten", "").strip()
        email = request.form.get("email", "").strip()

        if not ten_dang_nhap or not mat_khau:
            flash("Tên đăng nhập và mật khẩu là bắt buộc.", "loi")
            return render_template("dang_ky.html")

        if tim_nguoi_dung_theo_ten_dang_nhap(ten_dang_nhap) is not None:
            flash("Tên đăng nhập đã tồn tại.", "loi")
            return render_template("dang_ky.html")

        tao_nguoi_dung(
            ten_dang_nhap=ten_dang_nhap,
            mat_khau_goc=mat_khau,
            vai_tro="nguoi_dung",
            ho_ten=ho_ten,
            email=email,
        )
        flash("Đăng ký thành công. Bạn có thể đăng nhập ngay.", "thanh_cong")
        return redirect(url_for("dang_nhap"))

    return render_template("dang_ky.html")


@ung_dung.route("/dang-nhap", methods=["GET", "POST"])
@yeu_cau_quyen("dang_nhap")
def dang_nhap():
    if request.method == "POST":
        ten_dang_nhap = request.form.get("ten_dang_nhap", "").strip()
        mat_khau = request.form.get("mat_khau", "").strip()

        nguoi_dung = tim_nguoi_dung_theo_ten_dang_nhap(ten_dang_nhap)
        if nguoi_dung is None:
            flash("Sai tên đăng nhập hoặc mật khẩu.", "loi")
            return render_template("dang_nhap.html")

        if not check_password_hash(nguoi_dung["mat_khau_hash"], mat_khau):
            flash("Sai tên đăng nhập hoặc mật khẩu.", "loi")
            return render_template("dang_nhap.html")

        trang_thai = nguoi_dung.get("trang_thai", "hoat_dong")
        if trang_thai == "cho_duyet":
            flash("Tài khoản của bạn đang chờ Admin duyệt.", "loi")
            return render_template("dang_nhap.html")
        elif trang_thai == "bi_khoa":
            flash("Tài khoản của bạn đã bị khóa.", "loi")
            return render_template("dang_nhap.html")

        session["nguoi_dung_id"] = int(nguoi_dung["id"])
        session["ten_dang_nhap"] = nguoi_dung["ten_dang_nhap"]
        session["vai_tro"] = nguoi_dung["vai_tro"]
        flash("Đăng nhập thành công.", "thanh_cong")
        return redirect(url_for("trang_chu"))

    return render_template("dang_nhap.html")


@ung_dung.route("/dang-xuat")
@yeu_cau_quyen("dang_xuat")
def dang_xuat():
    session.clear()
    flash("Bạn đã đăng xuất.", "thanh_cong")
    return redirect(url_for("trang_chu"))


@ung_dung.route("/quan-tri")
@yeu_cau_quyen("xem_quan_tri")
def trang_quan_tri():
    ds_nguoi_dung = lay_tat_ca_nguoi_dung()
    ds_lich_su = lay_tat_ca_lich_su()
    return render_template(
        "quan_tri.html",
        ds_nguoi_dung=ds_nguoi_dung,
        ds_lich_su=ds_lich_su,
        tong_nguoi_dung=len(ds_nguoi_dung),
        tong_lich_su=len(ds_lich_su),
    )


@ung_dung.route("/quan-tri/duyet/<int:id>", methods=["POST"])
@yeu_cau_quyen("duyet_tai_khoan")
def duyet_tai_khoan_route(id: int):
    cap_nhat_trang_thai_nguoi_dung(id, "hoat_dong")
    flash("Đã duyệt tài khoản.", "thanh_cong")
    return redirect(url_for("trang_quan_tri"))


@ung_dung.route("/quan-tri/khoa-mo/<int:id>/<string:hanh_dong>", methods=["POST"])
@yeu_cau_quyen("khoa_tai_khoan")
def khoa_mo_tai_khoan(id: int, hanh_dong: str):
    trang_thai_moi = "bi_khoa" if hanh_dong == "khoa" else "hoat_dong"
    cap_nhat_trang_thai_nguoi_dung(id, trang_thai_moi)
    flash(f"Đã {'khóa' if hanh_dong == 'khoa' else 'mở khóa'} tài khoản.", "thanh_cong")
    return redirect(url_for("trang_quan_tri"))


@ung_dung.route("/quan-tri/xoa-lich-su/<int:ma_lich_su>", methods=["POST"])
@yeu_cau_quyen("xoa_lich_su_he_thong")
def xoa_lich_su_he_thong_route(ma_lich_su: int):
    xoa_lich_su_he_thong(ma_lich_su)
    flash("Đã xóa bản ghi lịch sử khỏi hệ thống.", "thanh_cong")
    return redirect(url_for("trang_quan_tri"))


@ung_dung.route("/xem-anh/<ten_tap_tin>")
def xem_anh_tai_len(ten_tap_tin: str):
    """Phục vụ ảnh đã upload để hiển thị trên trang kết quả."""
    duong_dan = os.path.join(THU_MUC_TAP_TIN_TAI_LEN, ten_tap_tin)
    if not os.path.exists(duong_dan):
        return "Ảnh không tồn tại", 404
    return send_file(duong_dan)


@ung_dung.route("/nhan-dien", methods=["POST"])
@yeu_cau_quyen("upload_anh_nhan_dien")
def nhan_dien_anh():
    tep_anh = request.files.get("tep_anh")

    if tep_anh is None or tep_anh.filename == "":
        flash("Bạn chưa chọn ảnh.", "loi")
        return redirect(url_for("trang_chu"))

    if not ten_tap_tin_hop_le(tep_anh.filename):
        flash("Định dạng ảnh không hợp lệ.", "loi")
        return redirect(url_for("trang_chu"))

    ten_an_toan = secure_filename(tep_anh.filename)
    ten_ngau_nhien = f"{uuid.uuid4().hex}_{ten_an_toan}"
    duong_dan_luu = os.path.join(THU_MUC_TAP_TIN_TAI_LEN, ten_ngau_nhien)
    tep_anh.save(duong_dan_luu)

    try:
        ket_qua, do_tin_cay = bo_nhan_dien.du_doan(duong_dan_luu)
    except FileNotFoundError as loi_mo_hinh:
        flash(str(loi_mo_hinh), "loi")
        return redirect(url_for("trang_chu"))

    session["ket_qua_tam"] = {
        "ten_tap_tin": ten_an_toan,
        "ten_tap_tin_luu": ten_ngau_nhien,
        "duong_dan_tap_tin": duong_dan_luu,
        "ket_qua": ket_qua,
        "do_tin_cay": do_tin_cay,
    }

    return render_template(
        "ket_qua.html",
        ten_tap_tin=ten_an_toan,
        ten_tap_tin_luu=ten_ngau_nhien,
        ket_qua=ket_qua,
        do_tin_cay=do_tin_cay,
        la_nguoi_dung=lay_vai_tro_hien_tai() == "nguoi_dung",
    )


@ung_dung.route("/luu-ket-qua", methods=["POST"])
@yeu_cau_quyen("luu_ket_qua_nhan_dien")
def luu_ket_qua_nhan_dien():
    thong_tin = session.get("ket_qua_tam")
    nguoi_dung_id = session.get("nguoi_dung_id")

    if thong_tin is None or nguoi_dung_id is None:
        flash("Không có kết quả tạm để lưu.", "loi")
        return redirect(url_for("trang_chu"))

    luu_lich_su(
        nguoi_dung_id=int(nguoi_dung_id),
        ten_tap_tin=thong_tin["ten_tap_tin"],
        duong_dan_tap_tin=thong_tin["duong_dan_tap_tin"],
        ket_qua=thong_tin["ket_qua"],
        do_tin_cay=float(thong_tin["do_tin_cay"]),
    )
    flash("Đã lưu kết quả nhận diện.", "thanh_cong")
    return redirect(url_for("xem_lich_su_ca_nhan"))


@ung_dung.route("/lich-su")
@yeu_cau_quyen("xem_lich_su_ca_nhan")
def xem_lich_su_ca_nhan():
    nguoi_dung_id = int(session["nguoi_dung_id"])
    lich_su = lay_lich_su_ca_nhan(nguoi_dung_id)
    return render_template("lich_su.html", lich_su=lich_su)


@ung_dung.route("/tai-xuong/<int:ma_lich_su>")
@yeu_cau_quyen("tai_anh_xuong")
def tai_anh_xuong(ma_lich_su: int):
    nguoi_dung_id = int(session["nguoi_dung_id"])
    ban_ghi = lay_lich_su_theo_id(ma_lich_su)

    if ban_ghi is None or int(ban_ghi["nguoi_dung_id"]) != nguoi_dung_id:
        flash("Không tìm thấy ảnh hoặc bạn không có quyền tải.", "loi")
        return redirect(url_for("xem_lich_su_ca_nhan"))

    duong_dan = ban_ghi["duong_dan_tap_tin"]
    if not os.path.exists(duong_dan):
        flash("Ảnh không còn tồn tại trên máy chủ.", "loi")
        return redirect(url_for("xem_lich_su_ca_nhan"))

    return send_file(duong_dan, as_attachment=True, download_name=ban_ghi["ten_tap_tin"])


@ung_dung.route("/xoa-lich-su/<int:ma_lich_su>", methods=["POST"])
@yeu_cau_quyen("xoa_lich_su_ca_nhan")
def xoa_lich_su_ca_nhan(ma_lich_su: int):
    nguoi_dung_id = int(session["nguoi_dung_id"])
    xoa_lich_su(ma_lich_su, nguoi_dung_id)
    flash("Đã xóa bản ghi lịch sử.", "thanh_cong")
    return redirect(url_for("xem_lich_su_ca_nhan"))


@ung_dung.route("/cap-nhat-thong-tin", methods=["GET", "POST"])
@yeu_cau_quyen("cap_nhat_thong_tin_ca_nhan")
def cap_nhat_thong_tin_ca_nhan():
    nguoi_dung_id = int(session["nguoi_dung_id"])

    if request.method == "POST":
        ho_ten = request.form.get("ho_ten", "").strip()
        email = request.form.get("email", "").strip()
        cap_nhat_thong_tin(nguoi_dung_id, ho_ten, email)
        flash("Cập nhật thông tin thành công.", "thanh_cong")
        return redirect(url_for("cap_nhat_thong_tin_ca_nhan"))

    thong_tin = tim_nguoi_dung_theo_id(nguoi_dung_id)
    return render_template("cap_nhat_thong_tin.html", thong_tin=thong_tin)


@ung_dung.route("/doi-mat-khau", methods=["GET", "POST"])
@yeu_cau_quyen("doi_mat_khau")
def doi_mat_khau_ca_nhan():
    nguoi_dung_id = int(session["nguoi_dung_id"])
    thong_tin = tim_nguoi_dung_theo_id(nguoi_dung_id)

    if request.method == "POST":
        mat_khau_hien_tai = request.form.get("mat_khau_hien_tai", "")
        mat_khau_moi = request.form.get("mat_khau_moi", "")
        xac_nhan = request.form.get("xac_nhan", "")

        if not check_password_hash(thong_tin["mat_khau_hash"], mat_khau_hien_tai):
            flash("Mật khẩu hiện tại không đúng.", "loi")
            return render_template("doi_mat_khau.html")

        if not mat_khau_moi or mat_khau_moi != xac_nhan:
            flash("Mật khẩu mới không hợp lệ hoặc không khớp.", "loi")
            return render_template("doi_mat_khau.html")

        doi_mat_khau(nguoi_dung_id, mat_khau_moi)
        flash("Đổi mật khẩu thành công.", "thanh_cong")
        return redirect(url_for("trang_chu"))

    return render_template("doi_mat_khau.html")


if __name__ == "__main__":
    khoi_tao_co_so_du_lieu()
    ung_dung.run(debug=True)
