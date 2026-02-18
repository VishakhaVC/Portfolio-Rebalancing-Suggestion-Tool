# basic imports for app
from agent.analyzer import PortfolioAnalyzer
from agent.reasoning_agent import RebalancingCrew  # Updated import

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def run_app(data=None):
    analyzer = PortfolioAnalyzer(data if data is not None else "data/portfolio.csv")
    analysis_result = analyzer.analyze()

    rules = load_text("knowledge_base/rebalancing_rules.txt")

    # crew ai instead of RebalancingAgent
    crew = RebalancingCrew()
    output = crew.run_crew(
        analysis_result["portfolio_table"],
        rules
    )

    return {
        "portfolio": analysis_result["portfolio_table"],
        "analysis": output["analysis"],
        "decision": output["decision"],
        "explanation": output["explanation"]
    }

if __name__ == "__main__":
    result = run_app()

    print("\nPORTFOLIO ANALYSIS:\n")
    print(result["analysis"])

    print("\nREBALANCING DECISION:\n")
    print(result["decision"])

    print("\nFINAL EXPLANATION:\n")
    print(result["explanation"])