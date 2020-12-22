import requests
import re
from .config import Config
from .pgdb import Dtabase as db

config = Config()

class CronJob:
    def __init__(self):

        t = db().get_dta('bot_config')

        h, m = divmod((t['hour'] * 60 + t['minute']) - 5, 60)

        session = requests.session()
        data = { 
                    "login": {
                                "action": "login",
                                "email": config['cronjob']['email'],
                                "pw": config['cronjob']['password']
                            },
                    "add": {
                                "action": "add",
                                "title": config['cronjob']['yourappname'],
                                "url": "http://" + str(config['cronjob']['yourappname']) + ".herokuapp.com/",
                                "exec_mode": "day_time",
                                "day_time_hour": h,
                                "day_time_minute": m,
                                "notify_disable": "on"
                            },
                    "edit": {
                                "action": "save",
                                "title": config['cronjob']['yourappname'],
                                "url": "http://" + str(config['cronjob']['yourappname']) + ".herokuapp.com/",
                                "exec_mode": "day_time",
                                "day_time_hour": h,
                                "day_time_minute": m,
                                "timezone": t['timezone'],
                                "enabled": "on",
                                "notify_disable": "on"
                            }
                }
        session.post("https://cron-job.org/en/members/", data=data['login'])

        self.session = session
        self.data = data
    
    def add(self):

        self.session.post("https://cron-job.org/en/members/jobs/add/", data=self.data['add'])

    def update(self):

        res = self.session.post("https://cron-job.org/en/members/jobs/")

        if "You did not create a cronjob yet" in res.text:
            self.add()
        else:
            jobid = re.findall(r"jobid=\d*", res.text)[0].strip('jobid=')

            print(jobid)

            self.session.post("https://cron-job.org/en/members/jobs/edit/?jobid={}".format(jobid), data=self.data['edit'])

        self.session.cookies.clear()

