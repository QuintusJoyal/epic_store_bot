from flask import make_response, request
import flask
import json
import pytz
from lib.config import Config
from lib.pgdb import Dtabase as DB
from lib.cronJob import CronJob as cj

config = Config()
app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def web():
    gdta = DB().get_dta('games_ordered')
    code = '<script>function openform(){ document.getElementById("lform").style.display = "block"; document.getElementById("butt").style.display = "none"; }</script>'
    code += '<center style="font-family: Arial, Helvetica, sans-serif;"><h4>Check_this_out: <a href="https://epicgamesfree4all.herokuapp.com/" target="new" style="text-decoration: none;">Link</a></h4>'
    code += '<h2>Purchased_list</h2>'
    code += '<div id="lform" style="display: none;"><form method="POST" action="/login" target="_parent"><input type="text" name="username" placeholder="Username" required /><br /><input type="password" name="password" placeholder="Password" required /><br /><input type="submit" value="Login" style="background: blue; color: white; padding: 8px; font-size: large; border-radius: 4px;" /></form></div><input type="button" value="Settings" onclick="openform()" id="butt" style="overflow: hidden;display: block;background: blue;color: white; padding: 8px; font-size: large; opacity: 0.4; border-radius: 4px;"/>'
    code += '<table border="0" style="border-collapse: collapse; width: 80%; margin: 1.5em; font-size: 1em;">'
    for i in list(gdta.keys()):
        dta = gdta[i]
        code += '''<tr style="border-bottom: 2px solid black; background: lightgray;">
                        <td>
                           <img src="{0}" style="height: 25%; width: auto;"/>
                        </td>
                        <td align="center" style="font-weight: bolder;font-size: larger;">
                           {1}
                        </td>
                    </tr>'''.format(dta['thumbnail'], dta['title'])

    code += '</table></center>'
    
    return make_response(code, 200)

@app.route('/login', methods=['POST'])
def log():                                             # login.
    username = request.form['username']
    password = request.form['password']
    code = '<center style="font-family: Arial, Helvetica, sans-serif;" ><script>function defaultval(){ const tz = Intl.DateTimeFormat().resolvedOptions().timeZone; document.getElementById("timez").value = tz;};</script>'
    if username == config['web']['username'] and password == config['web']['password']:       # change it if you want to.
        code += '<h1>Settings</h1><br /><form method="POST" action="/settings" target="_parent"><table><tr><td colspan=2 align="center">Days to run every week from <select name="day1">{0}</select> to <select name="day2">{0}</select></td></tr><tr><td align="left">Time to run : </td><td align="left"><input type="time" name="time" required /></td></tr><tr><td align="left">Timezone : </td><td align="left"><input list="tz" id="timez" name="timezone" value="" required /><datalist id="tz">{1}</datalist><input type="button" onclick="defaultval()" value="Guess" /></td></tr><tr><td colspan=2 align="center"><input type="submit" value="Apply" style="background: blue; color: white; padding: 8px; font-size: large; border-radius: 4px;" /></td></tr></table></form>'.format(''.join([ '<option value="{0}">{1}</option>'.format(sd, dd) for sd, dd in { 'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'wednesday', 'thu': 'Thursday', 'fri': 'Friday', 'sat': 'Saturday', 'sun': 'Sunday' }.items()]), ''.join([ '<option value="{0}">'.format(t) for t in pytz.all_timezones ]))
        code += '<br /><h2 align="center">Current_Settings</h2><pre align="left">'
        conf = DB().get_dta('bot_config')
        code += '<br />{}'.format(json.dumps(conf, indent=4))
    else:
        code += '<h1>Kinda_sus... Code: 666</h1>'

    code += '</center>'
    return make_response(code, 200)

@app.route('/settings', methods=['POST'])
def conf():
    config = { "days": str(request.form['day1']) + "-" + str(request.form['day2']), "hour": int(request.form['time'].split(':')[0]), "minute": int(request.form['time'].split(':')[1]), "timezone": request.form['timezone'] }

    DB().ins_conf(json.dumps(config))
    DB().con_close()
    
    try:
        cj().update()
    except Exception as e:
        print(e)
    return make_response('<center style="font-family: Arial, Helvetica, sans-serif;" ><h1>Settings_Updated</h1><br /><br /><input type="button" value="Go back" style="background: blue; color: white; padding: 8px; font-size: large; border-radius: 4px;" onclick="window.location.href = \'/\'"></center>', 200)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
