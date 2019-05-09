# CRM客户关系管理系统

基于学员，讲师，销售，运营等不同的角色开发而成的客户关系系统
本项目是以一个教育平台作为业务背景开发的crm系统


## 开发环境

* Python3
* django2
* django自带的sqlite3数据库


## 主要功能

* 利用了django的admin组件原理，开发了一个同原理的组件startX，可快捷生成一个系统平台

* 基于不同的角色实现不同的功能，并做权限限制


###  以下为主要角色（只列举了主要功能）：
####  学员：
* 提交作业
* 查看作业批改情况

#### 导师：
* 批改作业
* 查看整个班级的作业提交情况
* 跟进学员学习进度

#### 销售：
* 创建私人客户，编辑客户信息
* 从公共客户中拉取到私人客户
* 跟进客户记录
* 创建缴费记录

### 财务：

* 审批学员的缴费记录
* 准许学员入学
* 驳回入学申请

### CEO：

* 公司主要业务
	 
### 技术员：

* 测试时带有所有的功能

## startX组件

* 在项目启动时自动生成表对应的url,以及url对应的视图函数
* 高效快速实现增删改查
* 结合不同角色的权限控制相关的功能

## crm

* 主要的业务逻辑部分
* 具体根据各个公司的规模，项目需求而定

## 说明

* 所有的用户登录密码都为:123
* 账号名可在数据库里查看

## 程序流程图

* http://naotu.baidu.com/file/9a523a85cb424db52788019b156fb910?token=c05f21d9d79d01f9




## 启动项目
	```python  Python manage.py runserver XXXX(您的ip和端口)```
	
* 页面展示
	
![后台登录页面](https://raw.githubusercontent.com/yang-va/pictures/master/19.png)

![后台首页](https://raw.githubusercontent.com/yang-va/pictures/master/20.png)

![菜单列表](https://raw.githubusercontent.com/yang-va/pictures/master/21.png)

![权限批量分配页面](https://raw.githubusercontent.com/yang-va/pictures/master/22.png)

![账单列表](https://raw.githubusercontent.com/yang-va/pictures/master/23.png)

![账单报表](https://raw.githubusercontent.com/yang-va/pictures/master/24.png)

![用户列表](https://raw.githubusercontent.com/yang-va/pictures/master/25.png)

![注册用户分析](https://raw.githubusercontent.com/yang-va/pictures/master/26.png)

![角色列表](https://raw.githubusercontent.com/yang-va/pictures/master/27.png)

![角色功能分配](https://raw.githubusercontent.com/yang-va/pictures/master/28.png)

![学生列表](https://raw.githubusercontent.com/yang-va/pictures/master/29.png)

![课程列表](https://raw.githubusercontent.com/yang-va/pictures/master/30.png)

![课程详情列表](https://raw.githubusercontent.com/yang-va/pictures/master/31.png)






