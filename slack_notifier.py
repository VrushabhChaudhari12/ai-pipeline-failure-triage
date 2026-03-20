"""
Slack Notifier - Formats and prints triage results in Slack-style output
"""

from datetime import datetime


def post_to_slack(triage_result, pipeline_name):
    """
    Print a formatted Slack-style message to console.

    Args:
        triage_result: Dictionary with fields: PIPELINE, PHASE, WHAT, WHY, FIX, RERUN
        pipeline_name: Name of the pipeline or project
    """
    rerun_value = triage_result.get("RERUN", "NO").strip().upper()

    # Determine header style based on RERUN value
    if rerun_value == "YES":
        header_color = ":white_check_mark:"
        header_text = "BUILD FAILURE - CAN RERUN"
        header_color_ansi = "\033[92m"  # Green
        reset_ansi = "\033[0m"
    else:
        header_color = ":x:"
        header_color_ansi = "\033[91m"  # Red
        header_text = "BUILD FAILURE - FIX REQUIRED"
        reset_ansi = "\033[0m"

    # Header
    header = "=" * 60
    print(header)
    print(f"{header_color_ansi} {header_color} {header_text} {header_color}{reset_ansi}")
    print(header)

    # Divider
    divider = "-" * 60
    print(divider)

    # Pipeline info
    print(f"*Pipeline:* {pipeline_name}")
    print(f"*Project:* {triage_result.get('PIPELINE', 'N/A')}")
    print(divider)

    # Triage fields
    print(f"*PHASE:* {triage_result.get('PHASE', 'N/A')}")
    print(f"*WHAT:* {triage_result.get('WHAT', 'N/A')}")
    print(f"*WHY:* {triage_result.get('WHY', 'N/A')}")
    print(f"*FIX:* {triage_result.get('FIX', 'N/A')}")
    print(f"*RERUN:* {rerun_value}")

    # Footer with timestamp
    print(divider)
    footer = "=" * 60
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f" _Triage completed at {timestamp}_ ")
    print(footer)
    print()