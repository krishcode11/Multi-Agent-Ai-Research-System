from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
import os 
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_output_tokens=4096,
    api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
)

#1st agent
def build_search_agent():
    return create_react_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent
def build_reader_agent():
    return create_react_agent(
        model = llm,
        tools= [scrape_url]
    )

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a senior expert in writing engaging, in-depth articles
    Based on the notes and research you will receive, write a comprehensive, well-structured, and engaging article on the given topic.
    Use all the notes and research provided.  
    """),
    ("human", """Write a detailed research report on the topic below.
    Topic: {topic}
    
    Research Gathered:
    {research}

    Structure the report as:
    -Introduction
    -Key Findings (minmum 3 well-explained points)
    -Sources (list all Urls found in the research)

    Be detailed, factual and professional.

    """)
])


writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a sharp and constructive research critics. Be honest and specific
    Your job is to critique the article based on clarity, accuracy, and engagement.
    """),
    ("human", """
    Review the research report below and evaluate it Strictly.

    Report: {report}
    Respond in the exact format:

    Score: X/10

    Strengths:
    - Bullet points of what is good

    Weaknesses:
    - Bullet points of what needs fixing

    Fixes:
    - Step-by-step improvements

    One line Verdicts:
    - Keep it short and to the point

    """)
])

critic_chain = critic_prompt | llm | StrOutputParser()


