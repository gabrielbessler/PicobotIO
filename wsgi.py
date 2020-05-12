from PicoIO import app
# WSGI only looks for the default name 'application'
# this file is actually somewhat unecessary, we could point the GUnicorn server
# directly at the real module

if __name__ == "__main__":
    app.run(host='0.0.0.0')
