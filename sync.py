from typing import Callable, List
import requests as rq
import json
from time import sleep
import threading as th


sid: int
pid: int
name: str
HOST = 'http://127.0.0.1:5000'
THRESHOLD = 0.5 # seconds


def newSession(_name: str, script: str) -> bool:
    global sid, pid, name
    name = _name

    try:
        rsp: rq.Response = rq.post(f'{HOST}/new',
                                   json={'name': name, 'script': script})
    except Exception: return True #False

    if rsp.status_code != 200:
        return True
    else:
        sid = int(json.loads(rsp.text)['sid'])
        pid = int(json.loads(rsp.text)['pid'])
        print(sid, pid)
        return True


def _checkForPlayers() -> List[str] | None:
    try:
        rsp: rq.Response = rq.get(f'{HOST}/chk/{pid}')
    except Exception: return None

    if rsp.status_code != 200:
        return None
    else:
        a = json.loads(rsp.text)
        return a


def waitForPlayers(onFinish: Callable, onWait: Callable = None):
    def wfp():
        while True:
            if (players := _checkForPlayers()) is not None and len(players) > 0:
                onFinish(players)
                break
            if onWait is not None:
                onWait()
            sleep(THRESHOLD)

    thread = th.Thread(target=wfp)
    thread.daemon = True
    thread.start()


def quitt():
    try:
        rsp: rq.Response = rq.post(f'{HOST}/qt/{pid}')
    except Exception: pass
