# 简介

结合深度学习、知识图谱技术，对典型工业产品建立质量管控系统，实现产品质量预测、知识图谱建模、关键参数工艺优化和质量知识可视化分析。

## 部署

### 配置前端

前端基于 Vue 3、Element Plus 和 Vite。

1. 进入 `web` 目录。
2. 准备 Node.js 环境。项目可使用 `v24.18.0 LTS`。
3. 安装依赖：

   ```bash
   npm install
   ```

4. 启动开发服务器：

   ```bash
   npm run dev
   ```

5. 构建生产版本：

   ```bash
   npm run build
   ```

### 配置后端

后端基于 Django 4，数据库使用 MySQL 和 Neo4j。

1. 打开 `server/DY_Server_Py/settings.py` 文件，修改 `CORS_ORIGIN_WHITELIST`，配置跨域白名单。
2. 根据需要创建 Python 3.9 或 Python 3.10 虚拟环境。
3. 根据 `server/requirements.txt` 安装依赖。
4. 修改 `ALLOWED_HOSTS`，添加服务部署地址。
5. 修改 `DATABASES` 中 MySQL 数据库的连接信息。
6. 配置数据库后，启动 Django 服务。

#### 配置 MySQL

1. 使用 MySQL 8.x，创建名为 `dy` 的数据库。
2. 数据库字符集设置为 `utf8mb4`，排序规则设置为 `utf8mb4_bin`。其他设置可能导致错误。
3. 在 `server` 目录下运行以下命令，创建数据库初始表：

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. 在 `server/init` 目录下运行以下命令，初始化数据库表数据：

   ```bash
   python init_mysql.py "127.0.0.1" "root" "password"
   ```

#### 配置 Neo4j

1. 安装 Neo4j `4.4.29` 或 `5.x`。
2. 安装 Neo4j 前，需要先安装对应版本要求的 JDK，通常为 JDK 11 或 JDK 21。
3. 根据需要修改 `neo4j/conf/neo4j.conf` 配置文件，判断是否开启外网访问。
4. 修改 `server/configs.py` 中的 `neo4j_username`、`neo4j_password` 和 `neo4j_url` 字段，改为当前图形数据库的实际部署信息。
5. 在 `server/init` 目录下运行以下命令，初始化图形数据库：

   ```bash
   python init_kg.py "bolt://127.0.0.1:7687" "neo4j" "password"
   ```

## 预览

![预览图 1](https://github.com/user-attachments/assets/2a17b837-c31d-4f00-b12a-46c1ac326b4d)
![预览图 2](https://github.com/user-attachments/assets/6055046e-c601-47e1-8c5f-977cd4432d8f)
![预览图 3](https://github.com/user-attachments/assets/e99cb241-03a0-47b6-911e-38bd9a87ef43)
![预览图 4](https://github.com/user-attachments/assets/66bcb523-d248-4032-bad0-4feebe4d2088)

## TODO

**前端**

- TypeScript 使用不充分。
- 组件化程度较低。
- 状态管理耦合较高。

**后端**

- `views` 中的业务逻辑、运维逻辑和模型调用耦合较高，需要进一步分层。
- 训练任务异步化程度不足，容易阻塞。
- 生产参数建议改为环境变量配置。
