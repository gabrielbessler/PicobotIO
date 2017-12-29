# PicobotIO
Multiplayer version of Picobot game created at MuddHacks (Harvey Mudd Hackathon) 
by Gabriel Bessler, Tyler Sam, Sam Tan, and Jake Lawrence 

## Local Testing 
In order to build the application, first start the python virtual environment by running 
```
\venv\Scripts\activate
```
Next, 
```
set FLASK_APP=Main.py
python -m flask run
```
By default, this will start the app on `http://127.0.0.1:5000.`

## Hosting Online 

The application is currently hosted [here](http://www.gabebessler.com). 
It uses a GUnicorn server behind NGINX to deploy the Python WSGI App*

*for more information on how this is done, check out this 
[digitalocean tutorial](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx)


## Libraries 
Frontend: JS, AJAX, jQuery

[Bootstrap 3](http://www.google.com) - Frontend styling 

[Flask](http://www.google.com) - Python backend microframework 


