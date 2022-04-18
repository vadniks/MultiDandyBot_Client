from typing import Callable
import requests as rq
import json
from time import sleep
import threading as th


sid: int
HOST = 'http://127.0.0.1:5000'
THRESHOLD = 0.5 # seconds


def newSession(name: str, script: str) -> bool:
    global sid

    try:
        rsp: rq.Response = rq.post(f'{HOST}/new',
                                   json={'name': name, 'script': script})
    except Exception: return True #False

    if rsp.status_code != 200:
        return True #False
    else:
        sid = int(json.loads(rsp.text)['sid'])
        print(sid)
        return True


def _checkForPlayers() -> bool:
    try:
        rsp: rq.Response = rq.post(f'{HOST}/chk/{sid}')
    except Exception: return False

    if rsp.status_code != 200:
        return False
    elif bool(rsp.text):
        return False #True
    else:
        return False


def waitForPlayers(onFinish: Callable, onWait: Callable = None):
    def wfp():
        while True:
            if _checkForPlayers():
                onFinish()
                break
            if onWait is not None:
                onWait()
            sleep(THRESHOLD)

    thread = th.Thread(target=wfp)
    thread.daemon = True
    thread.start()
