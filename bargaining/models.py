# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree.common import money_range

doc = """
This bargaining game involves 2 players. Each demands for a portion of some available amount. 
If the sum of demands is no larger than the available amount, both players get demanded portions. 
Otherwise, both get nothing.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/bargaining" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'bargaining'

    amount_shared = models.MoneyField(
        default=1.00,
        doc="""
        Amount to be shared by both players
        """
    )


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        total_requested_amount = sum([p.request_amount for p in self.get_players()])
        if total_requested_amount < self.subsession.amount_shared:
            for p in self.get_players():
                p.payoff = p.request_amount
        else:
            for p in self.get_players():
                p.payoff = 0


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    request_amount = models.MoneyField(
        default=None,
        doc="""
        Amount requested by this player.
        """
    )

    def request_amount_choices(self):
        """Range of allowed request amount"""
        return money_range(0, self.subsession.amount_shared, 0.05)

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]


