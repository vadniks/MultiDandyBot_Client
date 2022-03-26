import requests as rq
import json


sid: int


def newSession(name: str, script: str):
    global sid

    try:
        rsp: rq.Response = rq.post('http://127.0.0.1:5000/new',
            json={'name': name, 'script': script})
    except Exception: return None

    if rsp.status_code != 200:
        return False
    else:
        sid = int(json.loads(rsp.text)['sid'])
        print(sid)
        return True
