import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool

from .math_tools import calculate_math, solve_equation

load_dotenv()


@tool
def calculate_math_tool(expression: str) -> str:
    """Calculate a mathematical expression using SymPy."""
    try:
        return calculate_math(expression)
    except ValueError as exc:
        return str(exc)


@tool
def solve_equation_tool(equation: str) -> str:
    """Solve an equation like 'x^2 - 4 = 0' for x."""
    try:
        return solve_equation(equation)
    except ValueError as exc:
        return str(exc)


def get_agent() -> AgentExecutor:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI math assistant. Use the available tools to answer mathematical questions."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    tools = [calculate_math_tool, solve_equation_tool]
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)
