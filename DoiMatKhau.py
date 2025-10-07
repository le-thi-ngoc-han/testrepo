from PyQt6.QtWidgets import QWidget, QMessageBox

from Student_Management_App.classes.CLecturers import Lecturers


class DoiMatKhau(QWidget):
    def __init__(self):
        super().__init__()

    def lienketnutlenh(self):
        self.btnDoiMatKhau.clicked.connect(self.xuly_doimatkhau)

    def set_current_lecturer(self, lec):
        self.current_lecturer = lec  # Lưu giảng viên đang đăng nhập
        self.hienthi_thongtin(lec)  # Hiển thị thông tin

    def hienthi_thongtin(self, lec):
        self.txtMaGiangVien.setText(f"{lec.id}")
        self.txtTenGiangVien.setText(lec.name)

    def xuly_doimatkhau(self):
        try:
            # Bước 1: Phải đăng nhập trước, nếu thành công thì mới cho đổi mật khẩu
            username = self.txtUsername.text()
            password = self.txtMatKhauCu.text()
            lecturer_list = Lecturers()
            lec = lecturer_list.login(username, password)
            if lec == None:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Lỗi đổi mật khẩu")
                msgBox.setText("Username hoặc mật khẩu cũ bị sai, hãy kiểm tra lại.")
                msgBox.setIcon(QMessageBox.Icon.Critical)
                msgBox.exec()
            else:
                # Bước 2: Kiểm tra phía User mật khẩu mới và xác nhận lại mk mới có khớp không:
                newpassword = self.txtMatKhauMoi.text()
                confirm_newpassword = self.txtXacNhanLaiMatKhauMoi.text()
                if newpassword != confirm_newpassword:
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("Lỗi đổi mật khẩu")
                    msgBox.setText("Mật khẩu mới chưa trùng khớp, vui lòng nhập lại.")
                    msgBox.setIcon(QMessageBox.Icon.Critical)
                    msgBox.exec()
                else:
                    # bước 3: Đổi mật khẩu trong file JSON:
                    id = int(self.txtMaGiangVien.text())
                    result = lecturer_list.doimatkhau(id, newpassword)
                    if result > 0:
                        msg = "Đổi mật khẩu thành công."
                    else:
                        msg = "Đổi mật khẩu thất bại."
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("Thông báo")
                    msgBox.setText(msg)
                    msgBox.setIcon(QMessageBox.Icon.Information)
                    msgBox.exec()
        except Exception as e:
            print(f"Đã xảy ra lỗi khi đổi mật khẩu: {e}")
