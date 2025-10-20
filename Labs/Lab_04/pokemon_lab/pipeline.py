import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    print("Running the full data pipeline...", file=sys.stderr)

    print("Step 1: Making the portfolio file now...", file=sys.stderr)
    update_portfolio.main()

    print("Step 2: Creating the summary report...", file=sys.stderr)
    generate_summary.main()

    print("All done! The pipeline finished successfully.", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
