# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.dialog_context import DialogContext

class WaterfallStepContext(DialogContext):

    def __init__(self, stack: []):
        if stack is None:
            raise TypeError('DialogState(): stack cannot be None.')
        self.__dialog_stack = stack
        
    @property
    def dialog_stack(self):
        return __dialog_stack;