from alarmer.models import alarm

import schedule
import time


def set_alarm():
  alarm_robot = alarm.AlarmRobot()
  alarm_robot.use_past_settings()
  schedule.every().day.at(alarm_robot.start_alarm_time).do(alarm_robot.sub_sound)
  schedule.every().day.at(alarm_robot.wakeup_time).do(alarm_robot.main_sound)
  while True:
    schedule.run_pending()
    time.sleep(1)