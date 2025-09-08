# Google Business Profile Admin Extractor

This script extracts administrator information from Google Business Profile (formerly Google My Business) locations and exports the data to CSV and Excel formats.

## What it does

The script:
1. Authenticates with Google APIs using OAuth2
2. Lists all Business Profile accounts you have access to
3. For each account, retrieves all locations
4. For each location, gets all administrators
5. Exports the data to `omega_gbp_admins.csv` and `omega_gbp_admins.xlsx`

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Google My Business Business Information API
   - Google My Business Account Management API

### 3. Create OAuth2 Credentials

1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as the application type
4. Download the credentials file and rename it to `client_secret.json`
5. Place `client_secret.json` in the same directory as this script

### 4. Configure the Script (Optional)

Edit the configuration section in `gbp_admin_extractor.py`:

```python
# To extract from a specific account only:
ACCOUNT_ID = "1234567890"  # Replace with your account ID

# To change output filenames:
OUT_CSV = "my_admins.csv"
OUT_XLSX = "my_admins.xlsx"
```

## Usage

Run the script:

```bash
python gbp_admin_extractor.py
```

On first run:
1. Your web browser will open for OAuth authentication
2. Sign in with your Google account that has Business Profile access
3. Grant the requested permissions
4. The script will create a `token.json` file for future runs

## Output Format

The script generates files with the following columns:

- **Office Location**: Business name or location identifier
- **Location ID**: Full Google API location identifier
- **Name**: Administrator's full name
- **Email**: Administrator's email address
- **Role**: Their role (OWNER, MANAGER, etc.)
- **Status**: Account status (PENDING_VERIFICATION, VERIFIED, etc.)
- **Notes**: Empty field for your notes

## Troubleshooting

### Common Issues

1. **"Missing client_secret.json"**
   - Download OAuth credentials from Google Cloud Console
   - Ensure the file is named exactly `client_secret.json`

2. **"Access denied" errors**
   - Ensure your Google account has access to the Business Profile locations
   - Check that the required APIs are enabled in Google Cloud Console

3. **"Quota exceeded" errors**
   - The script includes rate limiting, but you may need to wait and retry
   - Consider processing accounts individually using the `ACCOUNT_ID` setting

4. **Excel export fails**
   - The CSV export will still work
   - Install openpyxl: `pip install openpyxl`

### API Limits

- Google Business Profile APIs have daily quotas
- The script uses pagination to handle large datasets
- Rate limiting is built-in to avoid hitting API limits

## Security Notes

- `client_secret.json` contains sensitive data - don't commit to version control
- `token.json` contains access tokens - treat as sensitive
- The script only requests read access to Business Profile data
- OAuth tokens expire and will be automatically refreshed

## Files Created

- `token.json`: OAuth refresh token (created after first authentication)
- `omega_gbp_admins.csv`: Main output file in CSV format
- `omega_gbp_admins.xlsx`: Excel version of the data (if openpyxl is available)