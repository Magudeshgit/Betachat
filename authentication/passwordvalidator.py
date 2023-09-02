from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.core.exceptions import ValidationError

class MinimumLengthValidator:
    """
    Validate that the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "This password is too short, It must contain at least "
                    "%(min_length)d Numbers.",
                    "This password is too short. It must contain at least "
                    "%(min_length)d Numbers.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_length)d character.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length,
        ) % {"min_length": self.min_length}



class NumericPasswordValidator:

    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError(
                _("Your password cannot be alphabetic."),
                code="password_entirely_alphabetic",
            )

    def get_help_text(self):
        return _("Your password can’t be alphabetic.")