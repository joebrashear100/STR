# Microsoft Graph API Test Example - Using Your Real FileLocator ID

## Real Example from Your Data

From your `STRDocumentOneDriveTXT.rtf`, here's an actual file:

```json
{
  "Id": "b!eX1FjKaJQU-O5Lw471RaJzT9GZ9zgDZBmkb14COMSTLGgHJOrHHQSqUln2Es5ASJ.01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC",
  "Name": "0009de35-a0ee-4a6b-be8f-3f138249b829Cypress-Flow.png",
  "FileLocator": "b!eX1FjKaJQU-O5Lw471RaJzT9GZ9zgDZBmkb14COMSTLGgHJOrHHQSqUln2Es5ASJ.01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC",
  "Size": 144762,
  "LastModified": "2025-07-10T13:43:02Z",
  "MediaType": "image/png"
}
```

---

## Test #1: Using Azure CLI (Easiest)

```bash
# Step 1: Login to Azure
az login

# Step 2: Get access token
TOKEN=$(az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv)

# Step 3: Test the API call using the Item ID from "Id" field
ITEM_ID="01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC"

curl -H "Authorization: Bearer $TOKEN" \
     https://graph.microsoft.com/v1.0/me/drive/items/$ITEM_ID

# You'll get back JSON like:
# {
#   "id": "01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC",
#   "name": "0009de35-a0ee-4a6b-be8f-3f138249b829Cypress-Flow.png",
#   "size": 144762,
#   "lastModifiedDateTime": "2025-07-10T13:43:02Z",
#   "webUrl": "https://deltaairlines-my.sharepoint.com/personal/...",
#   ...
# }
```

---

## Test #2: Using Python (No Azure Setup)

```python
import requests
from azure.identity import InteractiveBrowserCredential

# Step 1: Get token (opens browser for login)
credential = InteractiveBrowserCredential(client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46")  # Microsoft Graph CLI ID
token = credential.get_token("https://graph.microsoft.com/.default").token

# Step 2: Make the API call
item_id = "01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC"  # From your FileLocator ID
headers = {"Authorization": f"Bearer {token}"}

url = f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}"
response = requests.get(url, headers=headers)

data = response.json()
print(f"Filename: {data.get('name')}")
print(f"Size: {data.get('size')} bytes")
print(f"Last Modified: {data.get('lastModifiedDateTime')}")
print(f"Web URL: {data.get('webUrl')}")
```

---

## Test #3: Using PowerShell

```powershell
# Step 1: Install module
Install-Module Microsoft.Graph -Scope CurrentUser

# Step 2: Connect
Connect-MgGraph -Scopes "Files.Read.All"

# Step 3: Get the file
$itemId = "01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC"
$file = Get-MgDriveItem -DriveId (Get-MgDrive | Select-Object -First 1).Id -DriveItemId $itemId

$file | Select-Object Name, Size, LastModifiedDateTime, WebUrl
```

---

## Breaking Down the FileLocator ID

Your FileLocator: `b!eX1FjKaJQU-O5Lw471RaJzT9GZ9zgDZBmkb14COMSTLGgHJOrHHQSqUln2Es5ASJ.01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC`

```
[Drive ID (base64)]                                          [Item ID (base64)]
b!eX1FjKaJQU-O5Lw471RaJzT9GZ9zgDZBmkb14COMSTLGgHJOrHHQSqUln2Es5ASJ . 01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC
```

The **Item ID** (part after `.`) is what you use in the API call:
- `01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC`

---

## What the API Returns

When you call the Graph API, you get JSON like this:

```json
{
  "id": "01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC",
  "name": "0009de35-a0ee-4a6b-be8f-3f138249b829Cypress-Flow.png",
  "size": 144762,
  "lastModifiedDateTime": "2025-07-10T13:43:02Z",
  "mimeType": "image/png",
  "webUrl": "https://deltaairlines-my.sharepoint.com/personal/joseph_brashear_delta_com/Documents/STRIntakeDocumentLibrary/0009de35-a0ee-4a6b-be8f-3f138249b829Cypress-Flow.png",
  "parentReference": {
    "driveId": "b!eX1FjKaJQU-O5Lw471RaJzT9GZ9zgDZBmkb14COMSTLGgHJOrHHQSqUln2Es5ASJ",
    "path": "/drives/b!eX1FjKaJQU-O5Lw471RaJzT9GZ9zgDZBmkb14COMSTLGgHJOrHHQSqUln2Es5ASJ/root:/STRIntakeDocumentLibrary"
  }
}
```

---

## Quick Test Without Code

If you just want to test, you can use:

1. **Microsoft Graph Explorer** (Web):
   - Go to https://developer.microsoft.com/en-us/graph/graph-explorer
   - Login with your Delta account
   - Enter API: `/me/drive/items/01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC`
   - Click Run

2. **Postman**:
   - Import the Graph API collection
   - Set Bearer token
   - GET `https://graph.microsoft.com/v1.0/me/drive/items/01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC`

