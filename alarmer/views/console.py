import os
import string

import termcolor


def get_document_dir_path():
  """documentsディレクトリのパスを返す

  Returns:
    document_dir_path (str): documentsディレクトリのパス
  """
  base_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  document_dir_path = os.path.join(base_dir_path, 'documents')

  return document_dir_path


class NoDocumentError(Exception):
  """ドキュメントが見つからない場合のエラー"""
  pass


def find_document(document_file_name):
  """documentsディレクトリのなかから必要なドキュメントを見つける

  Args:
    document_file_name (str): 必要なドキュメントのファイルネーム

  Returns:
    document_file_path (str): ドキュメントのファイルパス

  Raises:
    NoDocumentError: 必要なドキュメントが見つからない場合に発生する
  """
  document_dir_path = get_document_dir_path()
  document_file_path = os.path.join(document_dir_path, document_file_name)

  if not os.path.exists(document_file_path):
    raise NoDocumentError(f'cannot find {document_file_path}')

  return document_file_path


def get_document(document_file_path, color = None):
  """documentsディレクトリのなかのテキストファイルの内容を
     任意に変更できるかたちで返す

  Args:
    document_file_path (str): ドキュメントのファイルパス
    color: (str): ターミナルに出力するときの文字の色
        詳細: https://pypi.python.org/pypi/termcolor

  Returns:
    string.Template: 任意に変更できるようになった、
    documentsディレクトリのなかのテキストファイルの内容
  """
  document = find_document(document_file_path)

  with open(document, 'r') as document_file:
    content = document_file.read()
    splitter = '=' * 60
    contents = f'{splitter}\n{content}\n{splitter}\n'
    contents = termcolor.colored(contents,color)

    return string.Template(contents)


def make_message_from_document(document_file_name, color, 
sub_error_message = '',  sub_what_do = '', sub_min_minute = '', sub_max_minute = '', 
sub_now = '', sub_ok_or_ng_message = '', sub_wakeup_time = '', sub_start_alarm_time = '', 
sub_interval = '', sub_ringing_time = ''):
  """documentsディレクトリのなかのテキストファイル
     の内容を書き換え、臨機応変にメッセージを作る

  Args:
    document_file_name (str): 開きたいファイルの名前
    color: (str): ターミナルに出力するときの文字の色
        詳細: https://pypi.python.org/pypi/termcolor
    以下 (str): ファイルの内容を書き換えるための文

  Returns:
    message (str): 作成したメッセージ
  """

  message = get_document(document_file_name, color)

  message = message.substitute(
    error_message = sub_error_message,
    what_do = sub_what_do,
    min_minute = sub_min_minute,
    max_minute = sub_max_minute,
    now = sub_now,
    ok_or_ng_message = sub_ok_or_ng_message,
    wakeup_time = sub_wakeup_time,
    start_alarm_time = sub_start_alarm_time,
    interval = sub_interval,
    ringing_time = sub_ringing_time,
  )

  return message
