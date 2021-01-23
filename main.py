from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count,Timer
from time import sleep
from datetime import datetime
import requests
import json

from requests.sessions import session

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def ReadJson(self,filename,method):
        with open(filename,method) as f:
            return json.load(f)

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('[Data]/useragents.txt','r')
        return choice(useragents)

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
        proxies = {}
        if self.use_proxy == 1:
            if self.proxy_type == 1:
                proxies = {
                    "http":"http://{0}".format(choice(proxies_file)),
                    "https":"https://{0}".format(choice(proxies_file))
                }
            elif self.proxy_type == 2:
                proxies = {
                    "http":"socks4://{0}".format(choice(proxies_file)),
                    "https":"socks4://{0}".format(choice(proxies_file))
                }
            else:
                proxies = {
                    "http":"socks5://{0}".format(choice(proxies_file)),
                    "https":"socks5://{0}".format(choice(proxies_file))
                }
        else:
            proxies = {
                    "http":None,
                    "https":None
            }
        return proxies

    def CalculateCpm(self):
        self.cpm = self.maxcpm * 60
        self.maxcpm = 0
        Timer(1.0, self.CalculateCpm).start()

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'[One Man Builds HashDecrypt Tool] ^| HITS: {self.hits} ^| BADS: {self.bads} ^| CPM: {self.cpm} ^| WEBHOOK RETRIES: {self.webhook_retries} ^| RETRIES: {self.retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.SetTitle('[One Man Builds HashDecrypt Tool]')
        self.clear()
        self.title = Style.BRIGHT+Fore.GREEN+"""                                        
                                  ╔═════════════════════════════════════════════════╗    
                                           ╦ ╦╔═╗╔═╗╦ ╦  ╔╦╗╔═╗╔═╗╦═╗╦ ╦╔═╗╔╦╗
                                           ╠═╣╠═╣╚═╗╠═╣   ║║║╣ ║  ╠╦╝╚╦╝╠═╝ ║ 
                                           ╩ ╩╩ ╩╚═╝╩ ╩  ═╩╝╚═╝╚═╝╩╚═ ╩ ╩   ╩ 
                                  ╚═════════════════════════════════════════════════╝

                
        """
        print(self.title)
        self.hits = 0
        self.bads = 0
        self.retries = 0
        self.webhook_retries = 0
        self.cpm = 0
        self.maxcpm = 0
        self.lock = Lock()

        self.session = requests.Session()

        config = self.ReadJson('[Data]/configs.json','r')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads_num = config['threads']
        self.webhook_enable = config['webhook_enable']
        self.webhook_url = config['webhook_url']

        print('')

    def SendWebhook(self,title,message,icon_url,thumbnail_url,proxy,useragent):
        try:
            timestamp = str(datetime.utcnow())

            message_to_send = {"embeds": [{"title": title,"description": message,"color": 65362,"author": {"name": "AUTHOR'S DISCORD SERVER [CLICK HERE]","url": "https://discord.gg/9bHfzyCjPQ","icon_url": icon_url},"footer": {"text": "MADE BY ONEMANBUILDS","icon_url": icon_url},"thumbnail": {"url": thumbnail_url},"timestamp": timestamp}]}
            
            headers = {
                'User-Agent':useragent,
                'Pragma':'no-cache',
                'Accept':'*/*',
                'Content-Type':'application/json'
            }

            payload = json.dumps(message_to_send)

            response = self.session.post(self.webhook_url,data=payload,headers=headers,proxies=proxy)

            if response.text == "":
                pass
            elif "You are being rate limited." in response.text:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
            else:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
        except:
            self.webhook_retries += 1
            self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)

    def find_string_between(self,string,first,last):
        try:
            start = string.index( first ) + len( first )
            end = string.index( last, start )
            return string[start:end]
        except:
            pass

    def HashDecrypt(self,combo):
        try:
            useragent = self.GetRandomUserAgent()

            headers = {
                'User-Agent':useragent
            }

            user = combo.split(':')[0]
            hash = combo.split(':')[1]

            proxy = self.GetRandomProxy()
        
            response = self.session.get(f'https://hashtoolkit.com/decrypt-hash/?hash={hash}',headers=headers,proxies=proxy)

            self.maxcpm += 1

            result = self.find_string_between(response.text,'<h1 class="res-header">Hashes for: <code>','</code></h1>')

            if result != None and '<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="' not in result:
                self.hits += 1
                self.PrintText(Fore.WHITE,Fore.GREEN,'HIT',f'{user}:{result}')
                with open('[Data]/[Results]/hits.txt','a',encoding='utf8') as f:
                    f.write(f'{user}:{result}\n')
                if self.webhook_enable == 1:
                    self.SendWebhook('HashDecrypt Result',f'{user}:{result}','https://cdn.discordapp.com/attachments/776819723731206164/796935218166497352/onemanbuilds_new_logo_final.png','https://cdn1.iconfinder.com/data/icons/essenstial-ultimate-ui/64/hashtag-512.png',proxy,useragent)
            else:
                self.bads += 1
                self.PrintText(Fore.WHITE,Fore.RED,'BAD',f'{user}:{hash}')
                with open('[Data]/[Results]/bads.txt','a',encoding='utf8') as f:
                    f.write(f'{user}:{result}\n')
        except:
            self.retries += 1
            self.HashDecrypt(combo)

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        self.CalculateCpm()
        combos = self.ReadFile('[Data]/combos.txt','r')
        for combo in combos:
            Run = True
            while Run:
                if active_count()<=self.threads_num:
                    Thread(target=self.HashDecrypt,args=(combo,)).start()
                    Run = False

if __name__ == '__main__':
    main = Main()
    main.Start()