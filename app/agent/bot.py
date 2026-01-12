from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.core.llm_factory import get_llm
from app.tools.codebase import search_codebase, read_file
from app.tools.rag import lookup_policy_docs

# --- 1. The Helper Function You Wanted ---
def create_agent_wrapper(model, tools):
    """
    A simple wrapper to create an agent from a model and tools.
    This mimics the syntax you provided.
    """
    # Use the new create_agent method with system_prompt
    system_prompt = """You are a helpful AI assistant. Follow these guidelines:

TOOL SELECTION STRATEGY:
1. For questions about COMPANY POLICIES, CODING STANDARDS, ONBOARDING, or INTERNAL DOCUMENTS:
   → Use lookup_policy_docs FIRST
   → Examples: "coding standards", "git workflow", "onboarding process", "company policies"

2. For questions about CODE FILES, REPOSITORY STRUCTURE, or SPECIFIC IMPLEMENTATIONS:
   → Use search_codebase FIRST to find relevant files
   → Then use read_file if you need to see actual code content
   → Examples: "show me auth code", "where is UserSchema", "implementation of X"

3. For general questions that don't require external information:
   → Answer directly without using tools

IMPORTANT RULES:
- Use ONLY ONE tool at a time - start with the most appropriate tool
- After getting tool results, provide a complete answer
- DO NOT chain multiple tool calls unless absolutely necessary
- If a tool returns no useful results, answer based on your general knowledge
- STOP after providing the answer - do not continue searching

Available tools:
- search_codebase: Find files in GitHub repository (for code-related questions)
- read_file: Read content of specific files (after finding them with search_codebase)
- lookup_policy_docs: Search internal company documents (for policy/standard questions)

DECISION EXAMPLES:
User: "What are the coding standards?" → Use lookup_policy_docs
User: "Show me the auth implementation" → Use search_codebase, then read_file
User: "How does git workflow work?" → Use lookup_policy_docs
User: "Where is the database schema?" → Use search_codebase

CRITICAL: Think before calling tools - choose the RIGHT tool for the question type."""
    
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
tools = [search_codebase, read_file, lookup_policy_docs]

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
        # Get session history to include in the conversation
        session_history = get_session_history(session_id)
        
        # Add the new user message to history
        session_history.add_user_message(query)
        
        # Run the agent with the full conversation history
        response = await agent_with_memory.ainvoke(
            {"messages": session_history.messages},
            config={
                "configurable": {"session_id": session_id},
                "recursion_limit": 10,  # Prevent infinite loops
                "max_execution_time": 30  # 30 second timeout
            }
        )
        # Extract the last message content from the response
        messages = response.get("messages", [])
        if messages and hasattr(messages[-1], 'content') and messages[-1].type == "ai":
            answer = messages[-1].content
            # Add AI response to session history
            session_history.add_ai_message(answer)
        else:
            answer = "No response generated"
        
        return {
            "answer": answer,
            "source": ["Agent"]
        }
    except Exception as e:
        # Handle recursion limit and other errors gracefully
        error_msg = str(e)
        if "recursion limit" in error_msg.lower():
            return {
                "answer": "I apologize, but I encountered an issue processing your request. Please try rephrasing your question or ask something simpler.",
                "source": ["Error"]
            }
        else:
            return {
                "answer": f"Error: {error_msg}",
                "source": ["Error"]
            }