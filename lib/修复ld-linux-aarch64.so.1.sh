#!/bin/bash

#ld-linux-aarch64.so.1 是一个动态链接器（dynamic linker）的文件，用于ARM 64位架构上的Linux系统，是一个系统组件。
# 部分docker容器中因使用了精简的系统镜像，不会包含此文件，部分程序在运行时会使用动态链接器来查找和加载共享库

REMOTE_FILE="https://mirror.ghproxy.com/https://raw.githubusercontent.com/Code-KKK/pycode/main/lib/ld-linux-aarch64.so.1"
LOCAL_DIR="/usr/lib"

if [ -f "$LOCAL_DIR/ld-linux-aarch64.so.1" ]; then
    echo "ld-linux-aarch64.so.1动态链接器文件已存在，无需下载。"
else
    # 下载文件
    #wget -P "$LOCAL_DIR" "$REMOTE_FILE"
    # 或者使用curl
     curl -o "$LOCAL_DIR/ld-linux-aarch64.so.1" "$REMOTE_FILE"
    # 检查下载是否成功
    if [ $? -eq 0 ]; then
        echo "文件下载成功！"
    else
        echo "文件下载失败。"
    fi
fi
