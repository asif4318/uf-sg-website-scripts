import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json
import os

# Replace with your own credentials and project ID
# You can get your credentials from your Google Cloud Console
# More info: https://cloud.google.com/docs/authentication/getting-started
cred = credentials.Certificate(
    "uf-sg-legislative-tracker-firebase-adminsdk-jl4ry-e293cdad4e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Reference to the "legislation" collection
legislation_ref = db.collection("legislation")

# Check if legislation_data.json already exists
output_file_path = "legislation_data.json"
if os.path.exists(output_file_path):
    print(f"{output_file_path} already exists. Checking for filtering.")

    # Load existing data from the JSON file
    with open(output_file_path, "r") as existing_file:
        existing_legislation_data = json.load(existing_file)

    # Filter out entries whose id property does not begin with "SSB"
    filtered_legislation_data = [
        entry for entry in existing_legislation_data if entry.get("id", "").startswith("SSB")]

    # Add verified value - if it does not exist, default to False
    for entry in filtered_legislation_data:
        entry["verified"] = entry.get("verified", False)

    # Write the filtered data back to the JSON file
    with open(output_file_path, "w") as output_file:
        json.dump(filtered_legislation_data, output_file, indent=2)

    print(
        f"Filtered and updated {output_file_path} with {len(filtered_legislation_data)} documents.")
else:
    # Retrieve all documents from the collection
    legislation_docs = legislation_ref.stream()

    # Create an empty list to hold the document data
    legislation_data = []

    # Iterate through each document and extract the data
    for doc in legislation_docs:
        doc_data = doc.to_dict()
        legislation_data.append(doc_data)

    # Write the data to the JSON file
    with open(output_file_path, "w") as output_file:
        json.dump(legislation_data, output_file, indent=2)

    print(f"Exported {len(legislation_data)} documents to {output_file_path}")
