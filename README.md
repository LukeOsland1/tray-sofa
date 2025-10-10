# SOFA Feed Builder

Automated Apple software update feed generator that runs on GitHub Actions.

## Overview

This project builds feeds for macOS and iOS software updates, including security releases, XProtect updates, and compatible devices.

## Setup

### Required Files

Before running the script, ensure you have these files in place:

1. **config.json** - Configuration specifying which OS versions to track
2. **AppleRoot.pem** - Apple's root certificate for SSL verification
   - Download from: https://www.apple.com/certificateauthority/
3. **process_ipsw.py** - IPSW processing module
4. **process_uma.py** - UMA (macOS installer) processing module
5. **model_identifier_*.json** - macOS model compatibility data:
   - model_identifier_tahoe.json (macOS 26)
   - model_identifier_sequoia.json (macOS 15)
   - model_identifier_sonoma.json (macOS 14)
   - model_identifier_ventura.json (macOS 13)
   - model_identifier_monterey.json (macOS 12)
6. **cache/supported_devices.json** - Device support mapping

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create the cache directory:
   ```bash
   mkdir -p cache
   ```

3. Run the script:
   ```bash
   python sofa-feed.py macOS iOS
   ```

## GitHub Actions

### SOFA Feed Builder Workflow

Runs automatically:
- **Daily at 2 AM UTC** - Automatic updates
- **Manual trigger** - Run from Actions tab with custom OS types

Manual trigger steps:
1. Go to your repository's Actions tab
2. Select "SOFA Feed Builder"
3. Click "Run workflow"
4. Optionally specify OS types (default: "macOS iOS")

Generated files:
- `macos_data_feed.json` - Complete macOS update data
- `ios_data_feed.json` - Complete iOS update data
- `rss_feed.xml` - RSS feed with all updates
- `timestamp.json` - Last update timestamps
- `cache/` - Cached data to minimize API calls

### Date Adjustment Workflow

Runs automatically:
- **Daily at 3 AM UTC** - After the SOFA feed builder
- **Manual trigger** - Run from Actions tab

This workflow:
1. Fetches the latest macOS data feed from [macadmins/sofa](https://github.com/macadmins/sofa)
2. Adds 24 hours to all dates EXCEPT for releases with actively exploited CVEs
3. Commits the adjusted feed as `macos_data_feed.json` to the repository

Generated file:
- `macos_data_feed.json` - Adjusted feed (replaces previous version each run)

**Date Adjustment Logic:**
- If `ActivelyExploitedCVEs` array is empty or doesn't exist → adds 24 hours
- If `ActivelyExploitedCVEs` contains items → preserves original dates

## Output

The script generates:
- JSON feeds with version information
- RSS feed for notifications
- Security release tracking with CVE data
- Compatible device lists
- XProtect version tracking (macOS only)

## Configuration

Edit `config.json` to specify which OS versions to track:

```json
{
  "softwareReleases": [
    {"osType": "macOS", "name": "Sequoia 15"},
    {"osType": "macOS", "name": "Sonoma 14"},
    {"osType": "iOS", "name": "18"}
  ]
}
```

## License

See LICENSE file for details.
