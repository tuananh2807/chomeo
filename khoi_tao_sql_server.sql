IF DB_ID(N'NhanDienChoMeo') IS NULL
BEGIN
    CREATE DATABASE NhanDienChoMeo;
END
GO

USE NhanDienChoMeo;
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[NguoiDung]') AND type in (N'U'))
BEGIN
    CREATE TABLE NguoiDung (
        id INT IDENTITY(1,1) PRIMARY KEY,
        ten_dang_nhap NVARCHAR(100) UNIQUE NOT NULL,
        mat_khau_hash NVARCHAR(255) NOT NULL,
        vai_tro NVARCHAR(30) NOT NULL,
        ho_ten NVARCHAR(120) NULL,
        email NVARCHAR(120) NULL,
        ngay_tao DATETIME2 NOT NULL DEFAULT GETDATE()
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LichSuNhanDien]') AND type in (N'U'))
BEGIN
    CREATE TABLE LichSuNhanDien (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nguoi_dung_id INT NOT NULL,
        ten_tap_tin NVARCHAR(255) NOT NULL,
        duong_dan_tap_tin NVARCHAR(500) NOT NULL,
        ket_qua NVARCHAR(20) NOT NULL,
        do_tin_cay FLOAT NOT NULL,
        thoi_gian DATETIME2 NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_LichSuNhanDien_NguoiDung FOREIGN KEY (nguoi_dung_id) REFERENCES NguoiDung(id)
    );
END
GO
