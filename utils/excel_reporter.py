import openpyxl
import os
from datetime import datetime


class ExcelReporter:
    def __init__(self, filename="QA_Test_Report.xlsx"):
        self.report_dir = "reports"
        self.filename = filename
        self.filepath = os.path.join(self.report_dir, self.filename)

        # reports 폴더 없으면 생성
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
        # file 없으면 생성
        if not os.path.exists(self.filepath):
            self._create_new_report()

    def _create_new_report(self):
        """새로운 보고서 파일 생성 및 헤더 작성"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test Report"
        headers = [

        ]

        headers = [
            "TC ID",
            "Module",
            "Scenario",
            "Test Data",
            "Expected",
            "Actual",
            "Status",
            "Time"
        ]
        ws.append(headers)
        wb.save(self.filepath)

    def log_result(self, tc_id, module, scenario, test_data, expected, actual, status):
        """테스트 결과를 엑셀에 추가"""
        try:
            wb = openpyxl.load_workbook(self.filepath)
            ws = wb.active

            timestamp = datetime.now().strftime('%H:%M:%S')
            row = [tc_id,
                   module,
                   scenario,
                   test_data,
                   expected,
                   actual,
                   status,
                   timestamp]
            ws.append(row)
            wb.save(self.filepath)
            print(f"    [Report] Saved: {tc_id} - {status}")

        except Exception as e:
            print(f"    [Error] 리포트 저장 실패: {e}")



