
import sched
from datetime import datetime, timedelta
import time
# SE DER TEMPO FAZER POLIMORFISMO DESSA CLASSE
from singleton_slack import slack


class BotScheduler(object):

    def __init__(self):
        self._scheduler = sched.scheduler(timefunc=time.time,
                                          delayfunc=time.sleep)
        self._delta_time_hours = 24

    def _rescheduler(self):
        next_sched = datetime.now() + timedelta(hours=self._delta_time_hours)
        self.operator()

        self._scheduler.enterabs(time.mktime(next_sched.timetuple()),
                                 priority=0,
                                 action=self._rescheduler,
                                 argument=())

    def _set_time(self, hours, minutes):
        """
        Set the start time of the reduction process.
        """
        current_time = datetime.now()
        set_time = current_time.replace(hour=hours, minute=minutes)
        delta_time = set_time - current_time
        if delta_time.total_seconds() < 0:
            next_time = current_time + timedelta(hours=12)
            next_time = next_time.replace(hour=hours, minute=minutes)
        else:
            next_time = set_time

        self._scheduler.enterabs(time.mktime(next_time.timetuple()),
                                 priority=0,
                                 action=self._rescheduler,
                                 argument=())

    def operator(self):
        slack.send_message_users()

    def run(self, hours=0, minutes=0):
        """
        Start the scheduler.
        input:
            hours: the hour of firts reduction start
            minutes: the minutes of firts reduction start
        """
        self._set_time(hours, minutes)
        try:
            self._scheduler.run()
        except KeyboardInterrupt:
            print('error')

