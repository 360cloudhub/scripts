import datetime
import pandas as pd
import argparse
from googleapiclient import discovery
from google.auth import default
import google.auth
from firebase_admin import auth, credentials, initialize_app

def fetch_identity_platform_users():
    users = auth.list_users().iterate_all()
    user_data = []

    for user in users:
        user_data.append(['', '', user.uid, user.email, user.provider_id, user.display_name])

    return user_data

def fetch_iam_permissions_for_account(account_name):
    credentials, _ = default()

    service = discovery.build('iam', 'v1', credentials=credentials)

    request = service.projects().serviceAccounts().getIamPolicy(resource=account_name)
    response = request.execute()
    policies = response.get('bindings', [])

    table_data = []

    for policy in policies:
        role_name = policy['role']
        for member in policy.get('members', []):
            member_type, member_name = member.split(':')
            if member_type in ["user", "serviceAccount"]:
                table_data.append([account_name, role_name, member_type, member_name])

    return table_data

def fetch_all_iam_permissions(project_id):
    credentials, _ = default()

    service = discovery.build('iam', 'v1', credentials=credentials)

    request = service.projects().serviceAccounts().list(name=f'projects/{project_id}')
    response = request.execute()
    accounts = response.get('accounts', [])
    print(f"Total number of accounts found: {len(accounts)}")
    table_data = []

    for account in accounts:
        account_name = account['name']
        table_data += fetch_iam_permissions_for_account(account_name)
        print(table_data)
    return table_data

def main(project_id):
    iam_table_data = fetch_all_iam_permissions(project_id)
    identity_platform_table_data = fetch_identity_platform_users()

    # Create separate DataFrames for Identity Platform users and IAM/service accounts
    df_identity_platform = pd.DataFrame(identity_platform_table_data, columns=['Account', 'Role', 'UID', 'Email', 'Provider ID', 'Display Name'])
    df_iam_service_accounts = pd.DataFrame(iam_table_data, columns=['Account', 'Role', 'Member Type', 'Member Name'])

    # Set the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Create an Excel file with separate sheets
    excel_filename = f"combined_data_{current_date}.xlsx"
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df_identity_platform.to_excel(writer, sheet_name='Identity Platform Users', index=False)
        df_iam_service_accounts.to_excel(writer, sheet_name='IAM and Service Accounts', index=False)

    print("Data exported successfully to Excel file with separate sheets.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch IAM permissions and Identity Platform users")
    parser.add_argument("--project_id", required=True, help="GCP Project ID")
    args = parser.parse_args()

    cred = credentials.ApplicationDefault()
    initialize_app(cred)

    credentials, _ = google.auth.default()

    main(args.project_id)
