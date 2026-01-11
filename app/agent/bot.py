from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.core.llm_factory import get_llm
from app.tools.codebase import search_codebase
from app.tools.rag import lookup_policy_docs

# --- 1. The Helper Function You Wanted ---
def create_agent_wrapper(model, tools):
    """
    A simple wrapper to create an agent from a model and tools.
    This mimics the syntax you provided.
    """
    # Use the new create_agent method with system_prompt
    system_prompt = "You are a helpful AI assistant. Use the provided tools to answer questions."
    
    # Construct the agent using the new create_agent method
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return agent

# --- 2. Setup ---
# Load Model & Tools
model = get_llm(temperature=0)
tools = [search_codebase, lookup_policy_docs]

# Create the Agent using the simple syntax
agent = create_agent_wrapper(model, tools)

# --- 3. Memory & Execution ---
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Wrap with Memory
agent_with_memory = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="messages",
    history_messages_key="chat_history",
)

async def ask_agent(query: str, session_id: str) -> Dict[str, Any]:
    try:
        # Run the agent with new message format
        response = await agent_with_memory.ainvoke(
            {"messages": [{"role": "user", "content": query}]},
            config={"configurable": {"session_id": session_id}}
        )
        # Extract the last message content from the response
        messages = response.get("messages", [])
        if messages and hasattr(messages[-1], 'content') and messages[-1].type == "ai":
            answer = messages[-1].content
        else:
            answer = "No response generated"
        
        return {
            "answer": answer,
            "source": ["Agent"]
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "source": ["Error"]
        }