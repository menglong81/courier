FROM centos:7
MAINTAINER menglong.zhou <345010969@qq.com>
RUN mkdir -p /home/q/www/courier
WORKDIR /home/q/www/courier
ADD . /home/q/www/courier


# 安装python3 配置pip
RUN yum -y install python3 python3-pip gcc make
RUN python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple/

RUN tar -zxvf sqlite-autoconf-3370200.tar.gz && cd sqlite-autoconf-3370200 && ./configure && make && make install
RUN mv /usr/bin/sqlite3 /usr/bin/sqlite3.bk &&  ln -s /home/q/www/courier/sqlite-autoconf-3370200/sqlite3 /usr/bin/sqlite3
RUN echo 'export LD_LIBRARY_PATH="/usr/local/lib"'>> /etc/profile && source /etc/profile


# 安装依赖
RUN pip3 install -r requirements/requirements_unix.txt

# 对外暴露端口
EXPOSE 8080

# 进入到项目目录
WORKDIR /home/q/www/courier

# 运行测试项目
ENV LD_LIBRARY_PATH "/usr/local/lib"

CMD ["python3","manage.py","runserver", "0.0.0.0:8080"]
