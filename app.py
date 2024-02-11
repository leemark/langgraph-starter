# conda activate langgraph-start
# pip install langchain langgraph langchain-openai langsmith langchainhub duckduckgo-search beautifulsoup4 gradio python-dotenv
import functools, os, operator, requests, json
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

#tools
@tool('search_web', return_direct=False)
def search_web(query: str)-> str:
   """Searches the web using DuckDuckGo.""" 
   with DDGS() as ddgs:
       results = [r for r in ddgs.text(query, max_results=5)]
       return results if results else "No results found."
   
   @tool('process_content', return_direct=False)
   def process_content(url: str)-> str:
       """Processes the content of a webpage."""
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'html.parser')
       return soup.get_text()
   
   tools = [search_web, process_content]

#agents
def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

#agent nodes
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

#agent supervisor
members = ["Web_Searcher", "Insight_Researcher"]
system_prompt = (
    "As a supervisor, your role is to oversee a dialogue between these"
    " workers: {members}. Based on the user's request,"
    " determine which worker should take the next action." 
    " Each worker is responsible for executing a specific task"
    " and reporting back their findings and progress." 
    " Once all tasks are complete,"
    " indicate that with 'FINISH'."
)



#ref https://www.youtube.com/watch?v=v9fkbTxPzs0