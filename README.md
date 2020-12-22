# epic_store_bot [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) 
Epic game's weekly free games purchasing bot without spending a single penny.

`I'll make a video tutorial later.`
------------------------------------
Run it on heroku (Recommend) or somewhere

**_if you wanna run it locally or some other place lemme know in the discussion tab._**

# Step by Step (The pain)

  * [Configuration](#configuration)
  * [Heroku](#Heroku)
    * [Create an account](https://signup.heroku.com/dc)
    * [Setup Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) **You need Git installed**
    * [Create an app](#create-an-app)
    * [Add Buildpacks](#Heroku-Buildpacks)
    * [Add Plug-in](#Heroku-Plugin)
    * [Deploy](#Deploy)
    * [Finally](#Web)

# Configuration
  To configure the bot open [config.json](https://github.com/5H4D0W-C0D3R/epic_store_bot/blob/master/config.json)

***

```
  {
	"gmail": {
			"email": "",
			"app_password": ""
		},
```
  email        | Your Gmail address eg: johndoe@gmail.com
  -------------|-----------------------------------
  app_password | See https://devanswers.co/create-application-specific-password-gmail/

***

```
	"facebook": {
			"email": "",
			"password": ""
		},
```
  email        | Your email used to login to facebook
 --------------|-------------------------------------
  password     | Your facebook password

***

```
	"db": {
			"host": "",
			"database": "",
       			"user": "",
			"port": 5432,
			"password": ""
		},
```
  Use ```sh $ heroku pg:credentials:url ``` to get credentials

***

```
	"cronjob": {
			"yourappname": "",
			"email": "",
			"password": ""
		},
```
  Make an account at [Cron-Job.org](https://cron-job.org/en/signup/)
  Yourappname  |  your app name that you created at heroku
  -------------|-------------------------------------------
  email  |  cron-job.org email
  password  | cron-job.org password 
  
***

```
	"web": {
			"username": "root",
			"password": "toor"
		}

}
```
  Web ui credentials it's your choice.

***

# Heroku
 ### [Create an account](https://signup.heroku.com/dc)
 
 ### [Setup Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) **You need Git installed**
 
 ### Create an app
  Continue after ```$ heroku login```
```
  $ heroku create yourappname
```
 ### Heroku-Buildpacks
  Chrome Driver | https://github.com/heroku/heroku-buildpack-chromedriver 
  --------------|---------------------------------------------------------
  Chrome Binary | https://github.com/heroku/heroku-buildpack-google-chrome
```
  $ heroku buildpacks:add --index 1 heroku/python
  $ heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-chromedriver
  $ heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-google-chrome
```
 
 ### Heroku-Plugin
  heroku-postgresql : https://elements.heroku.com/addons/heroku-postgresql
  
Get to the link and use install button
  or ```$ heroku addons:create heroku-postgresql:hobby-dev```
  
 ### Deploy
  ```
     $ cd epic_store_bot
     $ git init
     $ git add -A
     $ git commit -am "first commit"
     $ heroku git:remote -a yourappname
     $ git push heroku master
  ```
 ### Web
  Go to https://yourappname.herokuapp.com
  
  Here you can view purchased items & configure the schedule
  
  Login using the credentials that you gave under [Configuration](#Configuration)
  
  To apply the changes to your app you've to reboot it.
  ```
     $ heroku ps:scale clock=0 -a yourappname   # off
     $ heroku ps:scale clock=1 -a yourappname   # on
  ```

 ### Logging
```
  $ heroku logs -t -a yourappname
```


### Requirements
```sh
gunicorn  # For heroku
requests
flask
selenium
apscheduler
```

License
----

MIT
