# xiaohongshu-summary-agent
Capstone project for 5-Day AI Agents Intensive Course with Google, An Orchestrated Multi-Agent System for Parallel Data Retrieval and AI Summarization
## 💡 Problem Statement

Social media platforms like Xiaohongshu contain vast amounts of valuable, specialized content (travel, finance, lifestyle). However, efficiently extracting and synthesizing information from these platforms is challenging due to the need for:

1.  Complex data handling (extracting tokens from URLs).
2.  Executing sequential dependencies (Search $\rightarrow$ Detail Fetch).
3.  Dealing with the low efficiency of **sequentially retrieving the full content** of multiple search results.

This project uses the Google Agent Development Kit (ADK) to solve this problem by automating the complex I/O orchestration and intelligent summarization, transforming a time-consuming research task into a rapid, automated query.

## 🎯 Solution: Why Agents?

Agents are the ideal framework for this solution because they natively handle the required complexity:

* **Sequential Orchestration (A2A Protocol):** The Root Agent manages the strict flow of Data Acquisition $\rightarrow$ Summarization.
* **Parallel Tool Execution:** The LLM is instructed to execute multiple `get_feed_detail` calls concurrently, demonstrating efficient asynchronous I/O management.
* **Specialized LLM Tasking:** Agents are dedicated to specific roles (Getter for I/O, Summarizer for synthesis), leading to highly reliable and modular code.
* **External Tool Integration (MCP):** The system seamlessly integrates the specialized **xiaohongshu-mcp** service via an MCP Toolset to access the necessary data endpoints.

## 🏛️ Architecture Overview

The system employs a three-layered **Sequential Multi-Agent** architecture that manages data flow from external service to final output:

| Agent | Core Responsibility | Subagents/Tools |
| --- | --- |
| Root Agent | Routing Input, Sequential Flow Control. | 2 sub agents |
| XHS Getter Agent | Data I/O Specialist. Handles extraction from URL and orchestrates parallel tool calls. | search_feeds, get_feed_detail (MCP) |
| XHS Summarizer Agent | LLM Specialist. Synthesizes raw content into single-sentence summaries. | None (LLM-powered) |

## 🧱 The Build and Technologies

Core Technologies Used
* Framework: Google Agent Developer Kit (ADK)
* Model: Gemini 2.5 Flash
* Tool Integration: Model Context Protocol (MCP)
* Persistence: DatabaseSessionService (SQLite backend)

Integration Details
* Open Source Acknowledgment: The project's successful data retrieval relies heavily on the xiaohongshu-mcp open-source project. We integrated this specialized service via a dedicated MCP Toolset (xhs_mcp_server), allowing us to focus on the advanced Multi-Agent orchestration rather than complex reverse-engineering.
* Tool Integration: The xhs_mcp_server is configured via StreamableHTTPConnectionParams, connecting to a separately running external service.
* Persistence: DatabaseSessionService is used for state management, ensuring the Agent remembers prior interactions across restarts.
* Architecture Solution (Lazy Initialization): To ensure reliable startup and avoid environment errors (like the ValueError encountered during development), a Lazy Initialization pattern was implemented. The DatabaseSessionService is instantiated safely within the get_runner_instance() function.

## 📝 Example Usage
[user]: search for 首尔新沙洞攻略 and give me a summary
[xhs_summarizer_agent]: Here is a summary of the Xiaohongshu posts regarding "首尔新沙洞攻略":

The posts offer comprehensive guides for exploring Seoul's Sinsa-dong, often combining it with nearby Apgujeong and Seongsu-dong for a full day of activities. Key recommendations across the guides include:

*   **Shopping:** Sinsa-dong is highlighted for its unique fashion boutiques and popular brands like Tamburins, 8 Seconds, Lelabo, Low Classic, Ralph Lauren, Alo, and Ader Error. Apgujeong is also mentioned for shopping, including stores like Atelier Nian, Wiggle Wiggle, and Haus (which features Gentle Monster and Nudake cake). Seongsu-dong is also suggested for shopping.
*   **Food & Drink:** Recommended spots include Vienna Coffee, 신사890 (a high-end Korean-Western bar), 신사花蟹堂 (a famous soy-marinated crab restaurant), 乙支达拉克新沙路 (a retro Japanese curry restaurant), Conte de Tulear (brunch), London Bagel Museum, Camel Coffee, and Gumi Gopchang (a popular grilled beef intestines spot with 9 side dishes). KyoChon Fried Chicken is also mentioned in Seongsu-dong.
*   **Attractions & Photo Spots:** The Jennie poster wall (often found near Tamburins flagship stores in Sinsa-dong and Seongsu-dong) is a must-visit for 
photos. Other places include the SM Entertainment building and Kwangya store in Seoul Forest, and Cube Entertainment in Seongsu-dong.
*   **Logistics & Tips:** Many guides suggest starting from Sinsa Station (Exit 5 or 8) and exploring on foot. Optimal visiting hours are generally 11:00-22:00. Some posts provide detailed walking routes to avoid backtracking and advise checking for Chinese language services and tax refund options with a passport. Accommodation recommendations are also provided for convenient access to Sinsa-dong's nightlife.

## Setup and Instructions

### Prerequisites
* Python 3.10+
* Node.js (for running the external MCP server).
* A dedicated PowerShell/CMD window for running the MCP server.

### Step 1: Install Dependencies
Activate your Python virtual environment and install necessary packages:
``
uv pip install google-agent-adk python-dotenv requests
``

### Step 2: Configure Environment Variables
Create a file named .env in your project root and fill in the necessary secrets and URLs.

``
# Gemini API Key
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

# Xiaohongshu MCP Server Details
# NOTE: The XHS MCP Server MUST be running in a separate window.
XHS_MCP_SERVER_URL="http://localhost:18060" 
XHS_TOKEN="YOUR_XHS_AUTH_TOKEN" 
``

### Step 3: Run the External MCP Server
In a dedicated PowerShell/CMD window, start the xiaohongshu-mcp service (consult the project documentation for the exact command to run the external executable).

### Step 4: Run the Agent
Ensure the MCP server is running and your virtual environment is active. The adk run command will automatically use the get_runner_instance function for startup.

``
adk run xhs_summary.py
``
