import sqlite3


HISTORY_COLUMN_ID = 'ID'
HISTORY_COLUMN_WAKEUP_TIME = 'WAKEUP_TIME'
HISTORY_COLUMN_START_ALARM_TIME = 'START_ALARM_TIME'
HISTORY_COLUMN_INTERVAL = 'INTERVAL'
HISTORY_COLUMN_RINGING_TIME = 'RINGING_TIME'
HISTORY_DB_FILE_NAME = 'history.db'


class DataModel(object):
  """DBを扱うクラスの親クラス"""
  def __init__(self, db_file):
    self.db_file = db_file
    try:
      self.conn = sqlite3.connect(self.db_file)
    except sqlite3.OperationalError:
      pass


class HistoryModel(DataModel):
  """アラームの履歴を読み書きするクラス"""
  def __init__(self, db_file = None):
    if db_file is None:
      db_file = self.__get_db_file_name()
    super().__init__(db_file)
    self.id_counter = 0
    self.__history_data = []


  def load_history_define_id(self):
    """DBを読み込む。
       これから設定するアラームのIDを決めるため、
       これまでの最大のIDを取得しておく。

    Returns:
      self.history_data (tuple): DBの内容
    """
    curs = self.conn.cursor()
    try:
      curs.execute('select * from history')
      self.__history_data = curs.fetchall()
      curs.execute('select max(id) from history')
      id_counter_tuple = curs.fetchone()
      self.id_counter = id_counter_tuple[0]
    except sqlite3.OperationalError:
      pass
    if self.id_counter == None:
      self.id_counter = 1
    self.conn.commit()

    return self.__history_data


  def load_and_print_history(self):
    """DBを読み込む.。
       履歴を出力する。

    Returns:
      rows (tuple): DBの内容
    """
    curs = self.conn.cursor()
    curs.execute('select * from history')
    rows = curs.fetchall()
    self.conn.commit()

    print(HISTORY_COLUMN_ID,end='　')
    print(HISTORY_COLUMN_WAKEUP_TIME,end='　')
    print(HISTORY_COLUMN_START_ALARM_TIME,end='　')
    print(HISTORY_COLUMN_INTERVAL,end='　')
    print(HISTORY_COLUMN_RINGING_TIME,end='　')
    print()
    for j in range(self.id_counter):
      print(rows[j][0], end = '')
      print('　　　　', rows[j][1], end = '')
      print('　　　　　　', rows[j][2], end = '')
      print('　　', rows[j][3], end = '')
      print('　　　　', rows[j][4])

    return rows

  
  def __get_db_file_name(self):
    """DBの名前を設定する
        
    Returns:
      db_file_name (str): DBの名前
    """
    db_file_name = None

    try:
      import settings
      if settings.DB_FILE_NAME:
        db_file_name = settings.DB_FILE_NAME
    except ImportError:
      pass

    if db_file_name is None:
      db_file_name = HISTORY_DB_FILE_NAME

    return db_file_name


  def save(self, time_data):
    """DBに書き込む

    Args:
      time_data (tuple): アラームの履歴
    """
    curs = self.conn.cursor()
    self.id_counter = self.id_counter + 1
    try:
      curs.execute(
        f'''create table history\
        ({HISTORY_COLUMN_ID} integer,\
        {HISTORY_COLUMN_WAKEUP_TIME} string,\
        {HISTORY_COLUMN_START_ALARM_TIME} string,\
        {HISTORY_COLUMN_INTERVAL} string,\
        {HISTORY_COLUMN_RINGING_TIME} string)'''
      )
    except sqlite3.OperationalError:
      pass
    curs.execute(
      f'''insert into history\
      ({HISTORY_COLUMN_ID}, {HISTORY_COLUMN_WAKEUP_TIME},\
      {HISTORY_COLUMN_START_ALARM_TIME}, {HISTORY_COLUMN_INTERVAL},\
      {HISTORY_COLUMN_RINGING_TIME})\
      values({self.id_counter},\
      {time_data[0]}, {time_data[1]}, {time_data[2]}, {time_data[3]})'''
    )
    self.conn.commit()