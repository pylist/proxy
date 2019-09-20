import re
import os,signal
import subprocess
url_3proxy = 'https://raw.githubusercontent.com/pylist/s5/master/3proxy.sh'
def re_ip():
    try:
        with open('ipaddr.txt', encoding='utf-8') as ip_addrs:
            ip_addr = ip_addrs.read()
    except FileNotFoundError:
        print('无法打开指定的文件!请创建IP地址文本文件!!!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    re_ipaddr = re.findall(r'10\.\d\.\d\.\d{1,3}', ip_addr)
    return re_ipaddr
ip_addr = re_ip()


def add_ip():
    ieth = 0
    for ip in ip_addr[1:]:
        print(ip+'已添加到网络接口')
        ip_test = 'DEVICE=eth0:%d\nBOOTPROTO=static\nONBOOT=yes\nIPADDR=%s\nNETMASK=255.255.255.0' % (ieth, ip)
        with open("/etc/sysconfig/network-scripts/ifcfg-eth0:%s" % str(ieth), 'w', encoding='utf-8') as file_ip:
            file_ip.write(ip_test)
        ieth += 1
    print('本机器IP总数: {}'.format(len(ip_addr)))
    subprocess.run('/etc/init.d/network restart', shell=True)

proxy3_cfg = ['daemon', 'nserver 8.8.8.8', 'nserver 8.8.4.4', 'nscache 65536', 'users user12333:CL:pwd12333', 'log /var/log/3proxy/3proxy.log D', 'logformat "- +_L%t.%. %N.%p %E %U %C:%c %R:%r %O %I %h %T"', 'rotate 30', 'auth iponly strong', 'flush', 'allow user', 'maxconn 384']
proxy3_path = os.path.join('/usr/local', '3proxy')
def proxyCfg(put_prot, put_user, put_pwd):
    proxy3_cfg[4] = 'users {}:CL:{}'.format(put_user, put_pwd)
    for ip in ip_addr:
        proxy3_cfg.append('socks -p{0} -i{1} -e{1}'.format(put_prot, ip))
    if not os.path.exists(proxy3_path):
        os.mkdir(proxy3_path)
    with open(proxy3_path + '/3proxy.cfg', 'w+', encoding='utf-8') as f:
        for line in proxy3_cfg:
            f.write(line+'\n')



def kill_proxy3():
    out = os.popen("ps aux | grep 3proxy").read()
    for line in out.splitlines():
        if '/usr/bin/3proxy' in line:
            pid = int(line.split()[1])
            os.kill(pid, signal.SIGKILL)


def main():
    put_num = input('请输入下面数字执行相应的功能:\n1 .添加ip\n2 .安装socks5\n3 启动socks5\n4 .修改socks5配置\n5 .退出程序\n请输入数字: ')
    if put_num == '1':
        add_ip()
        main()
    elif put_num == '2':
        subprocess.run('wget -O 3proxy.sh %s' % url_3proxy, shell=True)
        subprocess.run('chmod +x 3proxy.sh', shell=True)
        subprocess.run('./3proxy.sh', shell=True)
        put_prot = input("请设置你的socks端口:")
        put_user = input("请设置你的socks用户名: ")
        put_pwd = input("请设置你的socks5密码:")
        proxyCfg(put_prot, put_user, put_pwd)
        main()
    elif put_num == '3':
        subprocess.run('/usr/bin/3proxy {}/3proxy.cfg'.format(proxy3_path), shell=True)
        main()
    elif put_num == '4':
        put_prot = input("请设置你的socks端口:")
        put_user = input("请设置你的socks用户名: ")
        put_pwd = input("请设置你的socks5密码:")
        proxyCfg(put_prot, put_user, put_pwd)
        kill_proxy3()
        subprocess.run('/usr/bin/3proxy {}/3proxy.cfg'.format(proxy3_path), shell=True)
        main()
    elif put_num == '5':
        print('再见!!!!!!!!')
    else:
        print('你的输入有误')
        main()

if __name__ == "__main__":
    main()