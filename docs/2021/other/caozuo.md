---
title: 计算机命令
date: 2021-01-31
autoGroup-3: 知识 
categories:
    - Knowledge
tags:
    - Tool
sidebarDepth: 3
publish: true
---

::: tip
在这里记录计算机批处理小技巧 (win + L to locker the computer)
:::

<!-- more -->

## Latex相关
```tex
% 1. inline mode 数学公式超出边界, 做法就是在document加\sloppy
\begin{document}\sloppy
...
\end{document}

% 2. conditonal on 符号, 用bigg或者更大的Bigg, 然后rvert是丨, 如果是希望自动调整高度
\left. \frac{1}{H(\hat S)} \right\rvert_{y=Y}

% 3. 在align环境下如果想把label放在某一行, 得每行后面加\nonumber

```

## Git相关
参考资料： [subtree教程](https://segmentfault.com/a/1190000012002151)
```bash
: '
⚛️ 创建远程分支
🕉️ 以某一个文件夹为蓝本在当前目录下创建一个子分支child, squash表示不考虑过往commit
✡️ 清除远程与本地不兼容的文件
☸️ 突然告诉我Connection was reset in connection to github.com:443
'

# 创建远程分支
git remote add deploy https://github.com/dennislblog/infosys.git

# 以某一个文件夹为蓝本在当前目录下创建一个子分支child, squash表示不考虑过往commit
git subtree split --prefix=other --squash --branch child

# 清除远程与本地不兼容的文件
git rm -r --cached to-delete-folder
git add . => git commit -m "msg" => git push remote local

# 突然告诉我Connection was reset in connection to github.com:443
# 从电脑-settings-proxy找到代理端口, 我现在的VPN是10809, 之后出国unset就好了
git config --global http.proxy http://127.0.0.1:10809
git config --global https.proxy http://127.0.0.1:10809
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 自动生成安装依赖
```bash
# 加"encoding"是考虑有汉字注释的原因
pipreqs --encoding=utf-8 ./
```

## Python对象占用内存大小
```python
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

"""返回比特字节
get_size(instance)
>> 3.037754 x 1e6 bytes
"""
```

## 子文件夹
Move all files from subdirectories to current directory
```bash
mv */*.ipynb .                     #将子文件夹内ipynb文件全部放到当前文件夹
find . -type d -empty -delete      #将内容为空的子文件夹删除
```

## 批量转换Jupyter
```bash
workon imitate & jupyter nbconvert --to html *.ipynb

# pip 换源 (Windows配置信息在pip.ini里)
pip config set global.index-url http://pypi.python.org/simple/
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple

# conda 换源 (.condarc文件)
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes  #显示包的来源
conda config --remove-key channels        #清空源配置, 出国
```

## 在错误出现之前调错
```bash
python -m ipdb -c continue *.py
```

## Python画图全局尺寸
```python
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 10, 3
```
## Python改变小数精度
```python
np.set_printoptions(precision = 4)
# 或者直接 %precision 4
```
## Python处理遍历失败
```python
"""在for循环完整完成后才执行else, 如果中途跳出循环, 则一并跳过else语句
"""
for i in range(n):
    if f(i) >= threshold: break
else:
    print("all below threshold")
```

## Jupyter自动补全
Jupyter lab中的TAB键失去作用, [参考这里](https://stackoverflow.com/questions/44186370/kernel-taking-too-long-to-autocomplete-tab-in-jupyter-notebook)
```python
# 进入ipython_config.py
c.Completer.use_jedi = False
```

## Jupyter-Plotly一片空白
折腾半天，发现Windows上安装还是傻逼安装最[简单](https://nodejs.org/en/download/)
```bash
# 安装 nodejs
conda install -c conda-forge nodejs  
# 安装jupyer lab plotly
jupyter lab clean; jupyter lab build
```
但是他给我报错, 好像是[webpack](https://github.com/jupyterlab/jupyterlab/issues/9533)的问题, 于是更新jupyterlab到`3.0.6`
```python
"""
先更新 jupyter lab
pip install --upgrade jupyterlab
jupyter labextension install jupyterlab-plotly
"""
import plotly.express as px
fig = px.line(x=["a","b","c"], y=[1,3,2], title="sample figure")
fig.show()
```

## IPython指令
```python
%precision 4        # sets printed precision for floats to 4 decimal places
%whos               # gives a list of variables and their values
%quickref           # gives a list of magics
```

## NPM安装错误
直接`npm install --ignore-scripts`
```python
"""
gyp ERR! stack     import sys; print "%s.%s.%s" % sys.version_info[:3];
"""
```

## 更新环境变量
```bash
set PATH=C  # 关闭后再打开 echo %PATH% 可以看见更新的路径
```

## 关闭占用端口程序
这里示范怎么把占用端口$8891$的程序后台强行关闭
```bash
netstat -ano | findstr 8891
netstat -nltp                   # 用端口找程序
# TCP    127.0.0.1:8891         0.0.0.0:0              LISTENING       40128
taskkill /F /PID 40128          # Windows系统
kill -s 9 40128                 # Linux系统, -s指定信号为9(意思是强行关闭), 如果不加则不一定关得了
# SUCCESS: The process with PID 40128 has been terminated.
```

## CentOS Yum卡在某一个包没有正常安装
```bash
:'
先安装yum-utils, 然后把这个包卸了
'
yum --disablerepo=google-cloud-monitoring -y install yum-utils
yum-config-manager --disable google-cloud-monitoring
```

## 连接VPS
👨‍🎓管理员身份密码登录;
```bash
sudo -i                     # 切换到root角色
vi /etc/ssh/sshd_config     # 修改PermitRootLogin和PasswordAuthentication为yes
passwd root                 # 给root设置密码
systemctl restart sshd      # centos 7里系统命令
```
👶普通用户密钥登录
- 将私钥`.ppk`对应的公钥粘贴到GCP的`Compute Engine -> Metadata -> SSH Keys`里就可以用私钥配合用户名登录了(注意私钥的用户名就是登录的用户名)
👨‍🦳可以考虑装个宝塔面板管理, 方便查看文件和系统信息
```bahs
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install.sh && sh install.sh
```

## 安装Jupyter Lab
::: tip
- 安装`wget`,`bzip2`等小工具
- 根据系统是32位还是64位去`https://repo.anaconda.com/archive/`下载最新的安装包
- 更改用户权限, 然后安装
- 新建一个环境, 然后配置Jupyter Lab, 并且把防火墙对应的端口打开
```bash
# 安装wget, 另外把比较新的源都加到yum里
curl -fsSL https://rpm.nodesource.com/setup_15.x | sudo bash -  
sudo yum -y install wget bzip2 nodejs gcc-c++ 
# 查看系统内核
uname -a 
:'
Linux instance-1 3.10.0-1160.21.1.el7.x86_64 #1 SMP Tue Mar 16 18:28:22 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
也可以通过 cat /etc/redhat-release 和 file /bin/ls 查看
'
# 安装
chmod +x Anaconda3-5.3.1-Linux-x86_64.sh
./Anaconda3-5.3.1-Linux-x86_64.sh
conda update conda; conda update all
source ~/.bashrc
conda create -n env_name python=3.8 anaconda # conda info -e 列出所有安装环境
# 配置
source activate env_name                     # 退出环境 source deactivate
jupyter lab --generate-config
vim ~/.jupyter/jupyter_notebook_config.py
:'
更改如下
c.NotebookApp.token = ''
c.NotebookApp.allow_root = True
c.NotebookApp.open_browser = False
c.NotebookApp.notebook_dir = 'notebook'
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8890
'
firewall-cmd --zone=public --remove-port=8890/tcp --permanent  # 好像得去VPC-firewall-rule设置才可以, 并且确定实例是静态IP(花钱)
act thesis && jlab
:'
最后浏览器访问 http://34.92.236.104:8890 便可, 另附上我的快捷键设置
'
alias jlab='nohup jupyter-lab > logs/jupyter.log 2>&1 &'
alias act='foo() { source activate "$1"; }; foo'
alias grep='grep --color=auto'
alias jconfig='vim ~/.jupyter/jupyter_notebook_config.py'
```
:::

## 在CentOS中如何把Node.js从V6升级到V15
```bash
node -v; npm -v   # v6.17.1; 3.10.10
curl -fsSL https://rpm.nodesource.com/setup_15.x | sudo bash -  # 增加源
ls -la /etc/yum.repos.d/|grep nodesource                        # 确定新源被添加
sudo yum list available nodejs                                  # 可以安装V15了
sudo yum install nodejs
```

## ~~Conda不小心崩了, 怎么撤销傻逼操作,~~ 怎么创建虚拟环境
::: tip
`mkvirtualenv -p python3 thesis`创建虚拟环境
```bash
$ mkvirtualenv [-a project_path] [-i package] [-r requirements_file] [virtualenv options] ENVNAME  
$ allvirtualenv pip install -U pip
$ rmvirtualenv ENVNAME
```
:::
```bash
conda list --revision      
:'
2021-04-04 20:30:21  (rev 1)
     ca-certificates  {2018.03.07 -> 2021.1.19}
     intel-openmp  {2019.0 -> 2020.2}

2021-04-04 20:34:11  (rev 2)
     certifi  {2018.8.24 -> 2020.12.5}
     chardet  {3.0.4 -> 4.0.0}
'
conda config --set allow_conda_downgrades true
conda install --revision 1  # 恢复安装到(rev 1)节点
conda clean --all           # 清除所有可能带有不正确安装的信息

:'
事实证明conda和pip还是不要混着用, 还是直接用virtualenv管理比较好
'
pip install virtualenv && pip install virtualenvwrapper
:'
把下面两句加到用户启动里, 这样就可以用workon/mkvirtualenv等命令
'
export WORKON_HOME=$HOME/.virtualenvs
source ~/anaconda3/bin/virtualenvwrapper.sh
```

## WRDS和GCP之间传递文件
```bash
:'
paramiko有窗口大小的问题, 采用rsync方法(速度不要太快)
在此之前, 我还把所有CSV文件单独转换成了ZIP
#!/usr/bin/env python3
import sys
from pathlib import Path
from zipfile import ZipFile

src_dir, dest_dir = map(Path, sys.argv[1:])
for filename in src_dir.glob('*.csv'): # enumerate all csv-files in the src folder
    # zip each file individually
    with ZipFile(str(dest_dir / (filename.stem + '.zip')), 'w') as archive:
        archive.write(str(filename), arcname=filename.name)
'
yum install rsync -y
rsync -zrP dennislx@wrds-cloud.wharton.upenn.edu:/scratch/udel/dennislx/data.zip ~/notebook/wrds/data.zip
```