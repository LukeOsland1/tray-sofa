# macOS SOFA Feed - Date Adjuster

Automatically fetches and adjusts dates in the macOS SOFA data feed for patch management workflows.

## Overview

This repository contains a GitHub Actions workflow that:
1. Fetches the latest macOS data feed from [macadmins/sofa](https://github.com/macadmins/sofa)
2. Adjusts release dates by adding 24 hours
3. Preserves original dates for releases with actively exploited CVEs
4. Commits the adjusted feed to this repository

This is useful for patch management systems that need a grace period before enforcing updates, while maintaining urgency for actively exploited vulnerabilities.

## Workflow

### Date Adjustment Workflow

**Schedule:**
- Runs daily at 3 AM UTC
- Can be manually triggered from the Actions tab

**Process:**
1. Downloads the latest `macos_data_feed.json` from macadmins/sofa
2. Processes all date fields (ReleaseDate, PostingDate, ExpirationDate)
3. Adds 24 hours to dates where `ActivelyExploitedCVEs` is empty
4. Preserves original dates where `ActivelyExploitedCVEs` contains items
5. Commits the adjusted feed to the repository

**Output:**
- `adjusted-times/macos_data_feed.json` - The adjusted feed file

### Date Adjustment Logic

```python
if ActivelyExploitedCVEs array is empty or doesn't exist:
    → Add 24 hours to all dates

if ActivelyExploitedCVEs contains items:
    → Preserve original dates (no delay for actively exploited vulnerabilities)
```

## Usage

### Accessing the Adjusted Feed

The adjusted feed is available at:
```
https://raw.githubusercontent.com/LukeOsland1/tray-sofa/main/adjusted-times/macos_data_feed.json
```

Or via GitHub Pages (if enabled):
```
https://lukeosland1.github.io/tray-sofa/adjusted-times/macos_data_feed.json
```

### Manual Trigger

1. Go to the [Actions tab](../../actions)
2. Select "Adjust macOS Data Feed Dates"
3. Click "Run workflow"
4. Click the green "Run workflow" button

## Files

- `adjust_dates.py` - Python script that performs the date adjustment
- `.github/workflows/adjust-dates.yml` - GitHub Actions workflow configuration
- `adjusted-times/macos_data_feed.json` - The adjusted feed (updated daily)

## Example

**Original date:**
```json
{
  "ProductVersion": "15.0",
  "ReleaseDate": "2025-09-29T00:00:00Z",
  "ActivelyExploitedCVEs": []
}
```

**Adjusted date (no exploited CVEs):**
```json
{
  "ProductVersion": "15.0",
  "ReleaseDate": "2025-09-30T00:00:00Z",
  "ActivelyExploitedCVEs": []
}
```

**Preserved date (has exploited CVEs):**
```json
{
  "ProductVersion": "14.7.1",
  "ReleaseDate": "2025-09-20T00:00:00Z",
  "ActivelyExploitedCVEs": ["CVE-2024-12345"]
}
```

## Credits

This project uses data from the [macadmins/sofa](https://github.com/macadmins/sofa) project.

## License

See LICENSE file for details.
