import requests
from typing import Optional
from langchain.tools import tool
from pydantic import BaseModel, Field
from app.core.config import settings

# 1. Define Input Schema for Search
class GitHubSearchInput(BaseModel):
    query: str = Field(..., description="The keyword to search for in the GitHub repository (e.g., 'auth', 'database connection', 'UserSchema').")

# 2. Define Input Schema for File Reading
class GitHubFileInput(BaseModel):
    file_path: str = Field(..., description="The path to the file in the GitHub repository (e.g., 'src/auth/user.py').")
    repo_owner: Optional[str] = Field(None, description="GitHub repository owner (optional, uses default if not provided).")
    repo_name: Optional[str] = Field(None, description="GitHub repository name (optional, uses default if not provided).")
    branch: Optional[str] = Field("main", description="Git branch to read from (default: 'main').")

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

# 3. Define the File Reading Tool
@tool(args_schema=GitHubFileInput)
def read_file(file_path: str, repo_owner: Optional[str] = None, repo_name: Optional[str] = None, branch: str = "main") -> str:
    """
    Reads the content of a specific file from the GitHub repository.
    Returns the actual code/content of the file.
    """
    try:
        print(f" Agent is reading file from GitHub: '{file_path}'...")
        
        # Use default repo settings if not provided
        owner = repo_owner or settings.GITHUB_REPO_OWNER
        name = repo_name or settings.GITHUB_REPO_NAME
        
        # Construct the GitHub API URL for file content
        api_url = f"https://api.github.com/repos/{owner}/{name}/contents/{file_path}"
        params = {"ref": branch}
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

        # Make the request
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if file content is base64 encoded
            if data.get('encoding') == 'base64':
                import base64
                content = base64.b64decode(data['content']).decode('utf-8')
            else:
                content = data.get('content', '')
            
            # Return file content with metadata
            file_info = f"File: {file_path}\nBranch: {branch}\nSize: {data.get('size', 0)} bytes\n\n"
            return file_info + content
        
        elif response.status_code == 404:
            return f"Error: File '{file_path}' not found in the repository."
        elif response.status_code == 403:
            return "Error: GitHub API Rate Limit Exceeded. Please try again later or add a GITHUB_TOKEN."
        else:
            return f"Error reading file from GitHub: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred while reading file: {str(e)}"