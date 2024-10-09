from firebase_admin import credentials
import json, firebase_admin, os, base64


class FirebaseService:
    def __init__(self) -> None:

        # decoding
        credential_base64 = os.getenv("FIREBASE_ADMIN_CREDENTIALS")
        decoded_bytes = base64.b64decode(credential_base64)
        decoded_string = decoded_bytes.decode("UTF-8")

        credential_json = json.loads(decoded_string)

        cred = credentials.Certificate(credential_json)
        firebase_admin.initialize_app(
            cred,
            {"storageBucket": os.getenv("FIREBASE_BUCKET_NAME")},
        )
