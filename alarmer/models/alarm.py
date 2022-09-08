from alarmer.views import console
from alarmer.models import history

import pygame
import time
import datetime


DEFAULT_SOUND_VOLUIME = 1.0
DEFAULT_SPEAK_COLOR = 'cyan'
DEFAULT_ERROR_SPEAK_COLOR = 'magenta'


class Robot(object):
  """ロボットを生成するクラスの親クラス"""
  def __init__(self, speak_color = DEFAULT_SPEAK_COLOR,
  error_speak_color = DEFAULT_ERROR_SPEAK_COLOR):
    self.speak_color = speak_color
    self.error_speak_color = error_speak_color


class AlarmRobot(Robot):
  """アラームデータを扱うクラス"""
  def __init__(
    self, speak_color = DEFAULT_SPEAK_COLOR, 
    error_speak_color = DEFAULT_ERROR_SPEAK_COLOR):
      super().__init__(speak_color, error_speak_color)
      self.history_model = history.HistoryModel()


  def __set_minute(self, minute_sub_message, min_minute, max_minute):
    """アラームの「分」を設定する

    Args:
      minute_sub_message (str): minute.txtの内容を書き換えるための文
      min_minute (int): minute.txtの内容を書き換えるための数字、
        ユーザーが入力できる「分」の最小値
      max_minute (int): minute.txtの内容を書き換えるための数字、
        ユーザーが入力できる「分」の最大値

    Returns:
      minute (int): アラームの「分」
    """
    while True:
      text = console.get_document('minute.txt', self.speak_color)
      minute = input(text.substitute(
        what_do = minute_sub_message,
        min_minute = min_minute,
        max_minute = max_minute
      ))

      try:
        minute = int(minute)
      except ValueError:
        error_text = console.get_document(
          'error_message.txt', self.error_speak_color
        )
        print(error_text.substitute(
          error_message = f'{min_minute}から{max_minute}の整数を'
        ))
        continue

      if min_minute <= minute and minute <= max_minute:
        break
      else:
        error_text = console.get_document(
          'error_message.txt',self.error_speak_color
        )
        print(error_text.substitute(
          error_message = f'{min_minute}から{max_minute}の整数を'
        ))
        continue

    return minute


  def __set_hour_and_minute(self, hour_sub_message, minute_sub_message,
    min_minute, max_minute, is_on=True):
    """アラームの「時」と「分」を設定する

    Args:
      hour_sub_message (str): minute.txtの内容を書き換えるための文
      minute_sub_message (str): minute.txtの内容を書き換えるための文
      min_minute (int): minute.txtの内容を書き換えるための数字、
        ユーザーが入力できる「分」の最小値
      max_minute (int): minute.txtの内容を書き換えるための数字、
        ユーザーが入力できる「分」の最大値
      is_on (bool): 「時」を自由に設定するか、0とするかの判別

    Returns:
      hour (int): アラームの「時」
      minute (int): アラームの「分」
    """
    if is_on:
      while True:
        text = console.get_document('hour.txt', self.speak_color)
        hour = input(text.substitute(what_do = hour_sub_message))

        try:
          hour = int(hour)
        except ValueError:
          error_text = console.get_document(
            'error_message.txt', self.error_speak_color
          )
          print(error_text.substitute(error_message = '0から23の整数を'))
          continue

        if 0 <= hour and hour <=23:
          break
        else:
          error_text = console.get_document(
            'error_message.txt', self.error_speak_color
          )
          print(error_text.substitute(error_message = '0から23の整数を'))
          continue
    else:
      hour = 0

    minute = self.__set_minute(minute_sub_message, min_minute,max_minute)

    return hour, minute

  
  def __judge_correct_time_setting(self, wakeup_hour, wakeup_minute, 
  start_alarm_hour, start_alarm_minute, interval_hour, interval_minute, 
  ringing_hour, ringing_minute):
    """アラームの「時」と「分」の設定に矛盾がないか判断する

    Args:
      wakeup_hour (int): 設定された、起きる時刻の「時」
      wakeup_minute (int): 設定された、起きる時刻の「分」
      start_alarm_hour (int): 設定された、アラームを鳴らし始める時刻の「時」
      start_alarm_minute (int): 設定された、アラームを鳴らし始める時刻の「時」
      interval_hour (int): 設定された、アラームを鳴らす間隔の「時」 = 0
      interval_minute (int): 設定された、アラームを鳴らす間隔の「分」
      ringing_hour (int): 設定された、アラームを鳴らし続ける時間の「時」 = 0
      ringing_minute (int): 設定された、アラームを鳴らし続ける時間の「分」

    Returns:
      is_ok (bool): アラームの「時」と「分」の設定に矛盾がないかどうか
    """
    is_ok = True

    if wakeup_hour + wakeup_minute / 60 \
       < start_alarm_hour + start_alarm_minute / 60 \
       or \
       (wakeup_hour + wakeup_minute / 60) \
       - (start_alarm_hour + start_alarm_minute / 60) \
       < interval_hour + interval_minute / 60:
      text = console.get_document('ok_or_ng.txt', self.error_speak_color)
      print(text.substitute(
        ok_or_ng_message = 
        'エラーが起こりました。\n'
        +'以下の点を確認し、もう一度設定してください。\n'
        +'・WAKEUP_TIMEがSTART_ALARM_TIMEより早い\n'
        +'・WAKEUP_TIMEとSTART_ALARM_TIMEの時間差がINTERVALより短い\n',
        wakeup_time = 
          f"{str(wakeup_hour).zfill(2)}:{str(wakeup_minute).zfill(2)}",
        start_alarm_time = 
          f"{str(start_alarm_hour).zfill(2)}:{str(start_alarm_minute).zfill(2)}",
        interval = 
          f"{str(interval_hour).zfill(2)}:{str(interval_minute).zfill(2)}",
        ringing_time = 
          f"{str(ringing_hour).zfill(2)}:{str(ringing_minute).zfill(2)}",
      ))

      is_ok = False

    return is_ok


  def __set_all_time(self):
    """起きる時刻、アラームを鳴らし始める時刻、何分ごとにアラームを鳴らすか、
       何分間アラームを鳴らし続けるか、を設定し、CSVファイルに書き込む関数を呼ぶ
    """
    while True:
      self.__wakeup_hour, self.__wakeup_minute \
        = self.__set_hour_and_minute(
          '起きますか？', '', 0, 59)
      self.__start_alarm_hour, self.__start_alarm_minute \
        = self.__set_hour_and_minute(
          'アラームを鳴らし始めますか？', '', 0, 59)
      interval_hour, self.__interval_minute \
        = self.__set_hour_and_minute(
          '', '何分おきにアラームを鳴らしますか？\n' ,5, 59, False)
      ringing_hour, self.__ringing_minute \
        = self.__set_hour_and_minute(
          '', '何分間アラームを鳴らし続けますか？\n', 1, 3, False)

      correct_time_setting = self.__judge_correct_time_setting(
        self.__wakeup_hour, self.__wakeup_minute, self.__start_alarm_hour,
        self.__start_alarm_minute, interval_hour, self.__interval_minute,
        ringing_hour, self.__ringing_minute)
      if correct_time_setting:
        break

    self.wakeup_time = \
    f"{str(self.__wakeup_hour).zfill(2)}:{str(self.__wakeup_minute).zfill(2)}"
    self.start_alarm_time = \
    f"{str(self.__start_alarm_hour).zfill(2)}:{str(self.__start_alarm_minute).zfill(2)}"
    self.__interval = \
    f"{str(interval_hour).zfill(2)}:{str(self.__interval_minute).zfill(2)}"
    self.__ringing_time = \
    f"{str(ringing_hour).zfill(2)}:{str(self.__ringing_minute).zfill(2)}"

    text = console.get_document('ok_or_ng.txt', self.speak_color)
    print(text.substitute(
      ok_or_ng_message = '以下の通りに設定しました。\n',
      wakeup_time = self.wakeup_time,
      start_alarm_time = self.start_alarm_time,
      interval = self.__interval,
      ringing_time = self.__ringing_time,
    ))

    time_data = [
      self.wakeup_time,
      self.start_alarm_time,
      self.__interval,
      self.__ringing_time
    ]

    if not time_data in self.__history_data:
      self.__history_data.append(time_data)
      self.history_model.save(self.__history_data)


  def use_past_settings(self):
    """履歴を使用するかどうかを判別し、結果に応じて相応しい関数を呼ぶ"""
    self.__history_data = self.history_model.load_history_exclude_header()
    if not self.__history_data:
      is_yes = False
    else:
      while True:
        text = console.get_document('past_settings.txt', self.speak_color)
        input_is_yes = input(text.substitute())
        if input_is_yes.lower() == 'n' or input_is_yes.lower() == 'no':
          is_yes = False
          break
        elif input_is_yes.lower() == 'y' or input_is_yes.lower() == 'yes':
          is_yes = True
          break
        else:
          error_message = console.get_document(
            'error_message.txt', self.error_speak_color
          )
          print(error_message.substitute(
            error_message='y, yes, n, noのいずれか（大文字・小文字は問いません）を'
          ))
          continue
    
    if is_yes:
        self.__fetch_past_settings()
    else:
      self.__set_all_time()

  
  def __undone_time_to_int(self, str_time):
    """string型になっているアラームの「時」と「分」をint型に戻す

    Args:
      str_time (str): string型になっているアラームの「時」と「分」

    Returns:
      int_hour (int): int型に戻したアラームの「時」
      int_minute (int): int型に戻したアラームの「分」
    """
    if str_time[0] == '0':
      int_hour = int(str_time[1])
    else:
      int_hour = int(str_time[:2])
      
    if str_time[3] == '0':
      int_minute = int(str_time[-1])
    else:
      int_minute = int(str_time[3:])

    return int_hour, int_minute

    
  def __fetch_past_settings(self):
    """どの履歴を使用するか決定する"""
    rows = self.history_model.load_history_include_header()
    is_ok=False

    while True:
      text = console.get_document('which_setting.txt', self.speak_color)
      user_id_choice = input(text.substitute())
      
      for j in range(1, (int(rows[-1][0]) + 1)):
        if user_id_choice == rows[j][0]:
          text = console.get_document('ok_or_ng.txt', self.speak_color)
          print(text.substitute(
            ok_or_ng_message = '以下の通りに設定しました。\n',
            wakeup_time = rows[j][1],
            start_alarm_time = rows[j][2],
            interval = rows[j][3],
            ringing_time = rows[j][4],
          ))

          self.wakeup_time = rows[j][1]
          self.start_alarm_time = rows[j][2]
          self.__interval = rows[j][3]
          self.__ringing_time = rows[j][4]

          self.__wakeup_hour ,self.__wakeup_minute = \
            self.__undone_time_to_int(rows[j][1])
          self.__start_alarm_hour ,self.__start_alarm_minute = \
            self.__undone_time_to_int(rows[j][2])
          not_use ,self.__interval_minute = \
            self.__undone_time_to_int(rows[j][3])
          not_use ,self.__ringing_minute = \
            self.__undone_time_to_int(rows[j][4])

          is_ok=True
          break

      if is_ok:
        break
      else:
        error_message = console.get_document(
          'error_message.txt', self.error_speak_color
        )
        print(error_message.substitute(
          error_message = '表示されているIDのいずれかを'
        ))
        continue


  def __set_music(self):
    """鳴らす音の設定"""
    pygame.mixer.init()
    music = None

    try:
      import settings
      if settings.MUSIC_FILE_NAME:
        music = settings.MUSIC_FILE_NAME
    except ImportError:
      pass
    
    if music is None:
      music=console.find_document('LGvoice.mp3')
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(DEFAULT_SOUND_VOLUIME)


  def __play_music(self):
    """音を鳴らす"""
    self.__set_music()
    now = datetime.datetime.now().strftime('%H:%M')
    text = console.get_document('hello.txt', self.error_speak_color)
    print(text.substitute(now = now))
    pygame.mixer.music.play(-1)
    time.sleep(self.__ringing_minute * 60)


  def __stop_music(self):
    """音を止める"""
    self.__set_music()
    pygame.mixer.music.stop()


  def __how_many_times_sound(self):
    """起きる時間に鳴らすアラームを除き、
       合計何回アラームを鳴らすか決める

    Returns:
      counter (int):
    """
    int_wakeup_time = datetime.time(self.__wakeup_hour, self.__wakeup_minute, 0)
    counter = 1

    while True:
      self.__start_alarm_minute = self.__start_alarm_minute + self.__interval_minute

      if self.__start_alarm_minute >= 60:
        self.__start_alarm_minute = self.__start_alarm_minute - 60
        self.__start_alarm_hour += 1
        if self.__start_alarm_hour >= 24:
          self.__start_alarm_hour = self.__start_alarm_hour - 24

      int_start_alarm_time = \
        datetime.time(self.__start_alarm_hour, self.__start_alarm_minute, 0)

      if int_start_alarm_time < int_wakeup_time:
        counter += 1
      else:
        break

    return counter


  def sub_sound(self):
    """アラームを鳴らし始める時刻から、設定した時間ごとにアラームを鳴らす"""
    how_many_times_sound = self.__how_many_times_sound()

    for i in range(how_many_times_sound):
      self.__play_music()
      self.__stop_music()
      if i != (how_many_times_sound - 1):
        time.sleep((self.__interval_minute - self.__ringing_minute) * 60)


  def main_sound(self):
    """起きる時刻にアラームを鳴らす"""
    self.__play_music()
    self.__stop_music()
    exit()