from unittest import result
import pytest

from alarmer.models import alarm
from alarmer.models import history
from alarmer.views import console

@pytest.mark.skip(reason='This method is private.')
def test_undone_time_to_int():
  test_alarm_robot = alarm.AlarmRobot()
  result1_hour, result1_minute = \
    test_alarm_robot.undone_time_to_int('12:12')
  result2_hour, result2_minute = \
    test_alarm_robot.undone_time_to_int('02:02')

  assert result1_hour == 12
  assert result1_minute == 12
  assert result2_hour == 2
  assert result2_minute == 2


class TestHistory(object):
  def setup_method(self):
    self.test_history_model = history.HistoryModel()
    

  @pytest.mark.skip(reason='This method is private.')
  def test_get_csv_file_name(self):
    result = self.test_history_model.get_csv_file_name()

    assert result == 'history.csv'


  def test_load_history_include_header(self):
    result = self.test_history_model.load_history_include_header()

    assert not result is False


  def test_load_history_exclude_header(self):
    result = self.test_history_model.load_history_exclude_header()

    assert not result is True

  
  def test_save(self):
    self.test_history_model.save([['11:00', '10:00', '00:05', '00:01']])
    result = self.test_history_model.load_history_exclude_header()

    assert not result is False


def test_find_document():
  result = console.find_document('hour.txt')

  assert result == \
    '/Users/kawaguchitoui/Downloads/ALARM/alarmer/documents/hour.txt'


def test_find_document_raise():
  with pytest.raises(console.NoDocumentError):
    console.find_document('abc.txt')