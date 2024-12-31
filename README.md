# MCP Reddit Server

[English](#english) | [中文说明](#chinese)

<h2 id="chinese">中文说明</h2>

## 1. 项目介绍

这是一个基于MCP（Model Context Protocol）协议的Reddit服务器，专门设计用于与Claude等大语言模型进行交互。通过这个服务，你可以让AI助手帮助你浏览和分析Reddit上的内容。

### 1.1 主要功能

- 搜索特定subreddit中的帖子
- 获取帖子详细信息和评论
- 浏览subreddit中的热门帖子

### 1.2 项目结构

```
nangeAGICode/reddit_chat_claude/
├── .github/
│   └── workflows/
│       └── docker.yml # GitHub Actions工作流配置
├── src/
│   ├── init.py
│   └── server.py # MCP服务器核心代码
├── .gitignore # Git忽略文件配置
├── Dockerfile # Docker构建文件
├── LICENSE # MIT许可证
├── README.md # 项目说明文档
└── requirements.txt # Python依赖包列表
```

## 2. 安装和配置

### 2.1 前提条件

- Docker（必须）
- Python 3.12+（用于本地开发）
- Reddit API凭证（必需）

### 2.2 获取Reddit API凭证

1. 访问 https://www.reddit.com/prefs/apps
2. 点击"create another app..."
3. 选择"script"
4. 填写必要信息
5. 获取client_id和client_secret

### 2.3 环境变量配置

需要设置以下环境变量：

```bash
REDDIT_CLIENT_ID=你的client_id
REDDIT_CLIENT_SECRET=你的client_secret
REDDIT_USER_AGENT=你的user_agent
```
### 2.4 Docker安装
MAC用户：
1.访问 Docker 官网：https://www.docker.com/products/docker-desktop
2.点击 "Download for Mac"
3.选择对应你的 Mac 芯片的版本（Apple Silicon 或 Intel）
4.下载并安装 .dmg 文件

5.验证安装：
```bash
# 检查 Docker 版本
docker --version

# 运行测试容器
docker run hello-world
```
6.确保 Docker 服务正在运行：
```bash
# 检查 Docker 服务状态
docker ps
```







## 3. 使用方法

### 3.1 在Claude桌面客户端中使用

在你的`claude_desktop_config.json`中添加以下配置：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "REDDIT_CLIENT_ID=你的client_id",
        "-e", "REDDIT_CLIENT_SECRET=你的client_secret",
        "-e", "REDDIT_USER_AGENT=你的user_agent",
        "ghcr.io/nangeplus/mcp-reddit:latest"
      ]
    }
  }
}
```

### 3.2 可用工具

1. **search_subreddit**: 搜索特定subreddit中的帖子
   - 参数：
     - `subreddit`: subreddit名称
     - `query`: 搜索关键词
     - `limit`: 最大返回结果数（默认：5）

2. **get_post_details**: 获取特定帖子的详细信息
   - 参数：
     - `post_id`: Reddit帖子ID
     - `comment_limit`: 获取评论的最大数量（默认：10）

3. **get_subreddit_hot**: 获取subreddit中的热门帖子
   - 参数：
     - `subreddit`: subreddit名称
     - `limit`: 返回帖子的最大数量（默认：5）

### 3.3 使用示例

在Claude中，你可以这样使用工具：

```json
{
  "tool": "get_subreddit_hot",
  "arguments": {
    "subreddit": "Python",
    "limit": 3
  }
}
```

**示例对话：**

用户：帮我查看Python subreddit中最热门的3个帖子。

Claude：好的，我来帮你查看。我将使用`get_subreddit_hot`工具：

```json
{
  "tool": "get_subreddit_hot",
  "arguments": {
    "subreddit": "Python",
    "limit": 3
  }
}
```

[Claude会返回帖子信息]

用户：帮我查看第一个帖子的详细内容和评论。

Claude：我将使用`get_post_details`工具：

```json
{
  "tool": "get_post_details",
  "arguments": {
    "post_id": "返回的帖子ID"
  }
}
```

## 4. 本地开发

### 4.1 克隆仓库

```bash
git clone https://github.com/nangeplus/mcp-reddit.git
cd mcp-reddit
```

### 4.2 安装依赖

```bash
pip install -r requirements.txt
```

### 4.3 运行服务器

```bash
python src/server.py
```

### 4.4 Docker构建

```bash
docker build -t mcp-reddit .
docker run -i --rm \
  -e REDDIT_CLIENT_ID=你的client_id \
  -e REDDIT_CLIENT_SECRET=你的client_secret \
  -e REDDIT_USER_AGENT=你的user_agent \
  mcp-reddit
```

## 5. 注意事项

1. **安全性**
   - 请妥善保管你的Reddit API凭证
   - 不要在公共场合分享你的配置文件
   - 建议使用环境变量而不是硬编码凭证

2. **使用限制**
   - Reddit API有调用频率限制
   - 默认返回的评论数量限制为10条
   - 搜索结果默认限制为5条

3. **故障排除**
   - 检查API凭证是否正确
   - 确保网络连接正常
   - 查看日志输出了解详细错误信息

## 6. 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 7. 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---
