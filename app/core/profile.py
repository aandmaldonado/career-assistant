import yaml
from pathlib import Path
from app.core.models import Portfolio

DATA_DIR = Path(__file__).parent.parent.parent / "data"
portfolio_path = DATA_DIR / "portfolio.yaml"

def load_portfolio() -> Portfolio:
    """Loads the portfolio from the YAML file."""
    if not portfolio_path.exists():
        raise FileNotFoundError(f"Portfolio not found at {portfolio_path}")
    
    with open(portfolio_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    return Portfolio(**data)

if __name__ == "__main__":
    # Test execution
    try:
        p = load_portfolio()
        print(f"Successfully loaded portfolio for {p.personal_info.name}")
    except Exception as e:
        print(f"Error loading portfolio: {e}")
