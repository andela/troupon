# ![bucketlist logo](http://s27.postimg.org/x0kjz2v33/logo_horizontal_small.png)
[![Circle CI](https://circleci.com/gh/andela/troupon/tree/develop.svg?style=shield)](https://circleci.com/gh/andela/troupon/tree/develop) [![Coverage Status](https://coveralls.io/repos/andela/troupon/badge.svg?branch=develop&service=github)](https://coveralls.io/github/andela/troupon?branch=develop) [![Circle CI](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg)

### Table of Contents
1.  [Introduction](#introduction)
2.  [Features](#features)
3.  [Installation](#installation)
4.  [Team](#team)
5.  [Demo](#demo)

### <a name="introduction"></a>Introduction
Troupon is a Groupon clone. Users are able to buy products and services at a discounted price.

### <a name="features"></a>Features
- Users can search for deals by cities.
- Users can view maps of deals.
- Users can search for deals by categories.

### <a name="installation"></a>Installation
- Clone repo: `$ git clone https://github.com/andela/troupon.git`
- Checkout to branch develop: `$ git checkout develop`
- Create a .env.py file in your root directory. In it put the following key - value pairs:
	```cmd
	DB_USER = "your_database_username_here"
	DB_PASSWORD = "your_database_password_here"
	MAILGUN_URL = "your_mailgun_url_here"
	MAILGUN_USERNAME = "your_mailgun_username_here"
	MAILGUN_PASSWORD = "your_mailgun_password_here"
	SECRET_KEY = "abcdefghijklmnop"
	```
	**Important**: the secret key must be of length 16, 24 or 32 bytes.   

- Run `$ pip install -r requirements.txt` to install all dependencies.
- Ensure npm and bower are installed in your environment.
- Run `$ bower install` in the project root folder.
- Run `$ python manage.py collectstatic` to collect static files.
- Run `$ python troupon/manage.py runserver` to start the server. 
- With that you can view the project in your browser via `http://127.0.0.1:8000/`.

##### Sass Setup
The codebase also includes the Sass build files used to style/theme the application. These can be found in the `troupon/static/scss` folder. Follow the steps below to setup **gulp** and **gulp-sass** for automated pre-processing of the __scss__ files to __css__ stylesheets:   
+ Ensure npm is installed in your environment.
+ Run `$ npm install` in the project root folder. This installs **gulp**, **gulp-sass** and it's other dependencies into the project.
+ Run `$ gulp` command for the initial Sass build as well as to start the 'watch' task responsible for pre-processing subsequent changes the Sass __scss__ files.   


To extend this Sass build with your own Sass styles:   
+ Write them in a Sass partial (.scss file named starting with an underscore e.g `_merchants.scss`) and save it in the `troupon/static/scss/partials` folder.
+ Import the partial at the end the `base_styles.scss` file. e.g 
  
  ```
  ...
  @import "partials/_merchants";
  ```

### <a name="team"></a>Team
- [Oluwatosin Adesanya](https://github.com/andela-tadesanya)
- [Samuel James](https://github.com/andela-sjames)
- [Oluwafemi Sule](https://github.com/andela-osule)
- [Awili Uzo](https://github.com/andela-uawili)
- [Amos Omondi](https://github.com/andela-aomondi)
- [Penina Wanjiru](https://github.com/andela-pwanjiru)
- [Jack Mwangi](https://github.com/andela-jmwangi)

### <a name="demo"></a>Demo
View our live demo on heroku at [http://troupon-staging.herokuapp.com/](http://troupon-staging.herokuapp.com/)