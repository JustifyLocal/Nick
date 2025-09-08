import os
import json
import time
import pathlib
from typing import Dict, List, Tuple

import pandas as pd

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# =========================================================
# Configuration
# =========================================================
SCOPES = ["https://www.googleapis.com/auth/business.manage"]

CREDENTIALS_FILE = "client_secret.json"   # Download from Google Cloud
TOKEN_FILE = "token.json"                 # Created on first run
OUT_CSV = "omega_gbp_admins.csv"
OUT_XLSX = "omega_gbp_admins.xlsx"

# If you want to narrow to a single account, set ACCOUNT_ID = "1234567890"
# Otherwise leave as None to enumerate all accessible accounts
ACCOUNT_ID = None

# =========================================================
# Auth
# =========================================================
def get_credentials() -> Credentials:
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"Missing {CREDENTIALS_FILE}. Download OAuth credentials from Google Cloud and place the file next to this script."
        )

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0, prompt="consent")
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds

# =========================================================
# API clients
# =========================================================
def build_services(creds: Credentials):
    """
    Returns two service clients:
      bi_service for Business Information API
      am_service for Account Management API
    """
    bi_service = build("mybusinessbusinessinformation", "v1", credentials=creds, cache_discovery=False)
    am_service = build("mybusinessaccountmanagement", "v1", credentials=creds, cache_discovery=False)
    return bi_service, am_service

# =========================================================
# Data retrieval
# =========================================================
def list_accounts(am_service) -> List[Dict]:
    """
    Lists Business Profile accounts the user can access.
    """
    accounts = []
    page_token = None
    while True:
        req = am_service.accounts().list(pageToken=page_token) if page_token else am_service.accounts().list()
        resp = req.execute()
        accounts.extend(resp.get("accounts", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return accounts

def list_locations_for_account(bi_service, account_name: str) -> List[Dict]:
    """
    account_name should be like 'accounts/1234567890'
    Returns a list of location objects. Uses pagination.
    """
    locations = []
    page_token = None

    while True:
        req = bi_service.accounts().locations().list(
            parent=account_name,
            pageToken=page_token,
            readMask="name,title,storeCode,languageCode,metadata"
        )
        resp = req.execute()
        locations.extend(resp.get("locations", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return locations

def list_admins_for_location(am_service, account_name: str, location_name_only: str) -> List[Dict]:
    """
    location_name_only will look like 'locations/9876543210' from the Business Information API.
    The Account Management API expects 'accounts/{accountId}/locations/{locationId}' as the parent.
    """
    parent = f"{account_name}/{location_name_only}"  # accounts/123/locations/456
    admins = []
    page_token = None

    while True:
        # The locations().admins().list supports pagination in newer responses.
        req = am_service.accounts().locations().admins().list(
            parent=parent,
            pageToken=page_token
        ) if page_token else am_service.accounts().locations().admins().list(parent=parent)

        resp = req.execute()
        admins.extend(resp.get("admins", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return admins

# =========================================================
# Utility
# =========================================================
def extract_office_label(loc: Dict) -> str:
    """
    Best effort to produce a readable office label.
    Preference order: title, storeCode, name suffix.
    """
    title = loc.get("title")
    if title:
        return title
    store = loc.get("storeCode")
    if store:
        return store
    # Fallback to trailing part of locations/{id}
    name = loc.get("name", "")
    return name.split("/")[-1] if name else "Unknown Location"

def normalize_admin_row(account_name: str, location_obj: Dict, admin_obj: Dict) -> Dict:
    """
    Creates a tidy row for export.
    """
    location_name_only = location_obj.get("name", "locations/unknown").split("/")[-1]
    location_full_name = f"{account_name}/locations/{location_name_only}"
    office = extract_office_label(location_obj)

    # Admin fields can include user or name strings depending on Google response
    # Typical fields: admin.name, admin.account, admin.admin, admin.role, admin.state
    role = admin_obj.get("role", "")
    state = admin_obj.get("state", "")
    # admin.user can contain 'name' and 'email'
    user_info = admin_obj.get("user", {})
    person_name = user_info.get("name", "")
    email = user_info.get("email", "")

    return {
        "Office Location": office,
        "Location ID": location_full_name,
        "Name": person_name,
        "Email": email,
        "Role": role,
        "Status": state,
        "Notes": ""
    }

# =========================================================
# Main run
# =========================================================
def main():
    creds = get_credentials()
    bi_service, am_service = build_services(creds)

    rows = []
    errors = []

    try:
        if ACCOUNT_ID:
            accounts = [{"name": f"accounts/{ACCOUNT_ID}"}]
        else:
            accounts = list_accounts(am_service)

        if not accounts:
            print("No Business Profile accounts found for this user.")
            return

        for acct in accounts:
            account_name = acct.get("name")
            if not account_name:
                continue

            locations = list_locations_for_account(bi_service, account_name)
            print(f"Found {len(locations)} locations under {account_name}")

            for loc in locations:
                try:
                    loc_name_only = loc.get("name", "locations/unknown")
                    # Keep only the 'locations/{id}' piece if full path leaked in
                    if "/" in loc_name_only and not loc_name_only.startswith("locations/"):
                        loc_name_only = "/".join(loc_name_only.split("/")[-2:]) if "locations/" in loc_name_only else loc_name_only
                        # Expect loc_name_only like 'locations/{id}'

                    admins = list_admins_for_location(am_service, account_name, loc_name_only)
                    if not admins:
                        # Record a location with no admins, which should not happen for a valid location
                        rows.append({
                            "Office Location": extract_office_label(loc),
                            "Location ID": f"{account_name}/{loc_name_only}",
                            "Name": "",
                            "Email": "",
                            "Role": "",
                            "Status": "NO_ADMINS_FOUND",
                            "Notes": ""
                        })
                        continue

                    for adm in admins:
                        rows.append(normalize_admin_row(account_name, loc, adm))

                except HttpError as e:
                    errors.append((loc.get("name", "unknown"), e._get_reason()))
                except Exception as ex:
                    errors.append((loc.get("name", "unknown"), str(ex)))

        # Export
        df = pd.DataFrame(rows, columns=["Office Location", "Location ID", "Name", "Email", "Role", "Status", "Notes"])
        df.sort_values(by=["Office Location", "Email", "Role"], inplace=True)
        df.to_csv(OUT_CSV, index=False)
        try:
            df.to_excel(OUT_XLSX, index=False)
        except Exception as ex:
            print(f"Excel export skipped: {ex}")

        print(f"\nExport complete.")
        print(f"CSV:  {pathlib.Path(OUT_CSV).resolve()}")
        if os.path.exists(OUT_XLSX):
            print(f"XLSX: {pathlib.Path(OUT_XLSX).resolve()}")

        if errors:
            print("\nSome locations returned errors. Summary:")
            for name, msg in errors:
                print(f"  - {name}: {msg}")

    except HttpError as e:
        print(f"HTTP error: {e._get_reason()}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

if __name__ == "__main__":
    main()