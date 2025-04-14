#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: models.py
# Created: 14-04-2025
# Author: Lorenzo Calandra Buonaura <lorenzocb01@gmail.com>
# Institution: APS Model European Parliament Italia
#
# Description: 
#


########################
# IMPORT ZONE          #
########################

from mepgest.speech import SpeechType


########################
# CLASSES              #
########################

committees = {} # Global
schools = {}    # Global
delegates = {}  # Global

class Committee:
    def __init__(self, name):
        self.name = name
        self.delegates = []

    def add_delegate(self, participant):
        self.delegates.append(participant)

    def total_weight(self):
        return sum(delegate.total_weight() for delegate in self.delegates) / len(self.delegates)

    def __str__(self):
        return f"Committee {self.name} with {len(self.delegates)} delegates"
    
    
class School:
    def __init__(self, name):
        self.name = name
        self.delegates = []

    def add_delegate(self, participant):
        self.delegates.append(participant)

    def total_weight(self):
        return sum(delegate.total_weight() for delegate in self.delegates) / len(self.delegates)

    def __str__(self):
        return f"School {self.name} with {len(self.delegates)} delegates"


class Delegate:
    def __init__(self, name, surname, gender, committee_name, school_name):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.committee_name = committee_name
        self.school_name = school_name
        self.speeches = []

        # Auto-register to committee
        if committee_name not in committees:
            committees[committee_name] = Committee(committee_name)
        committees[committee_name].add_delegate(self)

        # Auto-register to school
        if school_name not in schools:
            schools[school_name] = Committee(school_name)
        schools[school_name].add_delegate(self)
        
    def speak(self, speech_type, time=None):
        # Validate speech type and get weight
        weight = SpeechType.get_weight(speech_type)
        self.speeches.append({
            "type": speech_type,
            "weight": weight
        })

    def speech_count(self):
        return len(self.speeches)

    def total_weight(self):
        return sum(speech["weight"] for speech in self.speeches)
    
    def score(self):
        committee = committees.get(self.committee_name)
        school = schools.get(self.school_name)
        committee_weight = committee.total_weight() if committee else 0
        school_weight = school.total_weight() if school else 0
        
        # TO DO
        return self.total_weight() + committee_weight + school_weight

    def __str__(self):
        return f"{self.name} {self.surname} from {self.school} ({self.committee_name})"


def assign_delegate_codes():
    # Sort committee names alphabetically and number them starting from 1
    sorted_committees = sorted(committees.items())  # [(name, Committee), ...]
    for committee_index, (committee_name, committee) in enumerate(sorted_committees, start=1):
        # Sort delegates in the committee by surname then name
        sorted_delegates = sorted(committee.delegates, key=lambda d: (d.surname.lower(), d.name.lower()))
        for i, delegate in enumerate(sorted_delegates, start=1):
            code = f"{committee_index}{i:02d}"
            delegate.code = code
            delegates[code] = delegate  # Add delegate to global delegates dictionary
