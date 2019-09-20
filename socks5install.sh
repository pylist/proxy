#!/bin/bash

wget -O sock5.py https://raw.githubusercontent.com/pylist/proxy/master/sock5.py
yum install epel-release -y
yum install python36 -y
python3 $HOME/sock5.py