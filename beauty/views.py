# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):

    return {'total_q': 1}


class Introduction(Page):

    template_name = 'beauty/Introduction.html'


class Question1(Page):

    template_name = 'beauty/Question.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1_win_pick',
                   'training_question_1_my_payoff']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'beauty/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,
            'is_answer_win_pick_correct': self.player.is_training_question_1_win_pick_correct(),
            'is_answer_my_payoff_correct': self.player.is_training_question_1_my_payoff_correct(),
            'answer_win_pick': self.player.training_question_1_win_pick,
            'answer_my_payoff': self.player.training_question_1_my_payoff,
        }



class Guess(Page):

    template_name = 'beauty/Guess.html'

    form_model = models.Player
    form_fields = ['guess_value']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for the other participants."



class Results(Page):

    template_name = 'beauty/Results.html'

    def vars_for_template(self):
        other_guesses = []
        winners_cnt = int(self.player.is_winner)
        for p in self.player.get_others_in_group():
            other_guesses.append(p.guess_value)
            winners_cnt += int(p.is_winner)
        return {'guess_value': self.player.guess_value, #
                'other_guesses': other_guesses, #
                'other_guesses_count': len(other_guesses), #
                'two_third_average': round(self.group.two_third_guesses, 4), #
                'players': self.group.get_players(),
                'is_winner': self.player.is_winner, #
                'best_guess': self.group.best_guess, #
                'tie': self.group.tie, #
                'winners_count': winners_cnt, #
                'total_payoff': self.player.payoff + Constants.fixed_pay, #
                'payoff': self.player.payoff} #


pages = [Introduction,
            Question1,
            Feedback1,
            Guess,
            ResultsWaitPage,
            Results]
