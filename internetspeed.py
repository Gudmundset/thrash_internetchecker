from datetime import datetime
import speedtest
from functools import lru_cache
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, Bruce!</h1>"

@lru_cache(maxsize=5)
def check_speed(rtype):
    st = speedtest.Speedtest()
    if rtype == 'all':
        download = round(st.download()/1000000,2)
        upload = round(st.upload()/1000000,2)
        return download, upload
    if rtype == 'download':
        download = round(st.download()/1000000,2)
        upload = round(st.upload()/1000000,2)
        return download
    if rtype == 'upload':
        upload = round(st.upload()/1000000,2)
        return upload

@app.route('/internetspeed/<rtype>')
def internetspeed(rtype):
    if rtype == "all":
        download, upload = check_speed(rtype)
        return {"download": download, "upload": upload}
    if rtype == "download":
        download = check_speed(rtype)
        return {"download": download}
    if rtype == "upload":
        upload = check_speed(rtype)
        return {"upload": upload}

if __name__ == '__main__':
    # replace with your network IP, usually through
    # ifconfig on linux or ipconfig on windows
    app.run(host="0.0.0.0", debug=False)
