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

