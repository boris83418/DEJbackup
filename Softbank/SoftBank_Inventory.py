import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
from softbankapp import Ui_MainWindow  # 確保 `softbankapp` 是生成的 UI 模組
from SoftBank_SummaryTable_Export import export_summarytable_to_excel, connect_to_database

# 設定log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logfile.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)



class UpdateDatabaseThread(QThread):
    finished = pyqtSignal(bool, str)  # 信號：成功與否，訊息

    def run(self):
        """更新SoftBank資料庫"""
        # 更新腳本路徑
        SCRIPT_PATH = r"D:\Deltabox\OneDrive - Delta Electronics, Inc\deltaproject\DEJbackup\Softbank\SoftBank_ExceltoDB.py"
        try:
            logging.info("開始執行資料庫更新腳本...")
            result = subprocess.run(
                ["python", SCRIPT_PATH],
                # 讓外部腳本輸出訊息在終端機
                stdout=sys.stdout,
                # 讓外部腳本錯誤訊息在終端機
                stderr=sys.stderr,
                check=True
            )
            self.finished.emit(True, "寫入資料庫成功！")
        except subprocess.CalledProcessError as e:
            logging.error(f"寫入資料庫失敗: {e.stderr}")
            self.finished.emit(False, str(e.stderr))
        except Exception as e:
            logging.error(f"未知錯誤: {e}")
            self.finished.emit(False, str(e))


class ExportThread(QThread):
    finished = pyqtSignal(bool, str)  # 信號：成功與否，訊息

    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn

    def run(self):
        """執行匯出操作"""
        try:
            logging.info("開始匯出出貨清單...")
            output_excel_path = r"D:\\DeltaBox\\OneDrive - Delta Electronics, Inc\\deltaproject\\DEJbackup\\SoftbankExcel\\表單\\SoftBankSummaryTable.xlsx"
            table_name = "dbo.SoftBankSummaryView"
            export_summarytable_to_excel(self.conn, table_name, output_excel_path)  # 呼叫匯出函數
            self.finished.emit(True, "出貨清單匯出成功！")
        except Exception as e:
            logging.error(f"匯出失敗: {e}")
            self.finished.emit(False, str(e))


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind_events()
        self.update_database_thread = None
        self.export_thread = None
        # 設定背景圖片
        self.set_background_image()

    def set_background_image(self):
        """設定背景圖片"""
        pixmap = QPixmap("D:/DeltaBox/OneDrive - Delta Electronics, Inc/deltaproject/DEJbackup/Softbank/Pic/delta2.jpg")
        # 設定視窗背景
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), QBrush(pixmap))  # 直接使用圖片作為背景
        self.setPalette(p)

    def bind_events(self):
        """綁定按鈕事件"""
        self.pushButton.clicked.connect(self.start_database_update_thread)
        self.pushButton_2.clicked.connect(self.start_export_thread)

    def start_database_update_thread(self):
        """啟動資料庫更新執行緒"""
        logging.info("按下按鈕，開始資料庫更新過程...")
        self.pushButton.setEnabled(False)

        for button in self.findChildren(QPushButton):
            if button != self.pushButton:
                button.setEnabled(False)

        self.update_database_thread = UpdateDatabaseThread()
        self.update_database_thread.finished.connect(self.handle_database_update_result)
        self.update_database_thread.start()

    def handle_database_update_result(self, success, message):
        """處理資料庫更新執行緒的結果"""
        if success:
            logging.info("資料庫更新成功！")
            QMessageBox.information(self, "成功", message)
        else:
            logging.error("資料庫更新失敗！")
            QMessageBox.critical(self, "錯誤", message)

        self.pushButton.setEnabled(True)
        for button in self.findChildren(QPushButton):
            if button != self.pushButton:
                button.setEnabled(True)
        self.update_database_thread.deleteLater()  # 釋放資源
        self.update_database_thread = None

    def start_export_thread(self):
        """啟動匯出執行緒"""
        logging.info("按下按鈕，開始匯出出貨清單...")
        self.pushButton_2.setEnabled(False)

        try:
            conn = connect_to_database('jpdejitdev01', 'ITQAS2')
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"無法連接資料庫: {e}")
            self.pushButton_2.setEnabled(True)
            return
        
        self.export_thread = ExportThread(conn)
        self.export_thread.finished.connect(self.handle_export_result)
        self.export_thread.start()

    def handle_export_result(self, success, message):
        """處理匯出執行緒的結果"""
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.critical(self, "錯誤", message)

        self.pushButton_2.setEnabled(True)
        self.export_thread = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())