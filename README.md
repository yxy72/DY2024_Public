# 简介
结合深度学习、知识图谱技术对典型工业产品建立质量管控系统，实现产品的质量预测、知识图谱建模、关键参数工艺优化和质量知识可视化分析。

# 部署
## 配置前端
前端基于vue3和vue-cli脚手架。
1. 该项目的`node`环境版本为`16.13.1`，在`/web`目录下运行`npm install`下载依赖。
2. 在`/web/src/store/index.js`中，将`state.server.address`更改为服务器的实例地址。
3. 运行`npm run build`打包前端工程。
## 配置后端
后端基于`Django4`，数据库为`MySQL`和`Neo4j`
1. 打开`/server/DY_Server_Py/settings.py`文件，修改`CORS_ORIGIN_WHITELIST`配置项设置跨域白名单。
2. 修改`ALLOWED_HOSTS`添加服务器部署地址。
3. 修改`DATABASES`中`MySQL`数据库的连接信息。
4. 配置完数据库后发布Django服务。
### 配置MySQL
1. `MySQL`版本为`8.0.34`，需要建立数据库名为`dy`，数据库字符集为`utf8mb4`，数据库排序规则为`utf8mb4_bin`，其他设置可能会导致错误。
2. 在`/server`中，运行`python manage.py makemigrations`和`python manage.py migrate`以建立数据库初始表。
3. 在`/server/init`中，运行`python init_mysql.py "127.0.0.1" "root" "password"`来给数据库表初始化。
### 配置Neo4j
1. 安装`neo4j`版本为`4.4.29`，在安装该版本之前需要先安装`JDK 11`。
2. 修改`/neo4j/conf/neo4j.conf`配置文件，根据情况判断是否打开外网访问。
3. 修改`/server/config.py`中的`neo4j_username`、`neo4j_password`和`neo4j_url`字段为当前图形数据库的实际部署信息。
3. 在`/server/init`中，运行`python init_kg.py "bolt://127.0.0.1:7687" "neo4j" "password"`来给图形数据库表初始化。
# 一些预览

![QQ截图20240803195258](https://github.com/user-attachments/assets/2a17b837-c31d-4f00-b12a-46c1ac326b4d)
![QQ截图20240803195533](https://github.com/user-attachments/assets/6055046e-c601-47e1-8c5f-977cd4432d8f)
![QQ截图20240803195617](https://github.com/user-attachments/assets/e99cb241-03a0-47b6-911e-38bd9a87ef43)
![QQ截图20240803195555](https://github.com/user-attachments/assets/66bcb523-d248-4032-bad0-4feebe4d2088)

# 项目待改进点
1. 基于anyscipt的编程：在`typescript`里使用`any`类型限定过多，违背了`typescript`的设计初衷。（该项目使用`ts`的原因是element-plus组件库的高性能列表el-table-v2的api文档只支持`ts`，嘿嘿）
2. Vue组件化：项目里每一个页面都是一个`.vue`文件，没有充分利用到vue组件化开发的特点。经查找，以下界面的功能可以组件化：
* **模型读取组件**：质量预测-数据预测界面的模型信息、时序分析-CRNN模型/LSTM模型的模型信息、时序分析-工艺优化的载入分类模型。以上三处可以独立出“读取模型信息”独立组件。
* **数据预处理组件**：质量预测-导入数据-预处理、应用工具-数据预处理。以上两处可以独立出“数据预处理”独立组件。
* **高性能表格显示组件**：质量预测-导入数据、质量预测-数据预测-特征数据、时序分析-CRNN模型/LSTM模型-样本信息、时序分析-单目标优化-载入优化参数范围、知识图谱-创建三元组、应用工具-数据预处理。以上六处可以集成基于el-table-v2的“高性能表格读取显示组件”。
