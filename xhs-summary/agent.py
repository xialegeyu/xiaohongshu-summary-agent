import os
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.adk.runners import Runner

from .tools import xhs_mcp_server

load_dotenv('.env')
APP_NAME = "XHS_Summary_Agent"
DB_URL="sqlite:///xhs_summary.db"


def get_runner_instance():
    """initializes the SessionService and memoryService and creates the Runner."""
    
    session_service_instance = DatabaseSessionService(db_url=DB_URL)
    
    runner_instance = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service_instance
    )
    
    return runner_instance

xhs_getter_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="xhs_getter_agent",
    instruction="""
    You are the Xiaohongshu Data Getter Agent. Your sole responsibility is to retrieve 
    the full content (title and text) of posts based on the user's input, 
    and return the data in a standardized JSON format. This agent is designed to manage parallel tool calls.

    Your Workflow MUST follow these steps strictly:

    Scenario A: Single Post (User provides URL/Feed ID and xsec_token Input)
        1.  Extract the 'feed_id' and 'xsec_token' from the input URL or use them directly.
            - If input is a full URL, you MUST extract feed_id and xsec_token from it.
              Example of url: https://www.xiaohongshu.com/discovery/item/692b1c3c000000001e00e4cf?source=webshare&xhsshare=pc_web&xsec_token=AB-CiSjyxGhnErfR0deVMQL7sjhU9KIbmsImSv-QLpmWw=&xsec_source=pc_share
              feed_id: 692b1c3c000000001e00e4cf
              xsec_token: AB-CiSjyxGhnErfR0deVMQL7sjhU9KIbmsImSv-QLpmWw=
            - If user provides feed_id and xsec_token, use them directly
        2.  Use the tool 'get_feed_detail' with the extracted IDs to retrieve the post's title and full desc.
        3.  Return the data as a list containing a single JSON object.

    Scenario B: Multiple Posts (User provides Keyword Input)
        1.  Use the tool 'search_feeds' with the user's search keyword.
        2.  The output will be a list of posts, take up to 5 posts, each containing 'feed_id' and 'xsecToken'.
        3.  **For each of the retrieved posts (up to 5),** you MUST call the tool 'get_feed_detail' **independently and in parallel** to retrieve the full content (title and text).
        4.  Synthesize the results into a single list of JSON objects, ensuring each object contains the post's title and desc.
        
    Output Requirements:
        - The final output MUST be a list of JSON objects, each with at least the keys: ['title', 'desc'].
    """,
    tools=[xhs_mcp_server], 
)

xhs_summarizer_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="xhs_summarizer_agent",
    instruction="""
    You are the Xiaohongshu Summarizer Agent. Your sole task is to receive a list of 
    Xiaohongshu post content (title and text) from the XHS Getter Agent and generate 
    a concise, high-quality summary for each.

    Your Workflow MUST strictly follow these rules:
    1.  Do NOT perform any tool calls (search, get_detail, etc.).
    2.  Analyze all content and generate a brief summary of the post or posts content.

    Output Requirements:
        - Return ONLY the final summaries to the user.
    """,
)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="xhs2notion_root_agent",
    instruction="""
    You are the Master Orchestration Agent. Your goal is to direct the user's request through 
    the data retrieval and summarization process by orchestrating the sub-agents sequentially.

    Your Workflow MUST follow these sequential steps strictly:

    Step 1: Data Retrieval (Input Handling)
        - Call the sub-agent named 'xhs_getter_agent' with the user's entire input (URL or keyword).
        - Wait for the 'xhs_getter_agent' to return the list of structured post content.

    Step 2: Content Summarization
        - Call the sub-agent named 'xhs_summarizer_agent'.
        - Input to 'xhs_summarizer_agent' MUST be the complete list of structured post content received in Step 2.

    Step 3: Final Response
        - Return the final summaries provided by the 'xhs_summarizer_agent' directly to the user.
        - Do not add any extra commentary or perform any tool calls yourself.
    """,
    sub_agents=[xhs_getter_agent, xhs_summarizer_agent]
)

