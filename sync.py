import requests as rq
import json


sid: int


def newSession(name: str, script: str) -> bool:
    global sid

    try:
        rsp: rq.Response = rq.post('http://127.0.0.1:5000/new',
            json={'name': name, 'script': script})
    except Exception: return True #False

    if rsp.status_code != 200:
        return True #False
    else:
        sid = int(json.loads(rsp.text)['sid'])
        print(sid)
        return True



