from app.utils import (
    print_green_bold,
    model_mapper,
    json_camel_to_snake,
    text_to_red,
    text_to_blue,
)
from app.models import Officer, OfficerRepository
from app.services import fireant as fa, FirebaseService
from config import STOCK_SYMBOLS
from config.firebase import FIREBASE_INDIVIDUAL_URL
from config.fireant import INDIVIDUAL_AVATAR_URL

import pandas as pd, inflection, requests, os, sys
from firebase_admin import storage


def main():
    """
    This seeder accumulate all required officer before insert into database
    Which mean if it fails, you should go to your Firebase Storage and delete all the individual avatar
    """
    print_green_bold("=== SEEDING OFFICERS")

    raw_officers_data = []
    for symbol in STOCK_SYMBOLS:
        print(f"- fetching officer data for {text_to_red(symbol)}")
        raw_officers: list[dict] = fa.get_officers(symbol)
        # add symbol, a little redundant tho
        for officer in raw_officers:
            officer.update({"symbol": symbol})

        raw_officers_data.extend(raw_officers)

    officers_df = pd.DataFrame(raw_officers_data)
    officers_df.columns = [inflection.underscore(col) for col in officers_df.columns]
    officers_df.rename(columns={"individual_id": "id"}, inplace=True)

    # init firebase service
    FirebaseService()
    # Define to bucket
    bucket = storage.bucket()

    officers_accumulator: list[Officer] = []
    for _, row in officers_df.iterrows():
        officer_dict = row.to_dict()
        officer_id = officer_dict["id"]

        folder_name = "individual"
        avatar_name = f"{officer_id}.png"

        source_url = INDIVIDUAL_AVATAR_URL.format(id=officer_id)
        response = requests.get(source_url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:

            # Upload the image to Firebase Storage
            blob = bucket.blob(f"{folder_name}/{avatar_name}")
            # upload
            blob.upload_from_string(
                response.content, content_type=response.headers.get("content-type")
            )
            # the url to store in database
            avatar_url = FIREBASE_INDIVIDUAL_URL.format(
                bucket_name=os.getenv(
                    "FIREBASE_BUCKET_NAME",
                ),
                image_name=avatar_name,
            )
            print(
                f"{text_to_red(symbol)} Individual {text_to_blue(officer_dict['name'])} with id {officer_id} and avatar url: {avatar_url}"
            )
            # add avatar to the officer model
            officer_dict.update({"avatar": avatar_url})
            model = Officer(**officer_dict)
            officers_accumulator.append(model)

        else:
            print(
                f"Error fetching avatar for {officer_dict['name']} with id {officer_id}:",
                response.status_code,
            )
    OfficerRepository().save_many(officers_accumulator)


if __name__ == "__main__" or __name__ == "tasks":
    main()
