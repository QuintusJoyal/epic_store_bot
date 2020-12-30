import json
import os
import re
import requests


with open("config.json", "r") as old_config:
    config = json.load(old_config)

def update_config():
    with open("config.json", "w") as new_config:
        json.dump(config, new_config, indent=4)

def deploy():
    if os.name == "nt":
        os.system("del tmp")
    else:
        os.system("rm tmp")

    os.system("git commit -am 'deploying'")
    os.system("git push heroku master")

def heroku():
    print("Make sure you have Git")
    
    os.system("git init")
    os.system("git add -A")

    if os.name == "nt":
        os.system("start " + "https://id.heroku.com/login")
        try:
            os.system("heroku --version")
        except:
            if os.environ['PROCESSOR_ARCHITECTURE'].endswith('64'):
                r = requests.get("https://cli-assets.heroku.com/heroku-x64.exe")
                open("heroku-x64.exe", "wb+").write(r.content)
                os.system("heroku-x64.exe")
            else:
                r = requests.get("https://cli-assets.heroku.com/heroku-x86.exe")
                open("heroku-x86.exe", "wb+").write(r.content)
                os.system("heroku-x86.exe")

    else:
        os.system("open " + "https://id.heroku.com/login")
        os.system("curl https://cli-assets.heroku.com/install.sh | sh")

    input("Login then press any key...")

    os.system("heroku login")
    
    while True:
        app_name = input("How you wanna call your bot?( eg: epicbot1234 )\n: ")

        os.system("heroku create {} > tmp 2>&1".format(app_name))
        with open("tmp", "r") as tmp:
            if not re.findall(r"Name {} is already taken".format(app_name), tmp.read()):
                break
            else:
                print("Name already taken, Try again")
            
    os.system("heroku git:remote -a {}".format(app_name))
    os.system("heroku buildpacks:add --index 1 heroku/python -a {}".format(app_name))
    os.system("heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-chromedriver -a {}".format(app_name))
    os.system("heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-google-chrome -a {}".format(app_name))
    os.system("heroku addons:create heroku-postgresql:hobby-dev -a {}".format(app_name))
    os.system("heroku authorizations:create -d {}".format(app_name))
    os.system("heroku authorizations -j > tmp")
    with open("tmp", "r") as tmp:
        for i in json.load(tmp):
            if i['description'] == app_name:
                api_token = i['access_token']['token']

    config['cronjob']['yourappname'] = app_name
    config['cronjob']['api_token'] = api_token

def gmail():
    print("Give your gmail info")

    email = input("Your Gmail (eg: example@gmail.com)\n: ")

    if os.name == "nt":
        os.system("start https://myaccount.google.com/apppasswords")
    else:
        os.system("open https://myaccount.google.com/apppasswords")

    app_password = input("Your App password\n: ")

    config['gmail']['email'] = email
    config['gmail']['app_password'] = app_password

def facebook():
    print("Give your facebook info")

    email = input("Facebook Username or email\n: ")
    
    password = input("Facebook password\n: ")

    config['facebook']['email'] = email
    config['facebook']['password'] = password

def database():
    db = {}
    try:
        os.system("heroku pg:credentials:url > tmp")
        with open("tmp", "r") as tmp:
            for l in re.findall(r'"dbname=.*"', tmp.read())[0].strip('"').split(" "):
                db[l.split("=")[0]] = l.split("=")[1]

        config['db']['host'] = db['host']
        config['db']['database'] = db['dbname']
        config['db']['user'] = db['user']
        config['db']['password'] = db['password']
        config['db']['port'] = db['port']

    except:
        print("Setup Heroku first")

def cronjob():
    if os.name == "nt":
        os.system("start https://cron-job.org/en/signup/")
    else:
        os.system("open https://cron-job.org/en/signup/")

    email = input("Email you used to login\n: ")
    password = input("Password\n: ")

    config['cronjob']['email'] = email
    config['cronjob']['password'] = password

def web_ui():
    username = input("Username (root)\n: ")
    password = input("Password (toor)\n: ")

    if username == "" or password == "":
        pass
    else:
        config['web']['username'] = username
        config['web']['password'] = password

def setupBot():
    print("\nSetting up heroku...".center(10))
    heroku()
    print("\nSetting up Gmail...".center(10))
    gmail()
    print("\nSetting up Facebook...".center(10))
    facebook()
    print("\nSetting up Cron-Job...".center(10))
    cronjob()
    print("\nSetting up Web-UI...".center(10))
    web_ui()

if __name__ == '__main__':
    print("\nStarting the setup...".center(10))
    setupBot()
    print("\nSaving the config...".center(10))
    update_config()
    print("\nDeploying...".center(10))
    deploy()
    print("\nDone".center(10))
