# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.ai.luis import LuisRecognizer, LuisApplication
from botbuilder.core import TurnContext

from booking_details import BookingDetails

class LuisHelper:
    
    @staticmethod
    async def excecute_luis_query(configuration: dict, turn_context: TurnContext) -> BookingDetails:
        booking_details = BookingDetails()

        try:
            luis_application = LuisApplication(
                configuration['LUIS_APP_ID'],
                configuration['LUIS_API_KEY'],
                configuration['LUIS_API_HOST_NAME']
            )

            recognizer = LuisRecognizer(luis_application)
            recognizer_result = await recognizer.recognize(turn_context)

            if recognizer_result.intents:
                intent = sorted(recognizer_result.intents, key=recognizer_result.intents.get, reverse=True)[:1][0]
                if intent == 'Book_flight':
                    # We need to get the result from the LUIS JSON which at every level returns an array.
                    to_entities = recognizer_result.entities.get("$instance", {}).get("To", [])
                    if len(to_entities) > 0:
                        booking_details.destination = to_entities[0]['text']
                    from_entities = recognizer_result.entities.get("$instance", {}).get("From", [])
                    if len(from_entities) > 0:
                        booking_details.origin = from_entities[0]['text']

                    # TODO: This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop the Time part.
                    # TIMEX is a format that represents DateTime expressions that include some ambiguity. e.g. missing a Year.
                    date_entities = recognizer_result.entities.get("$instance", {}).get("datetime", [])
                    if len(date_entities) > 0:
                        text = date_entities[0]['text']
                        booking_details.travel_date = None  # TODO: Set when we get a timex format
        except Exception as e:
            print(e)
        
        return booking_details

