# !/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author : Code.K
# cron "5 9 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('美团微信小程序天天赚钱')
# 活动信息:浏览赚金币，累计1000可以提现微信1元
# 微信打开 美团 小程序 抓 cube.meituan.com/topcube/api/toc/task/getUserTasks 
# 标头 headers 里的 token值 uuid值  openid值 openidcipher值 四个值依次用#号组合
# 环境变量 mtttzqck 填 token#uuid#openid#openidcipher (顺序一定不要搞错！)
# 多账号新建变量mtttzqck或者用 @ 分开
# 

import random
import os
import sys
import platform
import subprocess
import time

from functools import partial
import concurrent.futures

token = os.environ.get("mtttzqck")
if token is None:
    print(f'⛔️未获取到ck：请检查变量是否填写 变量名：mtttzqck')
    exit(0)

if '@' in token:
    tokens = token.split('@')
else:
    tokens = [token]

bf = os.environ.get("mtttzq_BF")
if bf is None:
    print(f'🈳️未设置并发变量，默认1')
    bf = 1

print(f'✅获取到{len(tokens)}个账号 当前设置并发数: {bf}')

file_url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/Code-KKK/pycode/main/compiled/'

def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [8,9,10,11]) and o.lower() in ['linux'] and a.lower() in ['x86_64','aarch64']:
        print("当前环境符合运行要求")
        if o.lower() == 'linux':
            file_name += '.so'
            main_run(file_name, v.minor, o.lower(), a.lower())
    else:
        if not (v.minor in [8,9,10,11]):
            print("不符合运行要求: Python版本不是 3.8 ~ 3.11")
        if not (o.lower() in ['linux']):
            print(f"不符合运行要求: 操作系统类型[{o}] 支持：Linux")
        if not (a.lower() in ['x86_64','aarch64']):
            print(f"不符合运行要求: 当前处理器架构[{a}] 支持：x86_64 aarch64")

def main_run(file_name, py_v, os_info, cpu_info):
    if os.path.exists(file_name):
        file_name_ = os.path.splitext(file_name)[0]
        try:
            Code_module = __import__(file_name_)
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(bf)) as executor:
                for num in range(len(tokens)):
                    runzh = num + 1
                    run = Code_module.MtTTZQ(tokens[num],runzh)
                    executor.submit(run.main)
                    time.sleep(random.randint(2, 3))
        except Exception as e:
            print('aarch64架构如遇青龙容器运行报错，请在库里lib目录下载修复ld-linux-aarch64.so.1.sh运行')
    else:
        print(f"不存在{file_name}功能模块,准备下载模块文件")
        download_file(file_name, py_v, os_info, cpu_info,file_url)

def download_file(file_name, py_v, os_info, cpu_info, url):
    file_name_ = os.path.splitext(file_name)[0]
    if os_info == 'linux':
        url = url + f'{file_name_}/{file_name_}.cp3{py_v}-{cpu_info}-{os_info}.so'
    try:
        print(url)
        result = subprocess.run(['curl', '-I', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], capture_output=True, text=True)
        if result.stdout.strip() == '404':
            print('服务器文件不存在,已停止下载')
        else:
            print('服务器文件存在，将开始下载')
            subprocess.run(["curl",'-#',"-o", file_name, url], check=True)
            print(f"{file_name}文件下载成功~开始执行~")
            check_environment(file_name_)
    except subprocess.CalledProcessError:
        print("下载失败，请检查 URL 或 网络问题。")

if __name__ == '__main__':
    print = partial(print, flush=True)
    check_environment("mt_ttzq")
    print('【美团·微信小程序天天赚钱】运行完成！🎉')
    