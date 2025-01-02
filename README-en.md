# MCP Reddit Server

[English](#english) | [中文说明](#README.md)

<h2 id="english">English</h2>

## 1. Project Introduction

This is a Reddit server based on the MCP (Model Context Protocol) protocol, specifically designed to interact with large language models such as Claude. Through this service, you can have AI assistants help you browse and interact with Reddit.

### 1.1 Main Features

- Search posts in specific subreddits
- Get detailed information and comments on posts
- Browse popular posts in subreddits

### 1.2 Project Structure

```
nangeAGICode/reddit_chat_claude/
├── .github/
│   └── workflows/
│       └── docker.yml # GitHub Actions workflow configuration
├── src/
│   ├── init.py
│   └── server.py # Core code of the MCP server
├── .gitignore # Git ignore file configuration
├── Dockerfile # Docker build file
├── LICENSE # MIT license
├── README.md # Project description document
└── requirements.txt # List of Python dependencies
```

## 2. Installation and Configuration

### 2.1 Prerequisites

- Docker (required)
- Python 3.12+ (for local development)
- Reddit API credentials (required)

### 2.2 Obtaining Reddit API Credentials

1. Visit https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Choose "script"
4. Fill in the necessary information
5. Obtain `client_id` and `client_secret`

### 2.3 Environment Variable Configuration

Set the following environment variables:

```bash
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### 2.4 Docker Installation

For Mac users:
1. Visit Docker official website: https://www.docker.com/products/docker-desktop
2. Click "Download for Mac"
3. Choose the version corresponding to your Mac chip (Apple Silicon or Intel)
4. Download and install the .dmg file

5. Verify installation:
```bash
# Check Docker version
docker --version

# Run test container
docker run hello-world
```

6. Ensure Docker service is running:
```bash
# Check Docker service status
docker ps
```

## 3. Usage

### 3.1 Using in Claude Desktop Client

Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "reddit": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "REDDIT_CLIENT_ID=your_client_id",
        "-e", "REDDIT_CLIENT_SECRET=your_client_secret",
        "-e", "REDDIT_USER_AGENT=your_user_agent",
        "ghcr.io/nangeplus/mcp-reddit:latest"
      ]
    }
  }
}
```

### 3.2 Available Tools

1. **search_subreddit**: Search posts in a specific subreddit
   - Parameters:
     - `subreddit`: Name of the subreddit
     - `query`: Search keywords
     - `limit`: Maximum number of results to return (default: 5)

2. **get_post_details**: Get detailed information of a specific post
   - Parameters:
     - `post_id`: Reddit post ID
     - `comment_limit`: Maximum number of comments to retrieve (default: 10)

3. **get_subreddit_hot**: Get popular posts in a subreddit
   - Parameters:
     - `subreddit`: Name of the subreddit
     - `limit`: Maximum number of posts to return (default: 5)

### 3.3 Usage Example

In Claude, you can use the tools like this:

```json
{
  "tool": "get_subreddit_hot",
  "arguments": {
    "subreddit": "Python",
    "limit": 3
  }
}
```

**Example Conversation:**

User: Help me check the top 3 posts in the Python subreddit.

Claude: Sure, I will check for you. I will use the `get_subreddit_hot` tool:

```json
{
  "tool": "get_subreddit_hot",
  "arguments": {
    "subreddit": "Python",
    "limit": 3
  }
}
```

[Claude will return the post information]

User: Help me get the details and comments of the first post.

Claude: I will use the `get_post_details` tool:

```json
{
  "tool": "get_post_details",
  "arguments": {
    "post_id": "returned_post_id"
  }
}
```

## 4. Local Development

### 4.1 Clone the Repository

```bash
git clone https://github.com/nangeplus/mcp-reddit.git
cd mcp-reddit
```

### 4.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4.3 Run the Server

```bash
python src/server.py
```

### 4.4 Docker Build

```bash
docker build -t mcp-reddit .
docker run -i --rm \
  -e REDDIT_CLIENT_ID=your_client_id \
  -e REDDIT_CLIENT_SECRET=your_client_secret \
  -e REDDIT_USER_AGENT=your_user_agent \
  mcp-reddit
```

## 5. Notes

1. **Security**
   - Keep your Reddit API credentials safe
   - Do not share your configuration files in public
   - It is recommended to use environment variables instead of hardcoding credentials

2. **Usage Limitations**
   - Reddit API has rate limits
   - The default number of comments returned is limited to 10
   - The default number of search results is limited to 5

3. **Troubleshooting**
   - Check if the API credentials are correct
   - Ensure network connection is stable
   - Check log output for detailed error information

## 6. Contribution Guidelines

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 7. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
