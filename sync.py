"""
MIT License

Copyright (c) 2022 Vad Nik (https://github.com/vadniks)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Callable, List, Tuple
import requests as rq
import json
from time import sleep
from threading import Thread


sid = -1
pid = 0
name: str
level = 0
_HOST = 'http://127.0.0.1:5000'
_THRESHOLD = 0.5 # seconds
_waiterThread: Thread
_canWaitForServer = True
solo = True
_isReady = False


def connect(_name: str, script: str) -> bool:
    global sid, pid, name
    name = _name

    try:
        rsp: rq.Response = rq.post(f'{_HOST}/new',
            json={'name': name, 'script': script, 'level': level})
    except Exception: return False

    if rsp.status_code == 200:
        if (sid := int(json.loads(rsp.text)['sid'])) == -1:
            return False

        pid = int(json.loads(rsp.text)['pid'])
        return True


#                                   id   name status
def checkForPlayers() -> List[Tuple[int, str, bool]] | None:
    try:
        rsp: rq.Response = rq.get(f'{_HOST}/chk/{pid}')
    except Exception: return None

    if rsp.status_code != 200:
        return None
    else:
        a = json.loads(rsp.text)
        _list = [(int(i[0]), i[1], bool(i[2])) for i in a]
        return _list


def waitForPlayers(onWait: Callable, onFinish: Callable) -> Callable: # stop
    global _waiterThread, _canWaitForServer, _isReady

    def checkStatus(players: List[Tuple[int, str, bool]]) -> bool:
        result = True
        for i in players: result = result and i[2]
        return result

    def wait():
        while _canWaitForServer:
            if (players := checkForPlayers()) is not None:
                if len(players) > 0 and checkStatus(players) and _isReady:
                    onFinish(players)
                    break
                else:
                    onWait(players)
            else:
                onWait(None)
            sleep(_THRESHOLD)

    _waiterThread = Thread(target=wait)
    _waiterThread.daemon = True
    _waiterThread.start()

    return endWaiter


def endWaiter():
    global _canWaitForServer
    _canWaitForServer = False
    _waiterThread.join()


def quitt():
    try: rq.post(f'{_HOST}/qt/{pid}')
    except Exception: pass


#                                id  name level  x    y   gold
def tracePlayers() -> List[Tuple[int, str, int, int, int, int]] | None:
    if solo: return None
    try: rsp: rq.Response = rq.get(f'{_HOST}/trc/{sid}/{pid}')
    except Exception: return None

    if rsp.status_code != 200: return None

    jsn = json.loads(rsp.text)
    _list = []
    for i in jsn:
        _list.append((int(i[0]), i[1], int(i[2]), int(i[3]),
                      int(i[4]), int(i[5])))
    return _list


def updatePlayer(lvl: int, x: int, y: int, goldAmount: int):
    if solo: return
    try:
        rq.post(f'{_HOST}/upd/{pid}',
                json={'level': lvl, 'x': x, 'y': y, 'gold': goldAmount})
    except Exception: pass


#                                     x    y
def updateBoard(goldTakenFrom: Tuple[int, int]):
    if solo: return
    try: rq.post(f'{_HOST}/brd/{sid}/{level}',
                 json={'pid': pid, 'gtf_x': goldTakenFrom[0], 'gtf_y': goldTakenFrom[1]})
    except Exception: pass


#                              pid   x    y
def traceBoard() -> List[Tuple[int, int, int]] | None:
    if solo: return None
    try: rsp: rq.Response = rq.get(f'{_HOST}/trc_b/{sid}/{pid}/{level}')
    except Exception: return None

    if rsp.status_code != 200: return None

    jsn = json.loads(rsp.text)
    _list = []
    for i in jsn:
        _list.append((int(i[0]), int(i[1]), int(i[2])))
    return _list


def getCurrentGoldAmountOnBoard() -> int | None:
    if solo: return None
    try: rsp: rq.Response = rq.get(f'{_HOST}/gld/{sid}/{level}')
    except Exception: return None

    if rsp.status_code != 200: return None
    return int(rsp.text)


#                                  name score
def getSavedPlayers() -> List[Tuple[str, int]] | None:
    try: rsp: rq.Response = rq.get(f'{_HOST}/db',
            json={'mode': 'select', 'pid': pid})
    except Exception: return None

    if rsp.status_code != 200: return None

    jsn = json.loads(rsp.text)
    _list = []
    [_list.append((i[0], int(i[1]))) for i in jsn]
    return _list


def saveCurrentPlayerResult():
    if solo: return
    try: rq.Response = rq.post(f'{_HOST}/db',
            json={'mode': 'insert', 'pid': pid})
    except Exception: pass


def notifyPlayerIsReady():
    global _isReady
    _isReady = True
    try: rq.post(f'{_HOST}/rd/{pid}')
    except Exception: pass
