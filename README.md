![](https://img.shields.io/github/languages/code-size/menglong81/courier.svg)
![](https://img.shields.io/badge/createby-menglong81-green)
# Courier

## 项目特点
 * 工单系统
 * 工单模板可配置
 * 工单选项可配置
 * 工单后台处理通过队列解耦 可自动化扩展

## 简介

Courier 是一个工单系统，它可以减少用户沟通成本，制定流程化和自动化标准的工具
* 工单页
![avatar](http://rcyc0zoae.bkt.gdipper.com/WechatIMG471.png)
* 模板创建
![avatar](http://rcyc0zoae.bkt.gdipper.com/WechatIMG475.png)
* 工单创建
![avatar](http://rcyc0zoae.bkt.gdipper.com/WechatIMG476.png)
* 使用分析
![avatar](http://rcyc0zoae.bkt.gdipper.com/WechatIMG474.png)

## 主要功能
* 动态配置工单模板
* 工单状态管理
* 工单自动化配置
* 工单使用行为统计, 分析统计

## 注意
* 项目暂未接入ldap等登陆方式 可自行接入 ldap认证通过后把用户加入到对应的组即可
* 目前登陆走的还是django user中的登陆
* 除了管理员有全局视图，每个用户都有自己的视图, 如需修改请在admin.py中修改

## 应用结构

* app_ticket/
	主代码部分
	* api 视图
	* lib 主要是处理方法，数据库操作
* common/
    中间件认证日志及其他
* conf
    配置文件
* templates
    html文件
* static
    js/css

## 安装方式1 docker启动 
   ```
   docker pull mageyoyo/courier:v1 
   docker run -d -p 8080:8080 --name courier mageyoyo/courier:v1 
   ```
## 安装方式2 手动安装手册
* 环境 Python:3.7+  pip:22.1.1
* 支持的浏览器: chrome, Firefox
* 安装virtualenv: `pip install virtualenv`
* 项目克隆
* 依赖安装
    ```
    pip3.7 install -r requirements/requirements_unix.txt
    ```
* 配置conf 
    ```
    根据自己目录配置log_path 如需要修改数据库配置 自行更改setting.py
    ```
* 创建用户
    ```
     python3.7 manage.py createsuperuser
    ```
* 启动程序
    ```
    python3.7 manage.py runserver 0.0.0.0:8000
    or
    sh start.sh 需要修改脚本中的目录
    ```
* 登陆控制台
    ```
    http://127.0.0.1:8000/courier/admin
    默认用户名: zhoumenglong 密码: adminadmin
    ```
* 可增加Nginx配置
    ```
    server
    {
            listen  80;
            root /home/q/www/index/;
            server_name demo.xxx;

            location /courier {
                proxy_pass http://127.0.0.1:8000;
            }
            location /static/courier/ {
		        root /home/q/www/zhoumenglong_test/courier/;
            }
            location /media/courier/ {
		        root /home/q/www/zhoumenglong_test/courier/;
            }
            location /static/admin/ {
		        alias /home/q/www/zhoumenglong_test/courier/static/courier/website/admin/;
            }
    }
    ```
   