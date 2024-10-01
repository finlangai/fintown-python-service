from app.utils import print_green_bold, text_to_red
from app.services import FirebaseService
from app.models import CompanyRepository
from config import FIREBASE_LOGO_URL, SIMPLIZE_LOGO_URL
from core import mongodb

from firebase_admin import storage
import os, requests


def main():
    print_green_bold("=== SEEDING LOGOS")

    # init firebase service
    FirebaseService()

    symbol_list: list[dict] = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name,
        {
            "logo": {"$exists": False}
        },  # Filter to get documents without the 'logo' field
        {"_id": 0, "symbol": 1},  # Projection to include only the 'symbol' field
    )

    symbol_list: list[str] = [record["symbol"] for record in symbol_list]

    # Define to bucket
    bucket = storage.bucket()

    for symbol in symbol_list:

        source_url = SIMPLIZE_LOGO_URL.format(symbol=symbol)
        response = requests.get(source_url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Upload the image to Firebase Storage
            blob = bucket.blob(
                f"logo/{symbol}.jpeg"
            )  # Replace with your desired file path
            blob.upload_from_string(
                response.content, content_type=response.headers.get("content-type")
            )
            image_url = FIREBASE_LOGO_URL.format(
                bucket_name=os.getenv(
                    "FIREBASE_BUCKET_NAME",
                ),
                image_name=f"{symbol}.jpeg",
            )
            mongodb.update_one("companies", {"symbol": symbol}, {"logo": image_url})

            print(f"{text_to_red(symbol)} Logo uploaded successfully! URL:", image_url)
        else:
            print(f"{symbol} Error fetching logo :", response.status_code)

    print_green_bold(f"{len(symbol_list)} logo seeded")


if __name__ == "__main__" or __name__ == "tasks":
    main()
