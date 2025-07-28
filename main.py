import os
import sys

def run_reddit_analyzer():
    reddit_path = os.path.join(os.path.dirname(__file__), 'reddit')
    sys.path.insert(0, reddit_path)
    try:
        import main as reddit_main
        reddit_main.main()
    except Exception as e:
        print(f"❌ Error running Reddit Persona Analyzer: {e}")
    finally:
        sys.path.pop(0)  # Clean up import path

def run_github_analyzer():
    github_path = os.path.join(os.path.dirname(__file__), 'github')
    sys.path.insert(0, github_path)
    try:
        import main as github_main
        github_main.main()
    except Exception as e:
        print(f"❌ Error running GitHub Profile Analyzer: {e}")
    finally:
        sys.path.pop(0)  # Clean up import path

def main():
    print("\n📊 Welcome to Combined Insight!")
    print("Choose an analysis module:\n")
    print("1. Reddit Persona Analyzer")
    print("2. GitHub Profile Analyzer")
    
    choice = input("\nEnter your choice (1/2): ").strip()
    
    if choice == "1":
        run_reddit_analyzer()
    elif choice == "2":
        run_github_analyzer()
    else:
        print("❌ Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
