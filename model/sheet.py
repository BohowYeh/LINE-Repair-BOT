# 類別功能：
# 指定工作表名稱和標題
# 新增工作表內容

import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac


class GoogleSheet():
    '''
    建構式參數：
    wks_name：試算表名稱
    ws_title：工作表名稱，預設None。
    oauth_file：憑證檔名
    '''

    def __init__(self, wks_name, wks_title=None, oauth='oauth.json'):  # 請自行修改檔名
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        try:  # 嘗試讀取憑證檔
            JSON_PATH = os.path.join(os.getcwd(), 'model', oauth)
            cr = sac.from_json_keyfile_name(JSON_PATH, scope)
        except Exception as e:
            print('無法開啟憑證檔', e)
            sys.exit(1)  # 關閉程式

        try:  # 嘗試開啟Google試算表
            gc = gspread.authorize(cr)
            sh = gc.open(wks_name)
        except Exception as e:
            print('無法開啟Google試算表', e)
            sys.exit(1)

        if wks_title is None:
            # 開啟「工作表1」
            self._wks = sh.sheet1
        else:
            try:  # 嘗試開啟指定工作表
                self._wks = sh.worksheet(wks_title)
            except Exception as e:
                print('無法開啟工作表', e)
                sys.exit(1)

        # 讀取標題列
        # self.headers = self._wks.row_values(1)

    def append_row(self, data):
        self._wks.append_row(data)  # 插入新列

    def resize(self, n=1):
        self._wks.resize(n)

    def update_header(self, data, delete=True):
        if delete:
            self._wks.delete_row(1)

        self._wks.insert_row(data, 1)

    @property
    def headers(self):
        return self._wks.row_values(1)
