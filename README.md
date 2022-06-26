# ebuydotcom

#### 介绍

一个用Python Flask开发的电商平台应用，采用微服务架构

#### 项目结构

本应用采用微服务架构，主要服务介绍如下：

1. tbfile - 文件服务，提供图片上传、下载、查询接口
2. tbmall - 商城服务，提供与店铺、产品相关的接口
3. tbbuy - 购买服务，提供与订单、购物车等相关的接口
4. tbadmin - 后台管理服务，提供与用户管理相关的接口
5. tbweb - 主服务，提供从浏览器访问网站页面的接口

#### 其它目录

1. tblib - 共享库，包含错误处理、数据库连接管理及请求处理相关函数 

#### 前期准备

1.  配置MongoDB GridFS
2.  配置MySQL数据库，创建数据表
3.  配置相应的API测试用例（例：在Postman里）

#### 快速启动

1. clone项目仓库到本地
2. 进入各服务所在目录，在不同终端窗口中运行各目录下的run.bat （确保MongoDB和MySQL处于运行状态）
3. 进入项目主目录，运行run.bat

#### 使用说明


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
