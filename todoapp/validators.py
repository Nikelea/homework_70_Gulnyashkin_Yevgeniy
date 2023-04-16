from email import message
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Не жалей букв! Минимум %(limit_value)d надо, а в наличии только %(show_value)s!'

    def compare(self, a, b) -> bool:
        return a < b

    def clean(self, x):
        return len(x)


@deconstructible
class WordLengthValidator(BaseValidator):
    message = 'The word can be not longer than %(limit_value)d. Word %(show_value)s is too long!'


    def compare(self, a, b) -> bool:
        if len(a) > b:
            return True
        else:
            return False

    def longest_word(self, x) -> str:
        longest = ''
        for word in x.split():
            if len(word) > len(longest):
                longest = word
        return longest

    def clean(self, x):
        return self.longest_word(x)
