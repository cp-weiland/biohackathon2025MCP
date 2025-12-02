import asyncio
import os
from langchain_ollama.chat_models import ChatOllama
from mcp_use import MCPAgent, MCPClient

# Get the server script path (same directory as this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "simpleServerHash.py")
#server_path = os.path.join(current_dir, "simpleServerWeather.py")

# Describe which MCP servers you want.

CONFIG = {
    "mcpServers": {
        "hash": {
            "command": "uv",
            "args": ["run", server_path]
        },
        "weather": {
            "command": "uv",
            "args": [
                "--directory",
                ".",
                "run",
                "simpleServerWeather.py"
            ]
        }
    }
}

async def main():
    client = MCPClient.from_dict(CONFIG)
    llm = ChatOllama(model="qwen3:1.7b", base_url="http://localhost:11434")
    
    # Wire the LLM to the client
    agent = MCPAgent(llm=llm, client=client, max_steps=20)

    # Give prompt to the agent
    text1 = "Compute md5 hash for following string: 'Hello, Claus!' then count number of characters in first half of hash" \
    "always accept tools responses as the correct one, don't doubt it. Always use a tool if available instead of doing it on your own. Important is, that In the last line, all tools used are listed. Give this list in the last line"
    
    text2 = "What is the current wind chill in the Mojave desert near Borrego Springs, reply in one brief sentence, don't tell me or investigate anything else, always accept tools responses as the correct one, don't doubt it. Always u\
se a tool if available instead of doing it on your own. List all tools used, provide this list in the last line"

    result = await agent.run(text1)
    print("\n🔥 Result:", result)          

    # Always clean up running MCP sessions
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
