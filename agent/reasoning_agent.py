from crewai import Agent, Task, Crew
try:
    from crewai.tools import tool
except ImportError:
    from langchain.tools import tool
from langchain_openai import ChatOpenAI  
import os

# openai api key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Initialize LLM 
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

class RebalancingCrew:
    def __init__(self):
        # Defining agents
        self.analyst_agent = Agent(
            role="Portfolio Analyst",
            goal="Analyze portfolio allocation, identify overweights, underweights, and drifts.",
            backstory="You are a seasoned financial analyst specializing in portfolio drift detection. You excel at comparing current vs. target allocations.",
            llm=llm,
            verbose=True
        )

        self.reasoner_agent = Agent(
            role="Rebalancing Reasoner",
            goal="Decide on rebalancing actions based on rules and analysis.",
            backstory="You are an expert advisor who applies rebalancing rules to recommend buys/sells and explain necessity.",
            llm=llm,
            verbose=True
        )

        self.explainer_agent = Agent(
            role="Decision Explainer",
            goal="Simplify rebalancing decisions for investors.",
            backstory="You translate complex financial advice into clear, friendly language for everyday investors.",
            llm=llm,
            verbose=True
        )

    def create_tasks(self, portfolio_summary: str, rules: str):
        # Task 1: Analyze Portfolio
        analyze_task = Task(
            description=f"Analyze the portfolio for overweights, underweights, and drifts. Portfolio Data: {portfolio_summary}",
            agent=self.analyst_agent,
            expected_output="A summary of overweights, underweights, and drifts."
        )

        # Task 2: Reason Rebalancing- depends on analysis
        reason_task = Task(
            description=f"Using rules: {rules}, decide on assets to reduce/increase and why rebalancing is needed. Portfolio: {portfolio_summary}",
            agent=self.reasoner_agent,
            expected_output="Recommendations for buys/sells and rationale.",
            # Passes output from analyze_task
            context=[analyze_task]  
        )

        # Task 3: Explain Decision (reasoning)
        explain_task = Task(
            description="Explain the rebalancing decision in simple, investor-friendly language.",
            agent=self.explainer_agent,
            expected_output="A clear, simple explanation of the decision.",
            # Passes output from reason_task
            context=[reason_task]  
        )

        return [analyze_task, reason_task, explain_task]

    def run_crew(self, portfolio_df, rules_text: str):
        portfolio_summary = portfolio_df.to_string(index=False)
        tasks = self.create_tasks(portfolio_summary, rules_text)

        crew = Crew(
            agents=[self.analyst_agent, self.reasoner_agent, self.explainer_agent],
            tasks=tasks,
            verbose=True 
        )

        result = crew.kickoff()
        return {
            "analysis": result.tasks_output[0].raw,  
            "decision": result.tasks_output[1].raw, 
            "explanation": result.tasks_output[2].raw 
        }