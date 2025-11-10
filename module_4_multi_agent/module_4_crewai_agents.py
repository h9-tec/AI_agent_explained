# Module 4: Multi-Agent Orchestration with CrewAI
# This module introduces the CrewAI framework for building collaborative multi-agent systems.

"""
CrewAI is a framework for orchestrating role-playing AI agents.
It allows you to create a "crew" of agents, each with specific roles, goals, and tools,
that work together to accomplish complex tasks.

Key Concepts:
- Agent: An AI entity with a specific role, goal, and backstory
- Task: A specific job to be done by an agent
- Crew: A collection of agents working together
- Process: How tasks are executed (sequential, hierarchical, etc.)
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from typing import List
import os

# Import our unified LLM client
from llm_client import get_llm_client
from config import config


# Define custom tools using CrewAI's @tool decorator
@tool("Search Tool")
def search_tool(query: str) -> str:
    """
    Searches for information on a given query.
    Useful for finding facts, news, and general information.
    """
    # Mock search implementation
    knowledge_base = {
        "python": "Python is a high-level programming language created by Guido van Rossum in 1991. It emphasizes code readability and simplicity.",
        "ai agents": "AI agents are autonomous systems that can perceive their environment, make decisions, and take actions to achieve specific goals.",
        "crewai": "CrewAI is a framework for orchestrating role-playing AI agents that work together as a crew to accomplish complex tasks.",
        "llama": "LLaMA (Large Language Model Meta AI) is a family of large language models released by Meta AI, designed to be efficient and accessible.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    
    return f"General information about {query}: This is a topic worth exploring further."


@tool("Calculator Tool")
def calculator_tool(expression: str) -> str:
    """
    Evaluates mathematical expressions.
    Useful for performing calculations and solving math problems.
    """
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


@tool("Writing Tool")
def writing_tool(content: str) -> str:
    """
    Helps with writing and editing content.
    Useful for improving text quality and structure.
    """
    # Simple mock implementation
    word_count = len(content.split())
    return f"Content analyzed: {word_count} words. The content is well-structured and clear."


def create_research_crew() -> Crew:
    """
    Creates a research crew with multiple specialized agents.
    
    This crew consists of:
    - A researcher who gathers information
    - An analyst who processes the information
    - A writer who creates the final report
    """
    
    # Define the Researcher Agent
    researcher = Agent(
        role="Senior Researcher",
        goal="Gather comprehensive and accurate information on assigned topics",
        backstory="""You are an experienced researcher with a keen eye for detail.
        You excel at finding relevant information and verifying facts.
        You always cite your sources and present information objectively.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Define the Analyst Agent
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze information and extract key insights",
        backstory="""You are a skilled analyst who can identify patterns and draw 
        meaningful conclusions from data. You think critically and provide 
        evidence-based recommendations.""",
        tools=[calculator_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Define the Writer Agent
    writer = Agent(
        role="Technical Writer",
        goal="Create clear, engaging, and well-structured reports",
        backstory="""You are a talented writer who can transform complex information 
        into accessible content. You have a gift for explaining technical concepts 
        in simple terms while maintaining accuracy.""",
        tools=[writing_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Define Tasks
    research_task = Task(
        description="""Research the topic: {topic}
        
        Gather comprehensive information including:
        - Key facts and definitions
        - Historical context
        - Current state and trends
        - Important considerations
        
        Provide a detailed summary of your findings.""",
        agent=researcher,
        expected_output="A comprehensive research summary with key facts and context"
    )
    
    analysis_task = Task(
        description="""Analyze the research findings on: {topic}
        
        Based on the research, provide:
        - Key insights and patterns
        - Important implications
        - Potential applications
        - Recommendations
        
        Your analysis should be data-driven and objective.""",
        agent=analyst,
        expected_output="A detailed analysis with insights and recommendations"
    )
    
    writing_task = Task(
        description="""Create a final report on: {topic}
        
        Synthesize the research and analysis into a well-structured report that includes:
        - Executive summary
        - Main findings
        - Analysis and insights
        - Conclusions and recommendations
        
        The report should be clear, concise, and professionally written.""",
        agent=writer,
        expected_output="A polished final report suitable for presentation"
    )
    
    # Create the Crew
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,  # Tasks executed in order
        verbose=2  # Maximum verbosity for learning purposes
    )
    
    return crew


def create_coding_crew() -> Crew:
    """
    Creates a software development crew.
    
    This crew consists of:
    - A software architect who designs solutions
    - A developer who implements code
    - A QA engineer who tests and validates
    """
    
    architect = Agent(
        role="Software Architect",
        goal="Design robust and scalable software solutions",
        backstory="""You are a senior software architect with years of experience 
        in system design. You excel at breaking down complex problems and 
        designing elegant solutions.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    developer = Agent(
        role="Senior Developer",
        goal="Write clean, efficient, and well-documented code",
        backstory="""You are an expert programmer who writes production-quality code.
        You follow best practices and always consider maintainability.""",
        tools=[calculator_tool],
        verbose=True,
        allow_delegation=False
    )
    
    qa_engineer = Agent(
        role="QA Engineer",
        goal="Ensure code quality and identify potential issues",
        backstory="""You are a meticulous QA engineer who catches bugs before 
        they reach production. You think about edge cases and potential failures.""",
        tools=[],
        verbose=True,
        allow_delegation=False
    )
    
    # Define Tasks
    design_task = Task(
        description="""Design a solution for: {problem}
        
        Provide:
        - High-level architecture
        - Key components and their responsibilities
        - Data flow and interactions
        - Technology recommendations
        
        Focus on scalability and maintainability.""",
        agent=architect,
        expected_output="A detailed system design document"
    )
    
    implementation_task = Task(
        description="""Implement the designed solution for: {problem}
        
        Create:
        - Core implementation outline
        - Key functions and classes
        - Error handling approach
        - Documentation
        
        Follow best practices and coding standards.""",
        agent=developer,
        expected_output="Implementation plan with code structure"
    )
    
    testing_task = Task(
        description="""Review and test the solution for: {problem}
        
        Provide:
        - Test strategy
        - Key test cases
        - Potential issues and edge cases
        - Quality assessment
        
        Be thorough and think about failure scenarios.""",
        agent=qa_engineer,
        expected_output="Comprehensive test plan and quality report"
    )
    
    crew = Crew(
        agents=[architect, developer, qa_engineer],
        tasks=[design_task, implementation_task, testing_task],
        process=Process.sequential,
        verbose=2
    )
    
    return crew


def run_research_example():
    """Run a research crew example."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Research Crew")
    print("=" * 80 + "\n")
    
    crew = create_research_crew()
    
    # Run the crew with a specific topic
    result = crew.kickoff(inputs={"topic": "AI Agents and their applications"})
    
    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print(result)


def run_coding_example():
    """Run a software development crew example."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Software Development Crew")
    print("=" * 80 + "\n")
    
    crew = create_coding_crew()
    
    # Run the crew with a specific problem
    result = crew.kickoff(inputs={
        "problem": "Build a rate limiter for an API that prevents abuse while allowing legitimate traffic"
    })
    
    print("\n" + "=" * 80)
    print("FINAL DELIVERABLE")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    # Validate configuration
    try:
        config.validate()
        config.print_config()
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nNote: CrewAI works best with OpenAI models, but can be adapted for llama.cpp")
        print("For best results with llama.cpp, use models with strong instruction-following capabilities")
        exit(1)
    
    print("\n" + "=" * 80)
    print("Module 4: Multi-Agent Orchestration with CrewAI")
    print("=" * 80)
    print("\nCrewAI allows you to create teams of AI agents that collaborate")
    print("to solve complex problems. Each agent has a specific role and expertise.\n")
    
    # Run examples
    try:
        # Example 1: Research Crew
        run_research_example()
        
        print("\n\n")
        input("Press Enter to continue to the next example...")
        
        # Example 2: Coding Crew
        run_coding_example()
        
    except Exception as e:
        print(f"\n✗ Error running CrewAI examples: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you have installed: pip install crewai crewai-tools")
        print("2. If using llama.cpp, ensure your model supports instruction following")
        print("3. Check that your API keys are properly configured")
        import traceback
        traceback.print_exc()

