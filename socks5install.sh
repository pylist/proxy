#!/bin/bash

wget -O sock5.py https://raw.githubusercontent.com/pylist/proxy/master/sock5.py
yum install epel-release -y
yum makecache -y
yum install python3 -y
python3 $HOME/sock5.py
