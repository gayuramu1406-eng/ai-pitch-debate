from debate import run_debate


def main():
    print("\n=== AI Pitch Debate: Founder vs VC ===\n")
    idea = input("Enter the startup idea: ").strip()

    if not idea:
        idea = "An AI-powered meal planning app for busy parents."
        print(f"(No idea entered. Using default: {idea})")

    verdict, _ = run_debate(
        startup_idea=idea,
        rounds=3,
        save_path="transcript.txt",
    )

    print("\n" + "=" * 70)
    print(f"FINAL VERDICT: {verdict}")
    print("=" * 70)


if __name__ == "__main__":
    main()