from firebase_admin import credentials
import json, firebase_admin, os


class FirebaseService:
    def __init__(self) -> None:
        cred = credentials.Certificate(
            json.loads(os.environ.get("FIREBASE_ADMIN_CREDENTIALS"))
        )
        firebase_admin.initialize_app(
            cred,
            {"storageBucket": os.getenv("FIREBASE_BUCKET_NAME")},
        )
