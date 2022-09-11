import pathlib
import os
import csv


HISTORY_COLUMN_ID = 'ID'
HISTORY_COLUMN_WAKEUP_TIME = 'WAKEUP_TIME'
HISTORY_COLUMN_START_ALARM_TIME = 'START_ALARM_TIME'
HISTORY_COLUMN_INTERVAL = 'INTERVAL'
HISTORY_COLUMN_RINGING_TIME = 'RINGING_TIME'
HISTORY_CSV_FILE_NAME = 'history.csv'


class CsvModel(object):
  """CSVファイルを扱うクラスの親クラス"""
  def __init__(self, csv_file):
    self.csv_file = csv_file
    if not os.path.exists(self.csv_file):
      pathlib.Path(self.csv_file).touch()


class HistoryModel(CsvModel):
  """アラームの履歴を読み書きするクラス"""
  def __init__(self, csv_file = None):
    if csv_file is None:
      csv_file = self.__get_csv_file_name()
    super().__init__(csv_file)
    self.__csv_file_column = [
      HISTORY_COLUMN_ID,
      HISTORY_COLUMN_WAKEUP_TIME,
      HISTORY_COLUMN_START_ALARM_TIME,
      HISTORY_COLUMN_INTERVAL,
      HISTORY_COLUMN_RINGING_TIME
    ]
    self.__id_counter = 0
    self.__history_data = []


  def load_history_exclude_header(self):
    """CSVファイルを読み込む（ヘッダーは読み込まない）。
       これから設定するアラームのIDを決めるため、
       これまでの最大のIDを取得しておく。

    Returns:
      self.history_data (list): CSVファイルの内容（ヘッダーは読み込まない）
    """
    with open(self.csv_file, 'r') as csv_file:
      reader = csv.DictReader(csv_file)

      for row in reader:
        history_data_elements = [
          row[HISTORY_COLUMN_ID], 
          row[HISTORY_COLUMN_WAKEUP_TIME], 
          row[HISTORY_COLUMN_START_ALARM_TIME], 
          row[HISTORY_COLUMN_INTERVAL], 
          row[HISTORY_COLUMN_RINGING_TIME]
        ]
        self.__history_data.append(history_data_elements)

        if self.__id_counter < int(row[HISTORY_COLUMN_ID]):
          self.__id_counter = int(row[HISTORY_COLUMN_ID])

    return self.__history_data


  def load_history_include_header(self):
    """CSVファイルを読み込む（ヘッダーも読み込む）

    Returns:
      rows (list): CSVファイルの内容（ヘッダーも読み込む）
    """
    with open(self.csv_file, 'r') as csv_file:
      reader = csv.reader(csv_file)
      rows = [row for row in reader]

    for row in rows[0]:
      print(row,end='　')
    print()
    for j in range(1, (int(rows[-1][0]) + 1)):
      print(rows[j][0], end = '')
      print('　　　　', rows[j][1], end = '')
      print('　　　　　　', rows[j][2], end = '')
      print('　　', rows[j][3], end = '')
      print('　　　　', rows[j][4])

    return rows

  
  def __get_csv_file_name(self):
    """CSVファイルの名前を設定する
        
    Returns:
      csv_file_name (str): CSVファイルの名前
    """
    csv_file_name = None

    try:
      import settings
      if settings.CSV_FILE_NAME:
        csv_file_name = settings.CSV_FILE_NAME
    except ImportError:
      pass

    if csv_file_name is None:
      csv_file_name = HISTORY_CSV_FILE_NAME

    return csv_file_name


  def save(self, history_data):
    """CSVファイルに書き込む

    Args:
      history_data (list): アラームの履歴
    """
    with open(self.csv_file, 'w') as csv_file:
      writer = csv.DictWriter(csv_file,fieldnames = self.__csv_file_column)
      writer.writeheader()
      for id ,data in zip(range(1, self.__id_counter + 2), history_data):
        writer.writerow({
          HISTORY_COLUMN_ID : id,
          HISTORY_COLUMN_WAKEUP_TIME : data[0],
          HISTORY_COLUMN_START_ALARM_TIME : data[1],
          HISTORY_COLUMN_INTERVAL : data[2],
          HISTORY_COLUMN_RINGING_TIME : data[3],
        })
