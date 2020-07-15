import os
from fabric import Connection
from time import sleep
#CentOS7.0外网已连接部署。

def put_file(filename,conn):
    '''
    放同名文件
    '''
    conn.put(filename,filename)


def pip3_local_install(user,mod,mod_dir):
    '''
    用pip3本地文件夹离线安装，user安装的用户，mod模块名，mod_dir模块离线包目录
    安装完成后删除文件夹
    '''
    if user=='root':
        conn.run(f'pip3 install {mod} --no-index --find-links=file:///{user}/{mod_dir}')
        conn.run(f'rm -rf /{user}/{mod_dir}')
    else:
        conn.run(f'pip3 install {mod} --no-index --find-links=file:///home/{user}/{mod_dir}')
        conn.run(f'rm -rf /home/{user}/{mod_dir}')



def excute_any(command,conn):
    '''
    执行命令即使知道会返回错误
    '''
    try:
        conn.run(command)      #解决错误通过find / -name "*libcap.so*"找到文件/usr/bin/ld: cannot find -lcap
    except:pass


def sed_on_vsftpd_config(newtext,newtext_value,conn,filepath='/etc/vsftpd/vsftpd.conf'):
    if not f'{newtext}=' in conn.run(f'cat {filepath} | grep -v "#"').stdout:
        conn.run(f"sed -i '$a {newtext}={newtext_value}' {filepath}")
    try:
        next_grep=conn.run(f'cat {filepath} | grep -v "#" | grep "{newtext}={newtext_value}"').stdout
    except:
        next_grep=''
    if not newtext+'='+newtext_value in next_grep: 
        conn.run(fr"sed -i 's/{newtext}.*/{newtext}={newtext_value}/g' {filepath}")


def make_file_upload_and_delete(filename,strdd,target_filename,conn):
    '''
    打开临时文件，写完支行上传到服务器。
    '''
    with open(filename,'wb') as f:
        f.write(strdd.encode())
        f.close()
    conn.put(filename,target_filename)
    os.remove(filename)





host='175.24.111.140'
user='root'
password='Dan;06623QQ'
hostname='DDWebHost'
web_user='django_dd'
web_user_pass='Dan;06623'
dd_sudo='sudo -u '+web_user+' '

conn=Connection(host, user=user,connect_kwargs={"password": password})


conn.run('yum install git -y')    #安装git
#安装nigix要点（用户名的更改、/和/static的设置）

conn.run('yum install nginx -y')



conn.run('cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf_back')





# 修改配置文件为web用户可配置并添加配置文件目录到HTTP块
conn.run(fr"sed -i 's/user .*;/user {web_user};/g' /etc/nginx/nginx.conf")
conn.run(r"sed -ri 's/(include .*mime.types;)/\1\n    include             \/etc\/nginx\/sites-enabled\/*;/g' /etc/nginx/nginx.conf")

# 新建配置文件夹
conn.run('mkdir -p /etc/nginx/sites-availiable')
conn.run('mkdir -p /etc/nginx/sites-enabled')
domain_name='www.caylxxkj.xyz'

#添加文件，并写入配置
conn.run(f'touch /etc/nginx/sites-availiable/{domain_name}')
strdd='''
server {
    listen 80;
    server_name www.caylxxkj.xyz;
    location / {
        proxy_pass http://localhost:8000;
    }
    
    location /static {
            
            alias /home/django_dd/sites/ylkjddtestweb/static;
    }
    
}


'''
make_file_upload_and_delete(domain_name,strdd,f'/etc/nginx/sites-availiable/{domain_name}',conn)
# conn.run(f"sed -i '$a {strdd}' /etc/nginx/sites-availiable/{domain_name}")




excute_any(f'ln -s /etc/nginx/sites-availiable/{domain_name} /etc/nginx/sites-enabled/{domain_name}',conn)



conn.run('systemctl restart nginx')



#进入web_user用户部署应用

conn=Connection(host, user=web_user,connect_kwargs={"password": web_user_pass})
conn.run('ls -a')




#更改pip3源
strdd='''[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
'''

conn.run("mkdir -p .pip/")
conn.run("mkdir -p .pip3/")
make_file_upload_and_delete('pip.conf',strdd,'.pip/pip.conf',conn)
make_file_upload_and_delete('pip3.conf',strdd,'.pip3/pip3.conf',conn)




#添加sqlite3开机启动

sqlite3_add_str='export LD_LIBRARY_PATH="/usr/local/lib"'
if not sqlite3_add_str in conn.run('cat .bashrc').stdout:
    strdd=conn.run('cat .bashrc').stdout+f'\n{sqlite3_add_str}\n'
    make_file_upload_and_delete('.bashrc',strdd,'.bashrc',conn)
conn.run('export LD_LIBRARY_PATH="/usr/local/lib"')
conn.run('source .bashrc')








REPO_URL = 'https://github.com/angeldrop/DD_TDD.git'


def deploy(conn):
    site_folder = f'/home/{web_user}/sites/ylkjddtestweb'
    conn.run(f'mkdir -p {site_folder}')
    with conn.cd(f'{site_folder}'):
        _create_directory_structure_if_necessary(conn)
    with conn.cd(f'{site_folder}/source/'):
        _get_latest_source(conn)
        _update_settings(r"['www.caylxxkj.xyz','localhost','127.0.0.1']",conn)
        _update_virtualenv(conn)
        _update_static_files(conn)
        _update_database(conn)


def _create_directory_structure_if_necessary(conn):
    for subfolder in ('database','static','virtualenv','source'):
        conn.run(f'mkdir -p {subfolder}')


def _get_latest_source(conn):
    if int(conn.run("[ -e '.git' ] && echo 11 || echo 10").stdout)==11:    #如果存在
        conn.run('git fetch')
    else:
        conn.run(f'git clone {REPO_URL} .')
    # current_commit = conn.local("git log -n 1 --format=%H", capture=True)
    conn.run('git pull')


def _update_virtualenv(conn):
    if int(conn.run("[ -e '../virtualenv/bin/pip3' ] && echo 11 || echo 10").stdout)==10:
        conn.run(f'/usr/local/bin/python3 -m venv ../virtualenv')
    conn.run('../virtualenv/bin/pip3 install --upgrade pip')
    conn.run('../virtualenv/bin/pip3 install psycopg2-binary')
    conn.run(f'../virtualenv/bin/pip3 install -r requirements.txt')


def _update_settings(site_name,conn):
    settings_path='superlists/settings.py'
    conn.run(f"sed -i 's/DEBUG = True/DEBUG = False/g' {settings_path}")
    conn.run(f'sed -i "s/ALLOWED_HOSTS.*/ALLOWED_HOSTS = {site_name}/g" {settings_path}')


def _update_static_files(conn):
    conn.run('../virtualenv/bin/python3 manage.py collectstatic --noinput')


def _update_database(conn):
    conn.run('../virtualenv/bin/python3 manage.py migrate --noinput')


deploy(conn)



#安装调试gunicorn
put_file('gunicorn-linux.zip',conn)
conn.run('unzip gunicorn-linux.zip')
conn.run(f'/home/{web_user}/sites/ylkjddtestweb/virtualenv/bin/pip3 install gunicorn --no-index --find-links=file:///home/{web_user}/gunicorn-linux')
conn.run(f'rm -rf /home/{web_user}/gunicorn-linux')


with conn.cd('/home/django_dd/sites/ylkjddtestweb/source'):
    conn.run('ls -a')
    conn.run('nohup ../virtualenv/bin/gunicorn --bind localhost:8000 superlists.wsgi:application &')

