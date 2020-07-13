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
        conn.run('pip3 install '+mod+' --no-index --find-links=file:///'+user+'/'+mod_dir)
        conn.run('rm -rf '+'/'+user+'/'+mod_dir)
    else:
        conn.run('pip3 install '+mod+' --no-index --find-links=file:///home'+'/'+user+'/'+mod_dir)
        conn.run('rm -rf '+'/home'+'/'+user+'/'+mod_dir)
    


def excute_any(command,conn):
    '''
    执行命令即使知道会返回错误
    '''
    try:
        conn.run(command)      #解决错误通过find / -name "*libcap.so*"找到文件/usr/bin/ld: cannot find -lcap
    except:pass


def sed_on_vsftpd_config(newtext,newtext_value,conn,filepath='/etc/vsftpd/vsftpd.conf'):
    if not newtext+'=' in conn.run('cat '+filepath+' | grep -v "#"').stdout:
        conn.run("sed -i '$a "+newtext+'='+newtext_value+"' "+filepath)
    try:
        next_grep=conn.run('cat '+filepath+' | grep -v "#" | grep "'+newtext+'='+newtext_value+'"').stdout
    except:
        next_grep=''
    if not newtext+'='+newtext_value in next_grep: 
        conn.run("sed -i 's/"+newtext+r'.*'+"/"+newtext+'='+newtext_value+"/g' "+filepath)


def make_file_upload_and_delete(filename,strdd,target_filename,conn):
    '''
    打开临时文件，写完支行上传到服务器。
    '''
    with open(filename,'wb') as f:
        f.write(strdd.encode())
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
conn.run('mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf_back')
strdd='''# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user django_dd;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
            # proxy_pass http://unix:/tmp/www.caylxxkj.xyz.socket;
            # proxy_set_header Host $host;
            proxy_pass http://localhost:8000;
        }

        location /static {
            
            alias /home/django_dd/sites/ylkjddtestweb/static;
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers HIGH:!aNULL:!MD5;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}

'''

make_file_upload_and_delete('nginx.conf',strdd,'/etc/nginx/nginx.conf',conn)

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








REPO_URL = 'https://github.com/angeldrop/test_a_site_source'


def deploy(conn):
    site_folder = f'/home/{web_user}/sites/ylkjddtestweb'
    conn.run(f'mkdir -p {site_folder}')
    with conn.cd(f'{site_folder}'):
        _create_directory_structure_if_necessary(conn)
    with conn.cd(f'{site_folder}/source/'):
        _get_latest_source(conn)
        _update_settings(r"['localhost',]",conn)
        _update_virtualenv(conn)
        _update_static_files(conn)
        _update_database(conn)


def _create_directory_structure_if_necessary(conn):
    for subfolder in ('database','static','virtualenv','source'):
        conn.run(f'mkdir -p {subfolder}')


def _get_latest_source(conn):
    if int(conn.run("[ -e '.git' ] && echo 11 || echo 10").stdout)==11:    #如果存在
        conn.run(f'git fetch')
    else:
        conn.run(f'git clone {REPO_URL} .')
    # current_commit = conn.local("git log -n 1 --format=%H", capture=True)
    conn.run(f'git pull')


def _update_virtualenv(conn):
    if int(conn.run("[ -e '../virtualenv/bin/pip3' ] && echo 11 || echo 10").stdout)==10:
        conn.run(f'/usr/local/bin/python3 -m venv ../virtualenv')
    conn.run('../virtualenv/bin/pip3 install --upgrade pip')
    conn.run('../virtualenv/bin/pip3 install psycopg2-binary')
    conn.run(f'../virtualenv/bin/pip3 install -r requirements.txt')


def _update_settings(site_name,conn):
    settings_path='superlists/settings.py'
    conn.run(f"sed -i 's/DEBUG = True/DEBUG = False/g' "+settings_path)
    conn.run(f'sed -i "s/ALLOWED_HOSTS.*/ALLOWED_HOSTS = {site_name}/g" '+settings_path)


def _update_static_files(conn):
    conn.run(f'../virtualenv/bin/python3 manage.py collectstatic --noinput')


def _update_database(conn):
    conn.run(f'../virtualenv/bin/python3 manage.py migrate --noinput')


deploy(conn)



#安装调试gunicorn
with conn.cd('/home/django_dd/sites/ylkjddtestweb/source'):
    conn.run('../virtualenv/bin/pip3 install gunicorn')
    conn.run('../virtualenv/bin/gunicorn superlists.wsgi:application')
    # conn.run('../virtualenv/bin/gunicorn --bind unix:/tmp/www.caylxxkj.xyz.socket superlists.wsgi:application')
