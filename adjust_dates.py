"""
Adjust dates in macOS data feed by adding 24 hours to dates
unless ActivelyExploitedCVEs contains items.
"""

import json
import sys
from datetime import datetime, timedelta


def adjust_date(date_str: str) -> str:
    """Add 24 hours to an ISO 8601 date string."""
    if not date_str or date_str == "Unknown":
        return date_str

    try:
        # Parse ISO 8601 date
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        # Add 24 hours
        dt_adjusted = dt + timedelta(hours=24)
        # Return in ISO 8601 format
        return dt_adjusted.strftime('%Y-%m-%dT%H:%M:%SZ')
    except (ValueError, AttributeError):
        # If parsing fails, return original
        return date_str


def should_adjust_dates(item: dict) -> bool:
    """
    Check if dates should be adjusted for this item.
    Returns True if ActivelyExploitedCVEs is empty or doesn't exist.
    Returns False if ActivelyExploitedCVEs contains items.
    """
    actively_exploited = item.get('ActivelyExploitedCVEs', [])

    # If the field exists and has items, don't adjust dates
    if actively_exploited and len(actively_exploited) > 0:
        return False

    # Otherwise, adjust dates
    return True


def adjust_dates_in_dict(data: dict, parent_key: str = "") -> dict:
    """
    Recursively process a dictionary and adjust dates based on ActivelyExploitedCVEs.
    """
    # Check if this dict should have its dates adjusted
    adjust = should_adjust_dates(data)

    # List of date fields to potentially adjust
    date_fields = ['ReleaseDate', 'PostingDate', 'ExpirationDate']

    # Process each key in the dictionary
    for key, value in data.items():
        if key in date_fields and adjust:
            # Adjust this date field
            data[key] = adjust_date(value)
        elif isinstance(value, dict):
            # Recursively process nested dictionaries
            data[key] = adjust_dates_in_dict(value, key)
        elif isinstance(value, list):
            # Process each item in the list
            data[key] = [
                adjust_dates_in_dict(item, key) if isinstance(item, dict) else item
                for item in value
            ]

    return data


def process_feed(input_file: str, output_file: str):
    """Load, process, and save the macOS data feed."""
    try:
        # Load the JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Loaded {input_file}")

        # Process the data
        adjusted_data = adjust_dates_in_dict(data)

        # Save the adjusted data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(adjusted_data, f, indent=4, ensure_ascii=False)

        print(f"Saved adjusted data to {output_file}")
        print("Date adjustment complete!")

    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "macos_data_feed_adjusted.json"
    else:
        input_file = "macos_data_feed.json"
        output_file = "macos_data_feed_adjusted.json"

    process_feed(input_file, output_file)
