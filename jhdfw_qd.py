# !/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author : Code.K
# cron "5 9 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('建行大富翁进阶打卡CC豆')
# 活动信息: 建行大富翁进阶打卡 得CC豆 功能：每日自动签到 领豆
# 活动地址：https://lsjr.ccb.com/msmp/ecpweb/page/ty/dailysign/index.html
# 微信打开 抓 lsjr.ccb.com 该域名 headers 里的 token值 ey*****************
# 环境变量：jhdfwtoken 填抓到的 ey*****************

import random
import os
import sys
import platform
import subprocess
import time

from functools import partial
import concurrent.futures

token = os.environ.get("jhdfwtoken")
if token is None:
    print(f'⛔️未获取到ck：请检查变量是否填写 变量名：jhdfwtoken，格式：thirdId#wid#备注')
    exit(0)

if '@' in token:
    tokens = token.split('@')
else:
    tokens = [token]

print(f'✅获取到{len(tokens)}个账号 当前设置并发数: {bf}')

file_url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/Code-KKK/pycode/main/compiled/'

def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [10,11]) and o.lower() in ['linux'] and a.lower() in ['x86_64','aarch64']:
        print("当前环境符合运行要求")
        if o.lower() == 'linux':
            file_name += '.so'
            main_run(file_name, v.minor, o.lower(), a.lower())
    else:
        if not (v.minor in [10,11]):
            print("不符合运行要求: Python版本不是3.10.X 或 3.11.X")
        if not (o.lower() in ['linux']):
            print(f"不符合运行要求: 操作系统类型[{o}] 支持：Linux")
        if not (a.lower() in ['x86_64','aarch64']):
            print(f"不符合运行要求: 当前处理器架构[{a}] 支持：x86_64 aarch64")

def main_run(file_name, py_v, os_info, cpu_info):
    if os.path.exists(file_name):
        file_name_ = os.path.splitext(file_name)[0]
        Code_module = __import__(file_name_)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for num in range(len(tokens)):
                runzh = num + 1
                run = Code_module.CCBDFW(tokens[num],runzh)
                executor.submit(run.main)
                time.sleep(random.randint(2, 3))
    else:
        print(f"不存在{file_name}依赖模块,准备下载模块文件")
        download_file(file_name, py_v, os_info, cpu_info,file_url)

def download_file(file_name, py_v, os_info, cpu_info, url):
    file_name_ = os.path.splitext(file_name)[0]
    if os_info == 'linux':
        url = url + f'{file_name_}/{file_name_}.cp3{py_v}-{cpu_info}-{os_info}.so'
    if os_info == 'windows':
        url = url + f'{file_name_}/{file_name_}.cp3{py_v}-win_{cpu_info}.pyd'
    try:
        print(url)
        subprocess.run(["curl",'-#',"-o", file_name, url], check=True)
        print(f"{file_name}文件下载成功~开始执行~")
        check_environment(file_name_)
    except subprocess.CalledProcessError:
        print("下载失败，请检查 URL 或 网络问题。")

if __name__ == '__main__':
    print = partial(print, flush=True)
    check_environment("jhdfw")
    