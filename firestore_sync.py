import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json

# Replace with your own credentials and project ID
# You can get your credentials from your Google Cloud Console
# More info: https://cloud.google.com/docs/authentication/getting-started
cred = credentials.Certificate(
    "uf-sg-legislative-tracker-firebase-adminsdk-jl4ry-e293cdad4e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Firestore client


def upload_data(data):
    for entry in data:
        try:
            doc_ref = db.collection("legislation").document(entry["id"])
            doc_ref.set(entry)
        except:
            print("Error")
            print(entry)


def main():
    json_file_path = "legislation_data.json"
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        upload_data(data)
        print("Data uploaded to Cloud Firestore successfully!")


if __name__ == "__main__":
    main()
