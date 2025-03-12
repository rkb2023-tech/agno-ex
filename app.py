import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
# from agno.models.groq import GroqChat
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools


# Streamlit UI
st.title("Web & Finance Agent App")
st.write("This app searches the web and retrieves financial data based on your query.")

# Sidebar for API Configuration
st.sidebar.header("Configuration")
mode = st.sidebar.selectbox("Select Mode", ["GROQ", "OPENAI"], index=1)
api_key = st.sidebar.text_input("Enter API Key", type="password")

if api_key:
    # Choose model based on user selection
    if mode == "OPENAI":
        model = OpenAIChat(id="gpt-4o", api_key=api_key)
    else:
        model = Groq(id="llama3-8b-8192", api_key=api_key)
    
    # Initialize Web Agent
    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions="Always include sources",
        show_tool_calls=True,
        markdown=True,
    )

    # Initialize Finance Agent
    finance_agent = Agent(
        name="Finance Agent",
        role="Get financial data",
        model=model,
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
        instructions="Use tables to display data",
        show_tool_calls=True,
        markdown=True,
    )

    # Create an Agent Team
    agent_team = Agent(
        team=[web_agent, finance_agent],
        model=model,
        instructions=["Always include sources", "Use tables to display data"],
        show_tool_calls=True,
        markdown=True,
    )

    query = st.text_input("Enter your query:", "What's the market outlook and financial performance of AI semiconductor companies?")

    if st.button("Get Insights"):
        with st.spinner("Fetching data..."):
            response = agent_team.run(query)
            st.markdown(response.get_content_as_string())
else:
    st.warning("Please enter an API Key to proceed.")