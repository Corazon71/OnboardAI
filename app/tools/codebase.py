import requests
from typing import Optional
from langchain.tools import tool
from pydantic import BaseModel, Field
from app.core.config import settings

# 1. Define Input Schema
class GitHubSearchInput(BaseModel):
    query: str = Field(..., description="The keyword to search for in the GitHub repository (e.g., 'auth', 'database connection', 'UserSchema').")

# 2. Define the Tool
@tool(args_schema=GitHubSearchInput)
def search_codebase(query: str) -> str:
    """
    Searches the LIVE GitHub repository for code files matching the query.
    Returns a list of file paths and URLs where the code is located.
    """
    try:
        print(f" Agent is searching GitHub for: '{query}'...")
        
        # Construct the API URL
        base_url = "https://api.github.com/search/code"
        search_query = f"{query} repo:{settings.GITHUB_REPO_OWNER}/{settings.GITHUB_REPO_NAME}"
        params = {"q": search_query, "per_page": 5} # Limit to top 5 results
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

        # Make the request
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                return f"No results found in the repo for '{query}'."
            
            # Format the output for the LLM
            formatted_results = []
            for item in items:
                file_path = item['path']
                html_url = item['html_url']
                formatted_results.append(f"- File: {file_path}\n  Link: {html_url}")
            
            return "\n".join(formatted_results)
        
        elif response.status_code == 403:
            return "Error: GitHub API Rate Limit Exceeded. Please try again later or add a GITHUB_TOKEN."
        else:
            return f"Error searching GitHub: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred during GitHub search: {str(e)}"