# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import (ActivityTypes, Activity)
from .datetime_resolution import DateTimeResolution
from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult

class DateTimePrompt(Prompt):
    def __init__(self, dialog_id: str, validator: object = None, default_locale: str = None):
        super(DateTimePrompt, self).__init__(dialog_id, validator)
        self._default_locale = default_locale
        
    @property
    def default_locale(self) -> str:
        """Gets the locale used if `TurnContext.activity.locale` is not specified. 
        """
        return self._default_locale
        
    @default_locale.setter
    def default_locale(self, value: str) -> None:
        """Gets the locale used if `TurnContext.activity.locale` is not specified.

        :param value: The locale used if `TurnContext.activity.locale` is not specified.
        """
        self._default_locale = value
        
    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool):
        if not turn_context:
            raise TypeError('DateTimePrompt.on_prompt(): turn_context cannot be None.')
        if not options:
            raise TypeError('DateTimePrompt.on_prompt(): options cannot be None.')
        
        if is_retry == True and options.retry_prompt != None:
            await turn_context.send_activity(options.retry_prompt)  
        else:
            if options.prompt != None:
                await turn_context.send_activity(options.prompt)

    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError('DateTimePrompt.on_recognize(): turn_context cannot be None.')
        
        result = PromptRecognizerResult()
        if turn_context.activity.type == ActivityTypes.message:
            # Recognize utterance
            message = turn_context.activity
            # TODO: English contsant needs to be ported.
            culture = message.locale if message.locale != None else "English"
            # TODO: Move this import to top of file when recognizers package is published
            from recognizers_date_time import recognize_datetime
            results = recognize_datetime(message.text, culture)
            if len(results) > 0:
                result.succeeded = True
                result.value = []
                values = results[0].resolution['values']
                for value in values:
                    result.value.append(self.read_resolution(value))
        
        return result
        
    def read_resolution(self, resolution: Dict[str, str]) -> DateTimeResolution:
        result = DateTimeResolution()
        
        if "timex" in resolution:
            result.timex = resolution["timex"]
        if "value" in resolution:
            result.value = resolution["value"]
        if "start" in resolution:
            result.start= resolution["start"]
        if "end" in resolution:
            result.end = resolution["end"]
            
        return result
            

