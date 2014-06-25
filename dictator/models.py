# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from ptree.common import currency


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'dictator'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    allocated_amount = models.PositiveIntegerField(null=True,
                           doc="""
                           Initial amount allocated to Dictator player
                           """)


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    participants_per_match = 2

    offer_amount = models.PositiveIntegerField(null=True,
                         doc="""
                         Amount to be offered by Dictator player to the Other player
                         """)

    def offer_choices(self):
        """range of allowed incremented offer values"""
        return range(0, self.treatment.allocated_amount+1, 5)

    def get_offer_field_choices(self):
        """a tuple with the range of allowed offer values"""
        return tuple([(i, currency(i)) for i in self.offer_choices()])


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    def set_payoff(self):
        if self.index_among_participants_in_match == 1:
            self.payoff = self.treatment.allocated_amount - self.match.offer_amount
        else:
            self.payoff = self.match.offer_amount


def treatments():

    treatment_list = []

    treatment = Treatment(
        allocated_amount=100,
    )

    treatment_list.append(treatment)

    return treatment_list