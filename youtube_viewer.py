"""
MIT License

Copyright (c) 2021-2022 MShawon

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
import io
import json
import logging
import re
import textwrap
from concurrent.futures import ThreadPoolExecutor, wait
from time import gmtime, sleep, strftime, time

import psutil
from fake_headers import Headers, browsers
from requests.exceptions import RequestException
from tabulate import tabulate
from undetected_chromedriver.patcher import Patcher

from youtubeviewer import website
from youtubeviewer.basics import *
from youtubeviewer.config import create_config
from youtubeviewer.database import *
from youtubeviewer.download_driver import *
from youtubeviewer.load_files import *
from youtubeviewer.proxies import *

log = logging.getLogger('werkzeug')
log.disabled = True

SCRIPT_VERSION = '1.7.4'

print(bcolors.OKGREEN + """

Yb  dP  dP"Yb  88   88 888888 88   88 88""Yb 888888
 YbdP  dP   Yb 88   88   88   88   88 88__dP 88__
  8P   Yb   dP Y8   8P   88   Y8   8P 88""Yb 88""
 dP     YbodP  `YbodP'   88   `YbodP' 88oodP 888888

                        Yb    dP 88 888888 Yb        dP 888888 88""Yb
                         Yb  dP  88 88__    Yb  db  dP  88__   88__dP
                          YbdP   88 88""     YbdPYbdP   88""   88"Yb
                           YP    88 888888    YP  YP    888888 88  Yb
""" + bcolors.ENDC)

print(bcolors.OKCYAN + """
           [ GitHub : https://github.com/MShawon/YouTube-Viewer ]
""" + bcolors.ENDC)

print(bcolors.WARNING + f"""
+{'-'*26} Version: {SCRIPT_VERSION} {'-'*26}+
""" + bcolors.ENDC)

proxy = 37.57.15.43:47233
92.45.19.44:1080
154.70.151.73:5678
203.150.136.34:3629
93.171.224.50:4153
160.202.41.194:4153
183.6.57.161:5678
72.195.34.58:4145
200.192.236.242:1080
37.25.127.85:1080
217.169.88.79:4153
191.183.77.33:5678
176.97.190.107:3629
144.76.99.207:16009
108.175.23.1:13135
46.36.70.104:1080
213.210.67.186:3629
181.12.80.2:12000
173.212.250.65:14411
36.66.36.251:4153
192.111.139.162:4145
213.6.188.214:3629
192.111.129.145:16894
191.37.181.103:4145
159.203.164.41:39767
103.149.105.253:4153
115.164.18.166:13629
98.162.25.4:31654
185.179.196.19:1085
159.69.153.169:5566
192.111.137.37:18762
159.192.97.129:5678
202.133.4.49:4153
178.48.68.61:4145
174.77.111.197:4145
182.253.192.186:46634
72.221.164.34:60671
213.136.82.183:37795
181.143.45.21:4153
46.107.230.122:1080
123.49.48.130:5678
103.210.28.154:31433
179.43.140.131:9050
192.111.130.5:17002
43.224.8.12:6667
187.19.127.180:4153
103.82.8.193:4153
196.41.98.34:60216
43.243.60.56:5678
103.88.221.194:46450
36.67.14.151:5678
179.108.51.90:63253
190.186.240.148:4145
41.170.12.92:49142
203.128.72.62:4145
203.192.199.238:5678
180.180.152.94:4145
103.66.177.17:32251
93.175.194.155:3629
5.172.188.92:5678
103.80.210.174:5678
157.230.111.195:15080
46.23.155.18:62638
201.33.161.238:4153
102.64.116.1:4145
125.26.4.197:4145
178.212.199.95:1099
103.145.130.150:4673
192.111.137.35:4145
46.188.82.63:4153
181.78.24.28:5678
185.170.233.112:47574
174.77.111.196:4145
186.232.178.237:5678
170.244.0.179:4145
184.178.172.5:15303
213.145.139.202:5678
123.200.19.218:5678
189.85.118.22:1080
70.166.167.55:57745
102.66.228.116:5678
154.86.14.53:1080
98.170.57.231:4145
69.163.163.164:24260
181.78.24.30:5678
98.178.72.21:10919
184.95.0.122:4153
94.181.33.149:40840
41.89.162.100:4673
72.221.172.203:4145
62.112.194.224:26057
139.255.194.114:5678
175.143.179.244:5678
46.227.37.169:1088
92.84.56.10:47054
187.32.189.28:5678
213.135.12.27:5678
178.212.48.23:1080
187.111.160.8:58315
36.89.135.207:5678
171.100.8.82:49181
202.40.178.34:5678
143.255.108.173:4153
92.45.19.35:5678
115.127.121.194:5678
192.111.139.165:4145
114.134.90.110:10800
85.92.164.179:4145
202.84.76.190:5678
180.92.212.178:5678
45.71.195.150:4145
43.239.75.22:4145
182.48.70.154:38440
103.210.28.194:31433
115.75.189.99:4153
185.138.230.68:5678
192.252.208.70:14282
192.111.139.163:19404
212.98.147.60:4153
185.99.33.171:5678
72.195.34.42:4145
60.2.44.182:34659
103.47.93.250:1080
138.118.213.213:4153
182.160.114.158:5678
184.178.172.14:4145
201.18.91.34:4153
103.110.59.3:35294
102.66.234.2:5678
170.238.119.77:1080
66.135.227.181:4145
46.146.202.237:4153
170.80.71.78:5678
204.10.182.34:39593
101.51.121.141:4153
110.34.166.187:4153
43.224.10.8:6667
98.162.25.23:4145
103.199.157.137:41610
149.20.253.104:12551
185.255.47.48:4145
67.213.212.11:28220
191.184.42.152:4153
216.215.125.178:48324
188.72.6.98:50321
50.197.210.138:32100
213.222.34.200:4145
201.90.171.253:4153
202.179.184.42:5430
72.206.181.97:64943
72.195.34.59:4145
58.57.147.86:10800
72.195.34.60:27391
98.188.47.150:4145
103.210.35.62:4145
103.159.194.145:5678
202.162.214.250:5434
177.235.99.234:4145
24.249.199.4:4145
216.127.113.58:5678
186.10.10.138:5678
103.115.255.85:51372
72.217.216.239:4145
174.77.111.198:49547
103.248.42.88:5678
121.139.218.165:43295
176.36.138.237:1080
60.241.231.114:4153
192.111.135.18:18301
178.253.208.146:1080
221.224.213.156:1080
124.67.67.17:5678
174.75.211.222:4145
82.103.70.227:4145
93.113.101.85:5678
123.234.46.51:4153
190.110.183.22:4153
72.206.181.105:64935
47.180.63.37:54321
31.14.185.222:4153
190.109.2.90:4145
50.250.205.21:32100
78.46.225.37:19051
84.52.123.163:4145
54.36.108.221:40305
116.232.149.202:4145
105.234.156.237:5678
179.51.162.8:9898
184.178.172.13:15311
174.64.199.79:4145
195.5.55.10:4153
124.107.46.206:5678
164.92.205.28:9050
78.88.224.67:4145
185.206.80.227:10801
91.150.189.122:60647
212.50.60.231:5678
190.144.167.178:5678
197.251.236.226:5678
70.60.132.130:5678
181.129.70.82:44357
103.133.37.77:4153
23.94.73.246:1080
72.195.34.41:4145
186.224.225.30:42648
177.93.76.26:4153
81.91.157.134:5678
36.95.74.29:5678
104.139.74.25:34368
181.143.1.186:4673
184.178.172.28:15294
181.129.28.18:5678
103.79.96.141:4153
49.248.32.110:41363
182.52.19.136:3629
151.80.252.69:5580
182.48.65.195:5678
46.101.5.73:48528
188.136.162.30:4153
58.147.170.117:10801
36.89.246.187:4145
177.86.64.1:3629
24.249.199.12:4145
193.34.93.221:33861
103.8.115.27:48644
190.217.58.90:5678
37.238.130.85:58540
185.47.184.253:45463
180.87.170.21:1080
213.32.253.117:52396
165.227.104.122:58216
202.8.73.206:5678
187.37.121.236:4153
113.11.138.22:5678
184.181.217.210:4145
85.198.244.100:3629
103.59.203.197:4145
193.193.240.34:48785
83.220.234.102:5678
98.162.25.7:31653
94.253.95.241:3629
176.123.218.6:18080
72.221.232.155:4145
151.80.252.69:21034
81.219.155.193:65000
36.67.45.71:1086
200.231.188.18:4153
120.50.13.41:40308
119.93.122.233:4145
103.163.36.142:4145
27.116.51.186:6667
221.181.174.15:4153
103.51.45.9:4145
71.71.162.234:39593
98.175.31.195:4145
77.43.59.66:1080
183.91.81.250:5678
200.0.247.84:4153
93.91.118.141:3629
195.120.78.30:5678
58.8.139.129:4153
187.33.160.183:4153
103.240.33.161:8291
185.208.188.193:50318
109.92.133.194:5678
98.162.96.53:10663
78.31.93.76:1080
188.134.9.40:1080
50.47.75.212:5678
37.98.231.12:1080
45.7.177.220:39867
5.135.191.18:9100
202.153.91.165:1080
202.51.103.154:5678
91.203.165.23:5678
78.152.119.50:1088
174.64.199.82:4145
202.159.35.189:443
178.250.70.218:1088
14.207.207.112:3629
202.180.23.42:4153
45.7.177.219:39867
125.27.251.173:33008
193.163.116.29:1080
222.127.137.149:5678
103.205.128.7:4145
102.38.50.65:4153
80.78.130.106:3000
192.252.215.5:16137
162.243.115.237:45267
203.76.115.246:4145
103.172.17.7:5678
184.178.172.18:15280
115.75.163.225:5678
198.8.94.174:39078
184.178.172.25:15291
119.252.167.130:5678
95.43.42.100:4145
203.76.110.186:4145
103.24.177.59:4145
186.86.137.96:5678
58.246.245.122:4153
178.254.157.214:1080
98.162.96.52:4145
46.98.247.92:1080
72.206.181.123:4145
77.85.168.253:4145
43.225.163.209:4153
149.20.253.102:12551
181.209.103.98:5678
87.197.136.58:4153
103.150.115.186:4153
103.70.206.9:59311
192.252.208.67:14287
123.200.2.122:5678
103.94.133.91:4153
202.131.233.187:5678
79.0.251.45:4153
94.72.158.129:4153
103.197.206.9:5678
194.28.56.49:3629
192.252.220.92:17328
72.195.114.169:4145
213.21.56.20:4153
36.89.60.101:5678
124.106.234.215:5678
200.0.247.85:4153
36.90.49.168:51327
186.183.158.186:5678
193.105.62.11:58973
192.111.130.2:4145
93.171.224.48:4153
161.49.158.165:5678
116.68.196.209:1080
176.120.32.135:5678
41.223.234.116:37259
202.43.191.14:5430
216.215.125.182:48324
186.208.19.61:5678
213.145.137.102:37447
103.105.86.62:5678
103.96.40.172:5678
221.181.174.14:4153
195.158.8.67:1090
98.188.47.132:4145
72.221.196.157:35904
103.145.45.149:51372
202.62.42.218:5678
112.78.170.251:5678
98.162.96.41:4145
180.92.212.200:5678
151.80.252.69:50356
178.212.48.51:5678
93.171.224.41:4153
27.123.1.36:4153
210.245.51.20:4145
81.17.94.50:47163
189.51.144.28:5678
102.38.50.62:4153
179.191.18.59:5678
77.108.78.20:48079
2.137.228.110:4153
72.195.34.35:27360
118.179.87.170:5678
192.111.137.34:18765
72.195.114.184:4145
179.191.12.97:4153
89.237.36.193:51549
24.75.156.114:3366
109.110.82.245:5678
95.161.188.246:61537
177.10.84.121:4145
66.135.227.178:4145
67.73.141.150:5678
181.204.12.122:5678
123.203.156.224:65528
177.87.42.156:4145
110.77.145.159:4145
159.192.121.240:4145
72.210.252.134:46164
152.32.164.22:21616
192.111.135.17:18302
192.252.211.197:14921
103.146.170.244:5678
41.60.235.189:5678
117.2.155.245:4153
193.59.26.11:4153
177.93.72.98:4153
185.97.121.197:4153
138.219.201.242:5678
185.12.68.163:51626
186.208.68.26:4153
185.32.4.98:4153
124.158.168.22:5678
202.55.175.237:1080
103.106.112.13:5430
81.24.82.69:40980
89.132.207.82:4145
103.26.213.228:4153
80.28.111.248:4145
185.106.44.37:4153
103.77.10.98:5678
170.84.50.225:4153
103.58.16.57:4145
192.139.192.29:4153
185.196.176.77:4145
213.172.89.227:4153
66.42.224.229:41679
195.149.98.30:56897
72.210.208.101:4145
177.23.184.166:4145
192.252.209.155:14455
70.166.167.38:57728
213.16.81.182:35559
202.129.52.174:4153
170.81.141.254:61437
43.246.143.250:9999
185.17.134.185:31388
91.218.140.96:3629
186.5.205.1:54321
185.240.80.2:4153
94.240.24.91:5678
50.192.49.5:32100
103.30.84.50:1080
203.170.75.14:4153
116.199.168.1:4145
45.14.36.146:5678
119.93.53.35:5678
98.162.25.29:31679
200.91.160.111:4673
197.159.0.214:48506
45.156.184.104:25906
43.229.254.163:1080
89.216.52.217:4153
e
status = None
start_time = None
cancel_all = False

urls = [https://www.youtube.com/watch?v=aG572IKwl20&t=4s]
queries = []
suggested = []

hash_urls = None
hash_queries = None
hash_config = None

driver_dict = {}
duration_dict = {}
checked = {}
video_statistics = {}
view = []
bad_proxies = []
used_proxies = []
temp_folders = []
console = []

threads = 0
views = 75000

cwd = os.getcwd()
patched_drivers = os.path.join(cwd, 'patched_drivers')
config_path = os.path.join(cwd, 'config.json')
driver_identifier = os.path.join(cwd, 'patched_drivers', 'chromedriver')

DATABASE = os.path.join(cwd, 'database.db')
DATABASE_BACKUP = os.path.join(cwd, 'database_backup.db')

headers = ['Index', 'Video Title', 'Views']

width = 0
viewports = ['2560,1440', '1920,1080', '1440,900',
             '1536,864', '1366,768', '1280,1024', '1024,768']

referers = ['https://search.yahoo.com/', 'https://duckduckgo.com/', 'https://www.google.com/',
            'https://www.bing.com/', 'https://t.co/', '']

referers = choices(referers, k=len(referers)*3)

website.console = console
website.database = DATABASE


def monkey_patch_exe(self):
    linect = 0
    replacement = self.gen_random_cdc()
    replacement = f"  var key = '${replacement.decode()}_';\n".encode()
    with io.open(self.executable_path, "r+b") as fh:
        for line in iter(lambda: fh.readline(), b""):
            if b"var key = " in line:
                fh.seek(-len(line), 1)
                fh.write(replacement)
                linect += 1
        return linect


Patcher.patch_exe = monkey_patch_exe


def timestamp():
    global date_fmt
    date_fmt = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    return bcolors.OKGREEN + f'[{date_fmt}] | ' + bcolors.OKCYAN + f'{cpu_usage} | '


def clean_exe_temp(folder):
    temp_name = None
    if hasattr(sys, '_MEIPASS'):
        temp_name = sys._MEIPASS.split('\\')[-1]
    else:
        if sys.version_info.minor < 7 or sys.version_info.minor > 9:
            print(
                f'Your current python version is not compatible : {sys.version}')
            print(f'Install Python version between 3.7.x to 3.9.x to run this script')
            input("")
            sys.exit()

    for f in glob(os.path.join('temp', folder, '*')):
        if temp_name not in f:
            shutil.rmtree(f, ignore_errors=True)


def update_chrome_version():
    link = 'https://gist.githubusercontent.com/MShawon/29e185038f22e6ac5eac822a1e422e9d/raw/versions.txt'

    output = requests.get(link, timeout=60).text
    chrome_versions = output.split('\n')

    browsers.chrome_ver = chrome_versions


def check_update():
    api_url = 'https://api.github.com/repos/MShawon/YouTube-Viewer/releases/latest'
    response = requests.get(api_url, timeout=30)

    RELEASE_VERSION = response.json()['tag_name']

    if RELEASE_VERSION > SCRIPT_VERSION:
        print(bcolors.OKCYAN + '#'*100 + bcolors.ENDC)
        print(bcolors.OKCYAN + 'Update Available!!! ' +
              f'YouTube Viewer version {SCRIPT_VERSION} needs to update to {RELEASE_VERSION} version.' + bcolors.ENDC)

        try:
            notes = response.json()['body'].split('SHA256')[0].split('\r\n')
            for note in notes:
                if note:
                    print(bcolors.HEADER + note + bcolors.ENDC)
        except Exception:
            pass
        print(bcolors.OKCYAN + '#'*100 + '\n' + bcolors.ENDC)


def create_html(text_dict):
    if len(console) > 250:
        console.pop()

    date = f'<span style="color:#23d18b"> [{date_fmt}] | </span>'
    cpu = f'<span style="color:#29b2d3"> {cpu_usage} | </span>'
    str_fmt = ''.join(
        [f'<span style="color:{key}"> {value} </span>' for key, value in text_dict.items()])
    html = date + cpu + str_fmt

    console.insert(0, html)


def detect_file_change():
    global hash_urls, hash_queries, urls, queries

    if hash_urls != get_hash("urls.txt"):
        hash_urls = get_hash("urls.txt")
        urls = load_url()
        suggested.clear()

    if hash_queries != get_hash("search.txt"):
        hash_queries = get_hash("search.txt")
        queries = load_search()
        suggested.clear()


def direct_or_search(position):
    keyword = None
    video_title = None
    if position % 2:
        try:
            method = 1
            url = choice(urls)
            if 'music.youtube.com' in url:
                youtube = 'Music'
            else:
                youtube = 'Video'
        except IndexError:
            raise Exception("Your urls.txt is empty!")

    else:
        try:
            method = 2
            query = choice(queries)
            keyword = query[0]
            video_title = query[1]
            url = "https://www.youtube.com"
            youtube = 'Video'
        except IndexError:
            try:
                youtube = 'Music'
                url = choice(urls)
                if 'music.youtube.com' not in url:
                    raise Exception
            except Exception:
                raise Exception("Your search.txt is empty!")

    return url, method, youtube, keyword, video_title


def features(driver):
    if bandwidth:
        save_bandwidth(driver)

    bypass_popup(driver)

    bypass_other_popup(driver)

    play_video(driver)

    change_playback_speed(driver, playback_speed)


def update_view_count(position):
    view.append(position)
    view_count = len(view)
    print(timestamp() + bcolors.OKCYAN +
          f'Worker {position} | View added : {view_count}' + bcolors.ENDC)

    create_html({"#29b2d3": f'Worker {position} | View added : {view_count}'})

    if database:
        try:
            update_database(
                database=DATABASE, threads=max_threads)
        except Exception:
            pass


def set_referer(position, url, method, driver):
    referer = choice(referers)
    if referer:
        if method == 2 and 't.co/' in referer:
            driver.get(url)
        else:
            if 'search.yahoo.com' in referer:
                driver.get('https://duckduckgo.com/')
                driver.execute_script(
                    "window.history.pushState('page2', 'Title', arguments[0]);", referer)
            else:
                driver.get(referer)

            driver.execute_script(
                "window.location.href = '{}';".format(url))

        print(timestamp() + bcolors.OKBLUE +
              f"Worker {position} | Referer used : {referer}" + bcolors.ENDC)

        create_html(
            {"#3b8eea": f"Worker {position} | Referer used : {referer}"})

    else:
        driver.get(url)


def youtube_normal(method, keyword, video_title, driver, output):
    if method == 2:
        msg = search_video(driver, keyword, video_title)
        if msg == 'failed':
            raise Exception(
                f"Can't find this [{video_title}] video with this keyword [{keyword}]")

    skip_initial_ad(driver, output, duration_dict)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.ID, 'movie_player')))
    except WebDriverException:
        raise Exception(
            "Slow internet speed or Stuck at recaptcha! Can't load YouTube...")

    features(driver)

    view_stat = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#count span'))).text

    return view_stat


def youtube_music(driver):
    if 'coming-soon' in driver.current_url:
        raise Exception(
            "YouTube Music is not available in your area!")
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="player-page"]')))
    except WebDriverException:
        raise Exception(
            "Slow internet speed or Stuck at recaptcha! Can't load YouTube...")

    bypass_popup(driver)

    play_music(driver)

    view_stat = 'music'
    return view_stat


def spoof_geolocation(proxy_type, proxy, driver):
    try:
        proxy_dict = {
            "http": f"{proxy_type}://{proxy}",
                    "https": f"{proxy_type}://{proxy}",
        }
        resp = requests.get(
            "http://ip-api.com/json", proxies=proxy_dict, timeout=30)

        if resp.status_code == 200:
            location = resp.json()
            params = {
                "latitude": location['lat'],
                "longitude": location['lon'],
                "accuracy": randint(20, 100)
            }
            driver.execute_cdp_cmd(
                "Emulation.setGeolocationOverride", params)

    except (RequestException, WebDriverException):
        pass


def control_player(driver, output, position, proxy, youtube, collect_id=True):
    current_url = driver.current_url

    video_len = duration_dict.get(output, 0)
    for _ in range(90):
        if video_len != 0:
            duration_dict[output] = video_len
            break

        video_len = driver.execute_script(
            "return document.getElementById('movie_player').getDuration()")
        sleep(1)

    if video_len == 0:
        raise Exception('Video player is not loading...')

    video_len = video_len*uniform(minimum, maximum)

    duration = strftime("%Hh:%Mm:%Ss", gmtime(video_len))
    print(timestamp() + bcolors.OKBLUE + f"Worker {position} | " + bcolors.OKGREEN +
          f"{proxy} --> {youtube} Found : {output} | Watch Duration : {duration} " + bcolors.ENDC)

    create_html({"#3b8eea": f"Worker {position} | ",
                 "#23d18b": f"{proxy.split('@')[-1]} --> {youtube} Found : {output} | Watch Duration : {duration} "})

    if youtube == 'Video' and collect_id:
        try:
            video_id = re.search(
                r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", current_url).group(1)
            if video_id not in suggested and output in driver.title:
                suggested.append(video_id)
        except Exception:
            pass

    current_channel = driver.find_element(
        By.CSS_SELECTOR, '#upload-info a').text

    error = 0
    loop = int(video_len/4)
    for _ in range(loop):
        sleep(5)
        current_time = driver.execute_script(
            "return document.getElementById('movie_player').getCurrentTime()")

        if youtube == 'Video':
            play_video(driver)
            random_command(driver)
        elif youtube == 'Music':
            play_music(driver)

        current_state = driver.execute_script(
            "return document.getElementById('movie_player').getPlayerState()")
        if current_state in [-1, 3]:
            error += 1
        else:
            error = 0

        if error == 10:
            error_msg = f'Taking too long to play the video | Reason : buffering'
            if current_state == -1:
                error_msg = f"Failed to play the video | Possible Reason : {proxy.split('@')[-1]} not working anymore"
            raise Exception(error_msg)

        elif current_time > video_len or driver.current_url != current_url:
            break

    output = textwrap.fill(text=output, width=75, break_on_hyphens=False)
    video_statistics[output] = video_statistics.get(output, 0) + 1
    website.html_table = tabulate(video_statistics.items(), headers=headers,
                                  showindex=True, numalign='center', stralign='center', tablefmt="html")
    return current_url, current_channel


def youtube_live(proxy, position, driver, output):
    error = 0
    while True:
        view_stat = driver.find_element(
            By.CSS_SELECTOR, '#count span').text
        if 'watching' in view_stat:
            print(timestamp() + bcolors.OKBLUE + f"Worker {position} | " + bcolors.OKGREEN +
                  f"{proxy} | {output} | " + bcolors.OKCYAN + f"{view_stat} " + bcolors.ENDC)

            create_html({"#3b8eea": f"Worker {position} | ",
                         "#23d18b": f"{proxy.split('@')[-1]} | {output} | ", "#29b2d3": f"{view_stat} "})
        else:
            error += 1

        play_video(driver)

        random_command(driver)

        if error == 5:
            break
        sleep(60)

    update_view_count(position)


def music_and_video(proxy, position, youtube, driver, output, view_stat):
    rand_choice = 1
    if len(suggested) > 1 and view_stat != 'music':
        rand_choice = randint(1, 3)

    for i in range(rand_choice):
        if i == 0:
            current_url, current_channel = control_player(
                driver, output, position, proxy, youtube, collect_id=True)

            update_view_count(position)

        else:
            print(timestamp() + bcolors.OKBLUE +
                  f"Worker {position} | Suggested video loop : {i}" + bcolors.ENDC)

            create_html(
                {"#3b8eea": f"Worker {position} | Suggested video loop : {i}"})

            try:
                output = play_next_video(driver, suggested)
            except WebDriverException as e:
                raise Exception(
                    f'Error suggested | {type(e).__name__} | {e.args[0]}')

            print(timestamp() + bcolors.OKBLUE +
                  f"Worker {position} | Found next suggested video : [{output}]" + bcolors.ENDC)

            create_html(
                {"#3b8eea": f"Worker {position} | Found next suggested video : [{output}]"})

            skip_initial_ad(driver, output, duration_dict)

            features(driver)

            current_url, current_channel = control_player(
                driver, output, position, proxy, youtube, collect_id=False)

            update_view_count(position)

    return current_url, current_channel


def channel_or_endscreen(proxy, position, youtube, driver, view_stat, current_url, current_channel):
    option = 1
    if view_stat != 'music' and driver.current_url == current_url:
        option = choices([1, 2, 3], cum_weights=(0.5, 0.75, 1.00), k=1)[0]

        if option == 2:
            try:
                output, log, option = play_from_channel(
                    driver, current_channel)
            except WebDriverException as e:
                raise Exception(
                    f'Error channel | {type(e).__name__} | {e.args[0]}')

            print(timestamp() + bcolors.OKBLUE +
                  f"Worker {position} | {log}" + bcolors.ENDC)

            create_html({"#3b8eea": f"Worker {position} | {log}"})

        elif option == 3:
            try:
                output = play_end_screen_video(driver)
            except WebDriverException as e:
                raise Exception(
                    f'Error end screen | {type(e).__name__} | {e.args[0]}')

            print(timestamp() + bcolors.OKBLUE +
                  f"Worker {position} | Video played from end screen : [{output}]" + bcolors.ENDC)

            create_html(
                {"#3b8eea": f"Worker {position} | Video played from end screen : [{output}]"})

        if option in [2, 3]:
            skip_initial_ad(driver, output, duration_dict)

            features(driver)

            current_url, current_channel = control_player(
                driver, output, position, proxy, youtube, collect_id=False)

        if option in [2, 3, 4]:
            update_view_count(position)


def windows_kill_drivers():
    for process in constructor.Win32_Process(["CommandLine", "ProcessId"]):
        try:
            if 'UserAgentClientHint' in process.CommandLine:
                # print(f'Killing PID : {process.ProcessId}')
                subprocess.Popen(['taskkill', '/F', '/PID', f'{process.ProcessId}'],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        except Exception:
            pass


def quit_driver(driver, data_dir):
    if driver and driver in driver_dict:
        driver.quit()
        if data_dir in temp_folders:
            temp_folders.remove(data_dir)

    proxy_folder = driver_dict.pop(driver, None)
    if proxy_folder:
        shutil.rmtree(proxy_folder, ignore_errors=True)

    status = 400
    return status


def main_viewer(proxy_type, proxy, position):
    global width, viewports
    driver = None
    data_dir = None

    if cancel_all:
        raise KeyboardInterrupt

    try:
        detect_file_change()

        checked[position] = None

        header = Headers(
            browser="chrome",
            os=osname,
            headers=False
        ).generate()
        agent = header['User-Agent']

        url, method, youtube, keyword, video_title = direct_or_search(position)

        if category == 'r' and proxy_api:
            for _ in range(20):
                proxy = choice(proxies_from_api)
                if proxy not in used_proxies:
                    break
            used_proxies.append(proxy)

        status = check_proxy(category, agent, proxy, proxy_type)

        if status != 200:
            raise RequestException(status)

        try:
            print(timestamp() + bcolors.OKBLUE + f"Worker {position} | " + bcolors.OKGREEN +
                  f"{proxy} | {proxy_type.upper()} | Good Proxy | Opening a new driver..." + bcolors.ENDC)

            create_html({"#3b8eea": f"Worker {position} | ",
                        "#23d18b": f"{proxy.split('@')[-1]} | {proxy_type.upper()} | Good Proxy | Opening a new driver..."})

            while proxy in bad_proxies:
                bad_proxies.remove(proxy)
                sleep(1)

            patched_driver = os.path.join(
                patched_drivers, f'chromedriver_{position%threads}{exe_name}')

            try:
                Patcher(executable_path=patched_driver).patch_exe()
            except Exception:
                pass

            proxy_folder = os.path.join(
                cwd, 'extension', f'proxy_auth_{position}')

            factor = int(threads/(0.1*threads + 1))
            sleep_time = int((str(position)[-1])) * factor
            sleep(sleep_time)
            if cancel_all:
                raise KeyboardInterrupt

            driver = get_driver(background, viewports, agent, auth_required,
                                patched_driver, proxy, proxy_type, proxy_folder)

            driver_dict[driver] = proxy_folder

            data_dir = driver.capabilities['chrome']['userDataDir']
            temp_folders.append(data_dir)

            sleep(2)

            spoof_geolocation(proxy_type, proxy, driver)

            if width == 0:
                width = driver.execute_script('return screen.width')
                height = driver.execute_script('return screen.height')
                print(f'Display resolution : {width}x{height}')
                viewports = [i for i in viewports if int(i[:4]) <= width]

            set_referer(position, url, method, driver)

            if 'consent' in driver.current_url:
                print(timestamp() + bcolors.OKBLUE +
                      f"Worker {position} | Bypassing consent..." + bcolors.ENDC)

                create_html(
                    {"#3b8eea": f"Worker {position} | Bypassing consent..."})

                bypass_consent(driver)

            if video_title:
                output = video_title
            else:
                output = driver.title[:-10]

            if youtube == 'Video':
                view_stat = youtube_normal(
                    method, keyword, video_title, driver, output)
            else:
                view_stat = youtube_music(driver)

            if 'watching' in view_stat:
                youtube_live(proxy, position, driver, output)

            else:
                current_url, current_channel = music_and_video(
                    proxy, position, youtube, driver, output, view_stat)

            channel_or_endscreen(proxy, position, youtube,
                                 driver, view_stat, current_url, current_channel)

            if randint(1, 2) == 1:
                try:
                    driver.find_element(By.ID, 'movie_player').send_keys('k')
                except WebDriverException:
                    pass

            status = quit_driver(driver=driver, data_dir=data_dir)

        except Exception as e:
            print(timestamp() + bcolors.FAIL +
                  f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0]}" + bcolors.ENDC)

            create_html(
                {"#f14c4c": f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0]}"})

            status = quit_driver(driver=driver, data_dir=data_dir)

    except RequestException:
        print(timestamp() + bcolors.OKBLUE + f"Worker {position} | " +
              bcolors.FAIL + f"{proxy} | {proxy_type.upper()} | Bad proxy " + bcolors.ENDC)

        create_html({"#3b8eea": f"Worker {position} | ",
                     "#f14c4c": f"{proxy.split('@')[-1]} | {proxy_type.upper()} | Bad proxy "})

        checked[position] = proxy_type
        bad_proxies.append(proxy)

    except Exception as e:
        print(timestamp() + bcolors.FAIL +
              f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0]}" + bcolors.ENDC)

        create_html(
            {"#f14c4c": f"Worker {position} | Line : {e.__traceback__.tb_lineno} | {type(e).__name__} | {e.args[0]}"})


def get_proxy_list():
    if filename:
        if category == 'r':
            factor = max_threads if max_threads > 1000 else 1000
            proxy_list = [filename] * factor
        else:
            if proxy_api:
                proxy_list = scrape_api(filename)
            else:
                proxy_list = load_proxy(filename)

    else:
        proxy_list = gather_proxy()

    return proxy_list


def stop_server(immediate=False):
    if not immediate:
        print('Allowing a maximum of 15 minutes to finish all the running drivers...')
        for _ in range(180):
            sleep(5)
            if 'state=running' not in str(futures[1:-1]):
                break

    if api:
        for _ in range(10):
            response = requests.post(f'http://127.0.0.1:{port}/shutdown')
            if response.status_code == 200:
                print('Server shut down successfully!')
                break
            else:
                print(f'Server shut down error : {response.status_code}')
                sleep(3)


def clean_exit():
    print(timestamp() + bcolors.WARNING +
          'Cleaning up processes...' + bcolors.ENDC)
    create_html({"#f3f342": "Cleaning up processes..."})

    if osname == 'win':
        driver_dict.clear()
        windows_kill_drivers()
    else:
        for driver in list(driver_dict):
            quit_driver(driver=driver, data_dir=None)

    for folder in temp_folders:
        shutil.rmtree(folder, ignore_errors=True)


def cancel_pending_task(not_done):
    global cancel_all

    cancel_all = True
    for future in not_done:
        _ = future.cancel()

    clean_exit()

    stop_server(immediate=True)
    _ = wait(not_done, timeout=None)

    clean_exit()


def view_video(position):
    if position == 0:
        if api:
            website.start_server(host=host, port=port)

    elif position == total_proxies - 1:
        stop_server(immediate=False)
        clean_exit()

    else:
        sleep(2)
        proxy = proxy_list[position]

        if proxy_type:
            main_viewer(proxy_type, proxy, position)
        elif '|' in proxy:
            splitted = proxy.split('|')
            main_viewer(splitted[-1], splitted[0], position)
        else:
            main_viewer('http', proxy, position)
            if checked[position] == 'http':
                main_viewer('socks4', proxy, position)
            if checked[position] == 'socks4':
                main_viewer('socks5', proxy, position)


def main():
    global cancel_all, proxy_list, total_proxies, proxies_from_api, threads, hash_config, futures, cpu_usage

    cancel_all = False
    start_time = time()
    hash_config = get_hash(config_path)

    proxy_list = get_proxy_list()
    if category != 'r':
        print(bcolors.OKCYAN +
              f'Total proxies : {len(proxy_list)}' + bcolors.ENDC)

    proxy_list = [x for x in proxy_list if x not in bad_proxies]
    if len(proxy_list) == 0:
        bad_proxies.clear()
        proxy_list = get_proxy_list()
    if proxy_list[0] != 'dummy':
        proxy_list.insert(0, 'dummy')
    if proxy_list[-1] != 'dummy':
        proxy_list.append('dummy')
    total_proxies = len(proxy_list)

    if category == 'r' and proxy_api:
        proxies_from_api = scrape_api(link=filename)

    threads = randint(min_threads, max_threads)
    if api:
        threads += 1

    loop = 0
    pool_number = list(range(total_proxies))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(view_video, position)
                   for position in pool_number]

        done, not_done = wait(futures, timeout=0)
        try:
            while not_done:
                freshly_done, not_done = wait(not_done, timeout=1)
                done |= freshly_done

                loop += 1
                for _ in range(70):
                    cpu = str(psutil.cpu_percent(0.2))
                    cpu_usage = cpu + '%' + ' ' * \
                        (5-len(cpu)) if cpu != '0.0' else cpu_usage

                if loop % 40 == 0:
                    print(tabulate(video_statistics.items(),
                          headers=headers, showindex=True, tablefmt="pretty"))

                if category == 'r' and proxy_api:
                    proxies_from_api = scrape_api(link=filename)

                if len(view) >= views:
                    print(timestamp() + bcolors.WARNING +
                          f'Amount of views added : {views} | Stopping program...' + bcolors.ENDC)
                    create_html(
                        {"#f3f342": f'Amount of views added : {views} | Stopping program...'})

                    cancel_pending_task(not_done=not_done)
                    break

                elif hash_config != get_hash(config_path):
                    hash_config = get_hash(config_path)
                    print(timestamp() + bcolors.WARNING +
                          'Modified config.json will be in effect soon...' + bcolors.ENDC)
                    create_html(
                        {"#f3f342": 'Modified config.json will be in effect soon...'})

                    cancel_pending_task(not_done=not_done)
                    break

                elif refresh != 0 and category != 'r':

                    if (time() - start_time) > refresh*60:
                        start_time = time()

                        proxy_list_new = get_proxy_list()
                        proxy_list_new = [
                            x for x in proxy_list_new if x not in bad_proxies]

                        proxy_list_old = [
                            x for x in proxy_list[1:-1] if x not in bad_proxies]

                        if sorted(proxy_list_new) != sorted(proxy_list_old):
                            print(timestamp() + bcolors.WARNING +
                                  f'Refresh {refresh} minute triggered. Proxies will be reloaded soon...' + bcolors.ENDC)
                            create_html(
                                {"#f3f342": f'Refresh {refresh} minute triggered. Proxies will be reloaded soon...'})

                            cancel_pending_task(not_done=not_done)
                            break

        except KeyboardInterrupt:
            print(timestamp() + bcolors.WARNING +
                  'Hold on!!! Allow me a moment to close all the running drivers.' + bcolors.ENDC)
            create_html(
                {"#f3f342": 'Hold on!!! Allow me a moment to close all the running drivers.'})

            cancel_pending_task(not_done=not_done)
            raise KeyboardInterrupt


if __name__ == '__main__':

    clean_exe_temp(folder='youtube_viewer')
    date_fmt = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    cpu_usage = str(psutil.cpu_percent(1))
    update_chrome_version()
    check_update()
    osname, exe_name = download_driver(patched_drivers=patched_drivers)
    create_database(database=DATABASE, database_backup=DATABASE_BACKUP)

    if osname == 'win':
        import wmi
        constructor = wmi.WMI()

    urls = load_url()
    queries = load_search()

    if os.path.isfile(config_path):
        with open(config_path, 'r', encoding='utf-8-sig') as openfile:
            config = json.load(openfile)

        if len(config) == 11:
            print(json.dumps(config, indent=4))
            previous = str(input(
                bcolors.OKBLUE + 'Config file exists! Do you want to continue with previous saved preferences ? [Yes/No] : ' + bcolors.ENDC)).lower()
            if previous == 'n' or previous == 'no':
                create_config(config_path=config_path)
        else:
            print(bcolors.FAIL + 'Previous config file is not compatible with the latest script! Create a new one...' + bcolors.ENDC)
            create_config(config_path=config_path)
    else:
        create_config(config_path=config_path)

    hash_urls = get_hash("urls.txt")
    hash_queries = get_hash("search.txt")
    hash_config = get_hash(config_path)

    while len(view) < views:
        try:
            with open(config_path, 'r', encoding='utf-8-sig') as openfile:
                config = json.load(openfile)

            if cancel_all:
                print(json.dumps(config, indent=4))
            api = config["http_api"]["enabled"]
            host = config["http_api"]["host"]
            port = config["http_api"]["port"]
            database = config["database"]
            views = config["views"]
            minimum = config["minimum"] / 100
            maximum = config["maximum"] / 100
            category = config["proxy"]["category"]
            proxy_type = config["proxy"]["proxy_type"]
            filename = config["proxy"]["filename"]
            auth_required = config["proxy"]["authentication"]
            proxy_api = config["proxy"]["proxy_api"]
            refresh = config["proxy"]["refresh"]
            background = config["background"]
            bandwidth = config["bandwidth"]
            playback_speed = config["playback_speed"]
            max_threads = config["max_threads"]
            min_threads = config["min_threads"]

            if minimum >= maximum:
                minimum = maximum - 5

            if min_threads >= max_threads:
                max_threads = min_threads

            if auth_required and background:
                print(bcolors.FAIL +
                      "Premium proxy needs extension to work. Chrome doesn't support extension in Headless mode." + bcolors.ENDC)
                input(bcolors.WARNING +
                      f"Either use proxy without username & password or disable headless mode " + bcolors.ENDC)
                sys.exit()

            copy_drivers(cwd=cwd, patched_drivers=patched_drivers,
                         exe=exe_name, total=max_threads)

            main()
        except KeyboardInterrupt:
            sys.exit()
