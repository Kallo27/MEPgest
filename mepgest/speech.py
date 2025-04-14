#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: speech.py
# Created: 14-04-2025
# Author: Lorenzo Calandra Buonaura <lorenzocb01@gmail.com>
# Institution: University of Innsbruck - UIBK
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
    
    # Default weights for each speech type
    default_weights = {
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

    @classmethod
    def get_weight(cls, speech_type):
        return cls.default_weights.get(speech_type, 1)
