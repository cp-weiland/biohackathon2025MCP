import asyncio
import os

from loguru import logger

from langchain_ollama.chat_models import ChatOllama
from mcp_use import MCPAgent, MCPClient

# Get the server script path (same directory as this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
hash_server_path = os.path.join(current_dir, "simpleServerHash.py")
weather_server_path = os.path.join(current_dir, "simpleServerWeather.py")
sparql_server_path = os.path.join(current_dir, "simpleServerSPARQL.py")

# Describe which MCP servers you want.

CONFIG = {
    "mcpServers": {
        "hash": {
            "command": "uv",
            "args": ["run", hash_server_path]
        },
        "weather": {
            "command": "uv",
            "args": ["run", weather_server_path]
        },
        "sparql": {
            "command": "uv",
            "args": ["run", sparql_server_path]
        }
    }
}

async def main():
    client = MCPClient.from_dict(CONFIG)
    #llm = ChatOllama(model="qwen3:1.7b", base_url="http://localhost:11434")
    llm = ChatOllama(model="qwen3:1.7b", base_url="http://localhost:11434")
    
    # Wire the LLM to the client
    agent = MCPAgent(llm=llm, client=client, max_steps=20)

    # Give prompt to the agent
    if True:
        text = await agent.run("Compute md5 hash for following string: 'Hello, Claus!' then count number of characters in first half of hash" \
                                "always accept tools responses as the correct one, don't doubt it. Always use a tool if available instead of doing it on your own. Important is, that In the last line, all tools used are listed. Give this list in the last line")
    elif True:
        text = await agent.run("Do a short weather forecast for New York City for tomorrow, be brief, use only 50 vwords. Use your own knowledge to calculate coordinates for New Yoork City."\
                               "always accept tools responses as the correct one, don't doubt it. Always use a tool if available instead of doing it on your own. Important is, that In the last line, all tools used are listed. Give this list in the last line.")
        #text  = await agent.run("List all currently available tools.")
    else:
        text = await agent.run("Query")
        
    print("\n🔥 Result:", text)          

    # Always clean up running MCP sessions
#    await client.close_all_sessions()
        
if __name__ == "__main__":
    asyncio.run(main())
