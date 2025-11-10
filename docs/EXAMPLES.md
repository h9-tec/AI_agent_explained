# Real-World Examples: From Concept to Code

**The Philosophy:** Learn by seeing complete, working examples. Each example builds on the modules you've learned.

**By Hesham Haroon**

---

## Example 1: Personal Research Assistant

**Uses:** Module 0 (loop), Module 1 (tools), Module 2 (memory), Module 3 (ReAct)

**The Problem:** You need to research topics and maintain context across multiple questions.

```python
from llm_client import UnifiedClient
from config import config

client = UnifiedClient()

class ResearchAssistant:
    """
    A research assistant that can search, remember context,
    and reason through multi-step queries.
    """
    
    def __init__(self):
        self.memory = []
        self.sources = []
    
    def search(self, query: str) -> str:
        """Mock search - replace with real API."""
        # In production: use Google Custom Search, Bing, or Wikipedia API
        knowledge = {
            "python history": "Python was created by Guido van Rossum in 1991...",
            "machine learning": "Machine learning is a subset of AI that...",
            "neural networks": "Neural networks are computing systems inspired by..."
        }
        
        for key, value in knowledge.items():
            if key in query.lower():
                self.sources.append(f"Source: {key}")
                return value
        
        return f"No information found for: {query}"
    
    def ask(self, question: str) -> str:
        """
        Answer a question using search and reasoning.
        """
        # Add to memory
        self.memory.append({"role": "user", "content": question})
        
        # System prompt
        system = """You are a research assistant. You can search for information.
        When you need information, say: SEARCH: <query>
        When you have enough information, provide your answer.
        Always cite your sources."""
        
        messages = [{"role": "system", "content": system}] + self.memory
        
        # ReAct loop
        for i in range(5):
            response = client.chat.completions.create(
                model="",
                messages=messages
            )
            
            content = response.choices[0].message.content
            
            # Check for search request
            if "SEARCH:" in content:
                query = content.split("SEARCH:")[1].strip()
                print(f"[Searching: {query}]")
                
                result = self.search(query)
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"Search result: {result}"})
            else:
                # Final answer
                self.memory.append({"role": "assistant", "content": content})
                return content
        
        return "Could not find answer within iteration limit."
    
    def summarize_conversation(self) -> str:
        """Summarize the research session."""
        summary_prompt = f"""Summarize this research session:
        
        {self.memory}
        
        Include:
        - Questions asked
        - Key findings
        - Sources used: {self.sources}
        """
        
        response = client.chat.completions.create(
            model="",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        
        return response.choices[0].message.content

# Usage
if __name__ == "__main__":
    assistant = ResearchAssistant()
    
    print(assistant.ask("What is Python?"))
    print(assistant.ask("When was it created?"))
    print(assistant.ask("Summarize what we discussed"))
    
    print("\n" + "="*60)
    print("SESSION SUMMARY")
    print("="*60)
    print(assistant.summarize_conversation())
```

---

## Example 2: Code Review Agent

**Uses:** Module 1 (tools), Module 3 (ReAct reasoning)

**The Problem:** You need automated code review with explanations.

```python
import ast
import re

class CodeReviewAgent:
    """
    Reviews Python code for bugs, style issues, and improvements.
    """
    
    def __init__(self):
        self.client = UnifiedClient()
        self.issues = []
    
    def read_file(self, filepath: str) -> str:
        """Read a Python file."""
        with open(filepath) as f:
            return f.read()
    
    def check_syntax(self, code: str) -> list:
        """Check for syntax errors."""
        try:
            ast.parse(code)
            return []
        except SyntaxError as e:
            return [f"Syntax error at line {e.lineno}: {e.msg}"]
    
    def check_style(self, code: str) -> list:
        """Check for style issues."""
        issues = []
        
        # Check line length
        for i, line in enumerate(code.split('\n'), 1):
            if len(line) > 100:
                issues.append(f"Line {i}: Line too long ({len(line)} chars)")
        
        # Check for TODO comments
        for i, line in enumerate(code.split('\n'), 1):
            if 'TODO' in line:
                issues.append(f"Line {i}: TODO comment found")
        
        # Check for print statements (should use logging)
        for i, line in enumerate(code.split('\n'), 1):
            if re.search(r'\bprint\(', line) and not line.strip().startswith('#'):
                issues.append(f"Line {i}: Use logging instead of print")
        
        return issues
    
    def check_security(self, code: str) -> list:
        """Check for security issues."""
        issues = []
        
        # Check for eval/exec
        if 'eval(' in code or 'exec(' in code:
            issues.append("Security: Avoid eval() and exec() - code injection risk")
        
        # Check for hardcoded secrets
        if re.search(r'(password|secret|key)\s*=\s*["\']', code, re.I):
            issues.append("Security: Possible hardcoded secret")
        
        # Check for SQL injection
        if re.search(r'execute\([^?]*%s', code):
            issues.append("Security: Possible SQL injection vulnerability")
        
        return issues
    
    def suggest_improvements(self, code: str) -> str:
        """Use LLM to suggest improvements."""
        prompt = f"""Review this Python code and suggest improvements:

```python
{code}
```

Focus on:
1. Code quality and readability
2. Performance optimizations
3. Best practices
4. Potential bugs

Be specific and provide examples."""
        
        response = self.client.chat.completions.create(
            model="",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def review(self, filepath: str) -> dict:
        """Complete code review."""
        print(f"Reviewing {filepath}...")
        
        code = self.read_file(filepath)
        
        review = {
            "file": filepath,
            "syntax_errors": self.check_syntax(code),
            "style_issues": self.check_style(code),
            "security_issues": self.check_security(code),
            "suggestions": self.suggest_improvements(code)
        }
        
        return review
    
    def print_review(self, review: dict):
        """Print formatted review."""
        print("\n" + "="*80)
        print(f"CODE REVIEW: {review['file']}")
        print("="*80)
        
        if review['syntax_errors']:
            print("\n❌ SYNTAX ERRORS:")
            for error in review['syntax_errors']:
                print(f"  - {error}")
        else:
            print("\n✓ No syntax errors")
        
        if review['style_issues']:
            print("\n⚠️  STYLE ISSUES:")
            for issue in review['style_issues']:
                print(f"  - {issue}")
        else:
            print("\n✓ No style issues")
        
        if review['security_issues']:
            print("\n🔒 SECURITY ISSUES:")
            for issue in review['security_issues']:
                print(f"  - {issue}")
        else:
            print("\n✓ No security issues")
        
        print("\n💡 SUGGESTIONS:")
        print(review['suggestions'])

# Usage
if __name__ == "__main__":
    reviewer = CodeReviewAgent()
    
    # Review a file
    review = reviewer.review("module_0_agent.py")
    reviewer.print_review(review)
```

---

## Example 3: Data Analysis Agent

**Uses:** Module 1 (tools), Module 3 (ReAct)

**The Problem:** Analyze CSV data and generate insights.

```python
import pandas as pd
import matplotlib.pyplot as plt

class DataAnalysisAgent:
    """
    Analyzes data and generates insights.
    """
    
    def __init__(self):
        self.client = UnifiedClient()
        self.df = None
    
    def load_data(self, filepath: str) -> str:
        """Load CSV data."""
        self.df = pd.read_csv(filepath)
        return f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns"
    
    def describe_data(self) -> str:
        """Get data description."""
        if self.df is None:
            return "No data loaded"
        
        return str(self.df.describe())
    
    def get_columns(self) -> str:
        """Get column names."""
        if self.df is None:
            return "No data loaded"
        
        return ", ".join(self.df.columns)
    
    def calculate(self, expression: str) -> str:
        """Calculate statistics."""
        try:
            # Safe eval with only df available
            result = eval(expression, {"df": self.df, "pd": pd})
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    
    def visualize(self, column: str, chart_type: str = "hist") -> str:
        """Create visualization."""
        if self.df is None:
            return "No data loaded"
        
        try:
            if chart_type == "hist":
                self.df[column].hist()
            elif chart_type == "box":
                self.df.boxplot(column=column)
            
            plt.title(f"{column} - {chart_type}")
            plt.savefig(f"{column}_{chart_type}.png")
            plt.close()
            
            return f"Saved {column}_{chart_type}.png"
        except Exception as e:
            return f"Error: {e}"
    
    def analyze(self, question: str) -> str:
        """
        Answer questions about the data using ReAct.
        """
        tools_desc = """Available tools:
        - describe_data(): Get statistical summary
        - get_columns(): List all columns
        - calculate(expression): Calculate using pandas (e.g., "df['column'].mean()")
        - visualize(column, chart_type): Create chart (hist or box)
        
        Use tools to answer the question step by step."""
        
        messages = [
            {"role": "system", "content": f"You are a data analyst. {tools_desc}"},
            {"role": "user", "content": question}
        ]
        
        for i in range(10):
            response = self.client.chat.completions.create(
                model="",
                messages=messages
            )
            
            content = response.choices[0].message.content
            print(f"\n[Agent]: {content}\n")
            
            # Parse tool calls
            if "describe_data()" in content:
                result = self.describe_data()
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"Result: {result}"})
            
            elif "get_columns()" in content:
                result = self.get_columns()
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"Result: {result}"})
            
            elif "calculate(" in content:
                expr = content.split("calculate(")[1].split(")")[0].strip('"\'')
                result = self.calculate(expr)
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"Result: {result}"})
            
            elif "visualize(" in content:
                # Parse visualize call
                args = content.split("visualize(")[1].split(")")[0]
                parts = [p.strip().strip('"\'') for p in args.split(",")]
                column = parts[0]
                chart_type = parts[1] if len(parts) > 1 else "hist"
                
                result = self.visualize(column, chart_type)
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"Result: {result}"})
            
            else:
                # Final answer
                return content
        
        return "Analysis incomplete"

# Usage
if __name__ == "__main__":
    agent = DataAnalysisAgent()
    
    # Load data
    print(agent.load_data("sales_data.csv"))
    
    # Analyze
    print(agent.analyze("What is the average sales amount? Create a histogram."))
    print(agent.analyze("Which product has the highest sales?"))
```

---

## Example 4: Customer Support Bot

**Uses:** Module 2 (memory), Module 3 (ReAct)

**The Problem:** Handle customer inquiries with context.

```python
class SupportBot:
    """
    Customer support bot with memory and escalation.
    """
    
    def __init__(self):
        self.client = UnifiedClient()
        self.memory = []
        self.customer_info = {}
        self.escalated = False
    
    def get_faq_answer(self, question: str) -> str:
        """Search FAQ database."""
        faqs = {
            "reset password": "To reset your password, click 'Forgot Password' on the login page...",
            "refund": "Refunds are processed within 5-7 business days...",
            "shipping": "Standard shipping takes 3-5 business days...",
            "cancel order": "To cancel an order, go to Orders > Select Order > Cancel..."
        }
        
        question_lower = question.lower()
        for key, answer in faqs.items():
            if key in question_lower:
                return answer
        
        return None
    
    def get_order_status(self, order_id: str) -> str:
        """Mock order lookup."""
        # In production: query database
        orders = {
            "12345": "Shipped - Arriving tomorrow",
            "67890": "Processing - Ships in 2 days"
        }
        
        return orders.get(order_id, "Order not found")
    
    def should_escalate(self, conversation: list) -> bool:
        """Determine if conversation should be escalated."""
        # Escalate if:
        # - Customer is frustrated (multiple negative messages)
        # - Complex technical issue
        # - Request for manager
        
        negative_count = 0
        for msg in conversation:
            if msg['role'] == 'user':
                content_lower = msg['content'].lower()
                if any(word in content_lower for word in ['frustrated', 'angry', 'terrible', 'worst']):
                    negative_count += 1
                if 'manager' in content_lower or 'supervisor' in content_lower:
                    return True
        
        return negative_count >= 2
    
    def chat(self, message: str) -> str:
        """Handle customer message."""
        # Add to memory
        self.memory.append({"role": "user", "content": message})
        
        # Check for escalation
        if self.should_escalate(self.memory):
            self.escalated = True
            return "I understand your frustration. Let me connect you with a supervisor who can better assist you."
        
        # Try FAQ first
        faq_answer = self.get_faq_answer(message)
        if faq_answer:
            self.memory.append({"role": "assistant", "content": faq_answer})
            return faq_answer
        
        # Use LLM for complex queries
        system = """You are a helpful customer support agent for TechStore.
        Be polite, professional, and empathetic.
        If you need to check order status, say: CHECK_ORDER: <order_id>
        If you can't help, say: ESCALATE"""
        
        messages = [{"role": "system", "content": system}] + self.memory
        
        response = self.client.chat.completions.create(
            model="",
            messages=messages
        )
        
        content = response.choices[0].message.content
        
        # Handle special commands
        if "CHECK_ORDER:" in content:
            order_id = content.split("CHECK_ORDER:")[1].strip()
            status = self.get_order_status(order_id)
            content = f"I checked your order #{order_id}. Status: {status}"
        
        elif "ESCALATE" in content:
            self.escalated = True
            content = "Let me transfer you to a specialist who can better assist you."
        
        self.memory.append({"role": "assistant", "content": content})
        return content

# Usage
if __name__ == "__main__":
    bot = SupportBot()
    
    print("Customer Support Bot (type 'quit' to exit)\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = bot.chat(user_input)
        print(f"Bot: {response}\n")
        
        if bot.escalated:
            print("[System: Conversation escalated to human agent]")
            break
```

---

## Example 5: Content Generation Pipeline

**Uses:** Module 4 (CrewAI multi-agent)

**The Problem:** Generate high-quality content with multiple review stages.

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool

@tool("Research Tool")
def research(topic: str) -> str:
    """Research a topic."""
    # Mock - replace with real research
    return f"Research findings about {topic}..."

@tool("SEO Tool")
def seo_analysis(content: str) -> str:
    """Analyze SEO of content."""
    # Mock - replace with real SEO analysis
    word_count = len(content.split())
    return f"Word count: {word_count}. Add more keywords for better SEO."

class ContentPipeline:
    """
    Multi-agent content generation pipeline.
    """
    
    def __init__(self):
        # Define agents
        self.researcher = Agent(
            role="Content Researcher",
            goal="Find accurate, relevant information",
            backstory="You are a thorough researcher who verifies facts.",
            tools=[research],
            verbose=True
        )
        
        self.writer = Agent(
            role="Content Writer",
            goal="Write engaging, clear content",
            backstory="You are a skilled writer who explains complex topics simply.",
            tools=[],
            verbose=True
        )
        
        self.seo_specialist = Agent(
            role="SEO Specialist",
            goal="Optimize content for search engines",
            backstory="You know how to make content rank well.",
            tools=[seo_analysis],
            verbose=True
        )
        
        self.editor = Agent(
            role="Editor",
            goal="Ensure content quality and accuracy",
            backstory="You have a keen eye for errors and improvements.",
            tools=[],
            verbose=True
        )
    
    def generate_article(self, topic: str) -> str:
        """Generate a complete article."""
        
        # Define tasks
        research_task = Task(
            description=f"Research {topic} thoroughly. Find key facts, statistics, and examples.",
            agent=self.researcher,
            expected_output="Comprehensive research notes"
        )
        
        writing_task = Task(
            description=f"Write a 500-word article about {topic} using the research.",
            agent=self.writer,
            expected_output="Draft article"
        )
        
        seo_task = Task(
            description="Optimize the article for SEO. Add keywords naturally.",
            agent=self.seo_specialist,
            expected_output="SEO-optimized article"
        )
        
        editing_task = Task(
            description="Edit the article for clarity, grammar, and flow.",
            agent=self.editor,
            expected_output="Final polished article"
        )
        
        # Create crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.seo_specialist, self.editor],
            tasks=[research_task, writing_task, seo_task, editing_task],
            process=Process.sequential,
            verbose=2
        )
        
        # Generate
        result = crew.kickoff()
        return result

# Usage
if __name__ == "__main__":
    pipeline = ContentPipeline()
    article = pipeline.generate_article("AI Agents in 2024")
    
    print("\n" + "="*80)
    print("FINAL ARTICLE")
    print("="*80)
    print(article)
```

---

## Key Takeaways

1. **Start with the problem** - Understand what you're solving
2. **Build incrementally** - Add features one at a time
3. **Test thoroughly** - Use real examples
4. **Handle errors** - Things will go wrong
5. **Log everything** - You need to debug

**Next Steps:**
1. Run these examples
2. Modify them for your use case
3. Combine patterns from multiple examples
4. Build something new!

Happy coding! 🚀

