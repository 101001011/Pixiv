import requests
from requests.exceptions import RequestException
from urllib.parse import quote
import time, random
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog, simpledialog
from screeninfo import get_monitors
import os
import json
import re
import math

MONITER_INFO = get_monitors()[0]

USER_AGENTS = [
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
"MAC:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
"Windows:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36",
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
]

class Spider:
    
    def __init__ (self) -> None:
        self.key = None
        self.amount = None
        self.open_r18 = False
        with open(os.path.join("AppData", "config.json"), 'r', encoding="UTF-8") as file:
            data_config = json.load(file)
        self.save_path = data_config["save_path"]
        self.cookie = data_config["cookie"]
        self.proxy = data_config["proxy"]
        
    def get_json (self, page: int) -> dict:
        """给出关键词和页数, 返回该页的 json 代码"""
        r18_url = ["mode=safe&s_mode=s_tag", "mode=r18&s_mode=s_tag"]
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.pixiv.net/tags/" + quote(self.key) + "/artworks?" + r18_url[self.open_r18],
            "Cookie": self.cookie
        }
        url = "https://www.pixiv.net/ajax/search/artworks/" + self.key
        params = {
            "word": self.key,
            "order": "date_d",
            "mode": "r18" if self.open_r18 else "safe",
            "p": str(page),
            "csw": "0",
            "s_mode": "s_tag",
            "type": "all",
            "lang": "zh",
            "version": "9800ad982e9b6a814939dd77a70a81311bf5d3ce"
        }
        proxies = {
            "http": self.proxy,
            "https": self.proxy
        }
        try:
            response = requests.get(url=url, params=params, headers=headers, proxies=proxies)
            if not response.text:
                raise Exception()
            return response.json()
        except Exception:
            time.sleep(random.random())
            return self.get_json(page)

    def get_image_info (self, datas: dict) -> list[dict]:
        """从页面 json 文件中提取图片信息"""
        infos = []
        for data in datas["body"]["illustManga"]["data"]:
            match = re.search(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\+09:00", data["createDate"])
            date = [match.group(i) for i in range(1, 7)]
            infos.append({
                "id": data["id"],
                "amount": data["pageCount"],
                "date": '/'.join(date)
            })
        return infos

    def get_image_url (self, info: dict) -> list[str]:
        """根据图片信息获取高清图片 url"""
        urls = []
        for i in range(info["amount"]):
            urls.append("https://i.pximg.net/img-original/img/" + info["date"] + '/' + info["id"] + '_p' + str(i))
        return urls
    
    def save_image (self, url: str, path: str, pos = 0) -> None:
        """根据图片地址获取图片, 返回是否成功获取"""
        format = [".jpg", ".png"]
        headers = {
            "Referer": "https://www.pixiv.net/"
        }
        try:
            response = requests.get(url=url + format[pos], headers=headers, timeout=5)
            if not response:
                if pos + 1 < len(format):
                    self.save_image(url, path, pos + 1)
                return
        except RequestException:
            time.sleep(random.random())
            self.save_image(url, path, pos)
        else:
            with open(path + format[pos], 'wb') as file:
                file.write(response.content)

    def run (self):
        urls, page_id = [], 0
        while True:
            page_id += 1
            data_json = self.get_json(page_id)
            infos = self.get_image_info(data_json)
            for info in infos:
                urls.extend(self.get_image_url(info))
            if len(urls) >= math.ceil(1.2 * self.amount): break
        for i in range(self.amount):
            url = urls[i]
            folder_path = os.path.join(self.save_path, self.key)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            os.startfile(folder_path)
            idx = re.search(r'\d+_p\d+', url).group()
            idx = re.sub(r'[^\d_]', '', idx)
            if not self.save_image(url=url, path=os.path.join(self.save_path, self.key) + '/' + idx): i -= 1

class Window (ttk.Window):

    epsWidth = MONITER_INFO.width // 100  # 显示器宽度的 1/100
    epsHeight = MONITER_INFO.height // 100  # 显示器高度的 1/100

    def __init__ (self):
        with open(os.path.join("AppData", "config.json"), 'r', encoding="UTF-8") as file:
            data_config = json.load(file)
        self.size_width = int(data_config["size_width"])
        self.size_height = int(data_config["size_height"])
        super().__init__(
            title = "Pixiv Spider",  # 窗口标题
            themename = "litera",  # 窗口主题样式
            size = (self.size_width * Window.epsWidth, self.size_height * Window.epsHeight),  # 窗口大小
            resizable = (False, False),  # 不允许拉伸窗口
            iconphoto = os.path.join("image", "CCA.png"),  # 窗口图标路径(.ico)
        )
        self.spider = Spider()
        # 计算窗口左上角的位置
        px = (MONITER_INFO.width - self.size_width * Window.epsWidth) // 2
        py = (MONITER_INFO.height - self.size_height * Window.epsHeight) // 2
        # 设置窗口的位置
        self.geometry(f'+{px}+{py}')
        # 确保窗口已经被完全初始化
        self.update_idletasks()
        
        # 关键词输入框设置
        key_setter_px = self.size_width // 6 * Window.epsWidth
        key_setter_py = self.size_height // 4 * Window.epsHeight
        key_setter_width = self.size_width * 6 // 10 * Window.epsWidth
        key_setter_height = self.size_width // 10 * Window.epsWidth
        self.key_setter = ttk.Entry(font=ttk.font.Font(size=round(key_setter_height / 4)))
        self.key_setter.place(x=key_setter_px, y=key_setter_py,
                              width=key_setter_width, height=key_setter_height)

        # 爬取按钮设置
        search_button_icon = ttk.PhotoImage(file=os.path.join("image", "search.png"))
        search_button_icon = search_button_icon.subsample(round(300 / key_setter_height),
                                                          round(300 / key_setter_height))
        self.search_button = ttk.Button(image=search_button_icon, command=self.search)
        self.search_button.image = search_button_icon
        self.search_button.place(x=key_setter_px + key_setter_width, y=key_setter_py,
                                 width=key_setter_height, height=key_setter_height)

        # 爬取数量输入框设置
        amount_setter_width = self.size_width // 6 * Window.epsWidth
        amount_setter_height = key_setter_height // 2
        amount_setter_px = key_setter_px
        amount_setter_py = self.size_height * 2 // 3 * Window.epsHeight
        self.amount_setter = ttk.Combobox(values=[10 * i for i in range(1, 11)],
                                          font=ttk.font.Font(size=round(amount_setter_height / 4)))
        self.amount_setter.place(x=amount_setter_px, y=amount_setter_py,
                                 width=amount_setter_width, height=amount_setter_height)

        # R18 按钮设置
        self.open_r18 = ttk.BooleanVar(value=False)  # 将是否开启 R18 选项绑定到 self.open_r18
        self.r18_button = ttk.Checkbutton(bootstyle=("square", "toggle", "primary"),
                                          variable=self.open_r18,
                                          command=self.update_open_r18)
        r18_button_width = key_setter_height * 2 // 3
        r18_button_height = key_setter_height // 3
        r18_button_px = key_setter_px + key_setter_width + key_setter_height - 2 * r18_button_height
        r18_button_py = amount_setter_py
        self.r18_button.place(x=r18_button_px, y=r18_button_py,
                              width=r18_button_width, height=r18_button_height)

        # 填入提示词
        self._set_entry_placeholder(self.amount_setter, '图片数')
        self._set_entry_placeholder(self.key_setter, '关键词')
        
        # 创建一个菜单栏
        menu_bar = ttk.Menu()
        # 为 Window 配置这个菜单栏, 此时该菜单栏变为主按钮
        self.config(menu=menu_bar)
        # 创建另一个菜单栏, 父元素设置为 menu_bar
        # 准备成为附属于该菜单按钮的菜单栏, 用于保存子菜单选项
        choices = ttk.Menu(master=menu_bar)
        # 为主菜单栏配置一个名称, 并且确认子菜单栏是 choices
        menu_bar.add_cascade(label="设置", menu=choices)
        # 为子菜单栏配置选项参数
        choices.add_command(label="Cookie", command=self.update_cookie)
        choices.add_command(label="保存路径", command=self.update_save_path)
        choices.add_command(label="代理地址", command=self.update_proxy)
        choices.add_command(label="窗口大小", command=self.update_windows_size)

    def _set_entry_placeholder (self, entry, text):
        """为可输入文字的组件添加占位符"""
        def on_focus_in (event):
            if entry.get() == text:
                entry.delete(0, ttk.END)
                entry.config(foreground="black")

        def on_focus_out (event):
            if entry == self.amount_setter:
                try:
                    int(entry.get())
                except ValueError:
                    entry.delete(0, ttk.END)
            
            if not entry.get():
                entry.insert(0, text)
                entry.config(foreground="grey")

        entry.insert(0, text)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.config(foreground="grey")
        
    def update_open_r18 (self):
        self.spider.open_r18 = self.open_r18.get()
        
    def search (self):
        if self.key_setter.get() == "关键词":
            Messagebox.show_warning(title="警告", message="请输入关键词")
            return
        if self.amount_setter.get() == "图片数":
            Messagebox.show_warning(title="警告", message="请输入图片数")
            return
        self.spider.key = self.key_setter.get()
        self.spider.amount = int(self.amount_setter.get())
        self.spider.run()
        
    def update_save_path (self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.spider.save_path = os.path.join(folder_path)
            with open(os.path.join("AppData", "config.json"), 'r', encoding="UTF-8") as file:
                data_config = json.load(file)
            data_config["save_path"] = folder_path
            with open(os.path.join("AppData", "config.json"), 'w', encoding="UTF-8") as file:
                json.dump(obj=data_config, fp=file, ensure_ascii=False, indent=4)
            Messagebox.show_info(title='提示', message=f'保存路径已更新至  {folder_path}')

    def update_cookie (self):
        user_cookie = simpledialog.askstring("修改 Cookie", "请输入 Cookie:")
        user_cookie = user_cookie.strip()
        if user_cookie:
            self.spider.cookie = user_cookie
            with open(os.path.join("AppData", "config.json"), 'r', encoding="UTF-8") as file:
                data_config = json.load(file)
            data_config["cookie"] = user_cookie
            with open(os.path.join("AppData", "config.json"), 'w', encoding="UTF-8") as file:
                json.dump(obj=data_config, fp=file, ensure_ascii=False, indent=4)
            Messagebox.show_info(title='提示', message=f'Cookie 已更新为  {user_cookie}')
    
    def update_proxy (self):
        user_proxy = simpledialog.askstring("修改代理地址", "请输入代理地址:")
        user_proxy = user_proxy.strip()
        if user_proxy:
            if not re.match(r"http://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}$", user_proxy):
                Messagebox.show_warning(title="警告", message="请输入正确的代理地址, 如 http://127.0.0.1:10809")
                return
            self.spider.proxy = user_proxy
            with open(os.path.join("AppData", "config.json"), 'r', encoding="UTF-8") as file:
                data_config = json.load(file)
            data_config["proxy"] = user_proxy
            with open(os.path.join("AppData", "config.json"), 'w', encoding="UTF-8") as file:
                json.dump(obj=data_config, fp=file, ensure_ascii=False, indent=4)
            Messagebox.show_info(title='提示', message=f'代理地址已更新为  {user_proxy}')
            
    def update_windows_size (self):
        user_size = simpledialog.askstring("修改窗口大小", "请输入窗口大小(width x height):")
        user_size = user_size.strip()
        if not re.match(r"(100|[1-9][0-9]?)x(100|[1-9][0-9]?)$", user_size):
            Messagebox.show_warning(title="警告", message="请输入正确的窗口大小, 长和宽均为 1 至 100 之间的整数, 如 20x25")
            return
        user_width, user_height = user_size.split('x')
        self.size_width, self.size_height = int(user_width), int(user_height)
        with open(os.path.join("AppData", "config.json"), 'r', encoding="UTF-8") as file:
            data_config = json.load(file)
        data_config["size_width"] = user_width
        data_config["size_height"] = user_height
        with open(os.path.join("AppData", "config.json"), 'w', encoding="UTF-8") as file:
            json.dump(obj=data_config, fp=file, ensure_ascii=False, indent=4)
        Messagebox.show_info(title='提示', message=f'窗口大小已更新为  {user_width}x{user_height}, 重启后生效')

if __name__ == "__main__":
    window = Window()
    window.mainloop()