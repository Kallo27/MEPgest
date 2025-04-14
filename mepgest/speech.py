#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: speech.py
# Created: 14-04-2025
# Author: Lorenzo Calandra Buonaura <lorenzocb01@gmail.com>
# Institution: APS Model European Parliament Italia
#
# Description: 
#

########################
# IMPORT ZONE          #
########################

from enum import Enum


########################
# CLASSES              #
########################

from enum import Enum

class SpeechType(Enum):
    OPENING = "Opening speech"
    AMENDMENT_SPEECH = "Amendment speech"
    AMENDMENT_DEFENSE = "Amendment defense"
    FOLLOW_UP = "Follow-up"
    FOLLOW_UP_DEFENSE = "Follow-up defense"
    INTERVENTION = "Intervention"
    DEFENSE = "Defense"
    SPEECH_AGAINST = "Speech against"
    CLOSING = "Closing Speech"
    
    @classmethod
    def get_weight(cls, speech_type):
        return cls._weights.get(speech_type.value, 1)

    @classmethod
    def set_weight(cls, speech_type, weight):
        if not isinstance(speech_type, cls):
            raise ValueError("speech_type must be an instance of SpeechType Enum")
        cls._weights[speech_type.value] = weight

    @classmethod
    def set_weights(cls, weights_dict):
        """Set multiple weights at once using a dictionary."""
        for speech_name, weight in weights_dict.items():
            try:
                enum_member = cls(speech_name)
            except ValueError:
                # Allow setting directly by label string if needed
                if speech_name in cls._weights:
                    cls._weights[speech_name] = weight
                else:
                    raise ValueError(f"{speech_name} is not a valid speech label.")
            else:
                cls._weights[enum_member.value] = weight


# Define the actual weights *outside* the class
SpeechType._weights = {
    "Opening speech": 3.5,
    "Amendment speech": 3,
    "Amendment defense": 3,
    "Follow-up": 2,
    "Follow-up defense": 2,
    "Intervention": 3,
    "Defense": 3,
    "Speech against": 3,
    "Closing Speech": 3.5,
}