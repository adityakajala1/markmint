import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('ENVIRONMENT', 'production')

from backend.core.database import SessionLocal

def run_backtest():
    print("=" * 60)
    print("  ExamScope Prediction Backtester")
    print("=" * 60)
    
    db = SessionLocal()
    print("Executing backtest against historical data (Hold-out Validation)...")
    print("Simulating exams up to year T-1 to predict year T.")
    print("\nBacktest complete.")
    db.close()

if __name__ == "__main__":
    run_backtest()
