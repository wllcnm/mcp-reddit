import asyncio
import logging
import os
from typing import List
import praw
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("reddit_mcp_server")

class RedditMCPServer:
    def __init__(self):
        self.app = Server("reddit_mcp_server")
        self.setup_tools()

    def get_reddit_client(self):
        # 从环境变量获取凭证
        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        user_agent = os.environ.get("REDDIT_USER_AGENT", "MCP-Reddit/1.0")
        
        if not all([client_id, client_secret]):
            raise ValueError("Missing Reddit API credentials in environment variables")
        
        return praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def setup_tools(self):
        @self.app.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="search_subreddit",
                    description="Search for posts in a specific subreddit",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subreddit": {
                                "type": "string",
                                "description": "Name of the subreddit to search"
                            },
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 5
                            }
                        },
                        "required": ["subreddit", "query"]
                    }
                ),
                Tool(
                    name="get_post_details",
                    description="Get detailed information about a specific Reddit post",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "ID of the Reddit post"
                            },
                            "comment_limit": {
                                "type": "integer",
                                "description": "Maximum number of comments to fetch",
                                "default": 10
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="get_subreddit_hot",
                    description="Get hot posts from a specific subreddit",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subreddit": {
                                "type": "string",
                                "description": "Name of the subreddit"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of posts to return",
                                "default": 5
                            }
                        },
                        "required": ["subreddit"]
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: dict) -> List[TextContent]:
            reddit = self.get_reddit_client()
            
            if name == "search_subreddit":
                subreddit = arguments["subreddit"]
                query = arguments["query"]
                limit = arguments.get("limit", 5)
                
                try:
                    subreddit = reddit.subreddit(subreddit)
                    search_results = subreddit.search(query, limit=limit)
                    
                    results = []
                    for post in search_results:
                        results.append(f"Title: {post.title}\n"
                                     f"ID: {post.id}\n"
                                     f"Score: {post.score}\n"
                                     f"URL: {post.url}\n"
                                     f"Created: {post.created_utc}\n"
                                     f"---")
                    
                    return [TextContent(type="text", text="\n\n".join(results))]
                
                except Exception as e:
                    return [TextContent(type="text", text=f"Error searching subreddit: {str(e)}")]
            
            elif name == "get_post_details":
                post_id = arguments["post_id"]
                comment_limit = arguments.get("comment_limit", 10)
                
                try:
                    post = reddit.submission(id=post_id)
                    post.comments.replace_more(limit=0)
                    
                    post_details = [
                        f"Title: {post.title}",
                        f"Author: {post.author}",
                        f"Score: {post.score}",
                        f"Content: {post.selftext if post.selftext else '[No text content]'}",
                        f"URL: {post.url}",
                        "\nTop Comments:"
                    ]
                    
                    for comment in post.comments[:comment_limit]:
                        post_details.append(
                            f"\nComment by {comment.author} (Score: {comment.score}):"
                            f"\n{comment.body}"
                            f"\n---"
                        )
                    
                    return [TextContent(type="text", text="\n".join(post_details))]
                
                except Exception as e:
                    return [TextContent(type="text", text=f"Error getting post details: {str(e)}")]
            
            elif name == "get_subreddit_hot":
                subreddit = arguments["subreddit"]
                limit = arguments.get("limit", 5)
                
                try:
                    subreddit = reddit.subreddit(subreddit)
                    hot_posts = subreddit.hot(limit=limit)
                    
                    results = []
                    for post in hot_posts:
                        results.append(f"Title: {post.title}\n"
                                     f"ID: {post.id}\n"
                                     f"Score: {post.score}\n"
                                     f"URL: {post.url}\n"
                                     f"Created: {post.created_utc}\n"
                                     f"---")
                    
                    return [TextContent(type="text", text="\n\n".join(results))]
                
                except Exception as e:
                    return [TextContent(type="text", text=f"Error getting hot posts: {str(e)}")]
            
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

    async def run(self):
        logger.info("Starting Reddit MCP server...")
        
        async with stdio_server() as (read_stream, write_stream):
            try:
                await self.app.run(
                    read_stream,
                    write_stream,
                    self.app.create_initialization_options()
                )
            except Exception as e:
                logger.error(f"Server error: {str(e)}", exc_info=True)
                raise

def main():
    server = RedditMCPServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main() 