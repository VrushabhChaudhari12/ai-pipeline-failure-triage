"""
AI Pipeline Failure Triage - Main entry point

Runs all four CodeBuild failure scenarios and prints formatted triage results.
"""

from mock_build_logs import get_build_log
from triage import triage_failure
from slack_notifier import post_to_slack


# Define the scenarios to run
SCENARIOS = [
    ("unit_test_failure", "payment-service-build"),
    ("dependency_error", "frontend-app-pipeline"),
    ("docker_build_failure", "containerized-api-build"),
    ("iam_permission_error", "prod-deployment-pipeline"),
]


def run_scenario(scenario_name, pipeline_name):
    """
    Run a single scenario: get build logs, triage, and post to Slack.

    Args:
        scenario_name: The scenario key
        pipeline_name: Name of the pipeline/project
    """
    # Print scenario name
    print(f"\n{'='*60}")
    print(f"  SCENARIO: {scenario_name.upper()}")
    print(f"{'='*60}\n")

    # Get build logs
    logs = get_build_log(scenario_name)

    # Triage the failure
    result = triage_failure(logs, pipeline_name)

    # Post to Slack
    post_to_slack(result, pipeline_name)

    # Add separator between scenarios
    print("\n" + "=" * 60 + "\n")


def main():
    """Run all scenarios sequentially."""
    print("\n" + "=" * 60)
    print("  AI PIPELINE FAILURE TRIAGE")
    print("=" * 60 + "\n")

    for scenario_name, pipeline_name in SCENARIOS:
        run_scenario(scenario_name, pipeline_name)

    print("\nAll scenarios completed.")


if __name__ == "__main__":
    main()