from lib.main import Bot
from lib.pgdb import Dtabase as DB
import json
from apscheduler.schedulers.blocking import BlockingScheduler

c = DB().get_dta('bot_config')
sched = BlockingScheduler(timezone=c['timezone'])

@sched.scheduled_job('cron', day_of_week=c['days'], hour=c['hour'], minute=c['minute'])
def trigg():
    try:
        Bot().main()
    except Exception as ee:
        print('error trig: ' + str(ee))

    DB().con_close()

if __name__ == '__main__':
    try:
        sched.start()
    except Exception as e:
        print('error sch: ' + str(e))
