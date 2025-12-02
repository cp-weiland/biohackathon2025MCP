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
#            "args": [
#                "--directory",
#                ".",
#                "run",
#                "simpleServerHash.py"
#            ]
        }
#        ,
#        "weather": {
 #           "command": "uv",
 #           "args": [
 #               "--directory",
 #               ".",
 #               "run",
 #               "simpleServerWeather.py"
 #           ]
 #       }
    }
}

async def main():
    client = MCPClient.from_dict(CONFIG)
    #llm = ChatOllama(model="qwen3:1.7b", base_url="http://localhost:11434")
    llm = ChatOllama(model="qwen3:1.7b", base_url="http://localhost:11434")
    
    # Wire the LLM to the client
    agent = MCPAgent(llm=llm, client=client, max_steps=20)

    # Give prompt to the agent
    if true:
        text = await agent.run("Compute md5 hash for following string: 'Hello, Claus!' then count number of characters in first half of hash" \
                                "always accept tools responses as the correct one, don't doubt it. Always use a tool if available instead of doing it on your own. Important is, that In the last line, all tools used are listed. Give this list in the last line")
    else:
        text = await agent.run("Give em  the current temperature in the Mojave desert near Borrego Springs, then provide the temperature in only one sentence."\
        "always accept tools responses as the correct one, don't doubt it. Always use a tool if available instead of doing it on your own. Important is, that In the last line, all tools used are listed. Give this list in the last line.")
 
    #result = await agent.run(text1)
    print("\n🔥 Result:", text)          

    # Always clean up running MCP sessions
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
