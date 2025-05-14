import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomComplexityValidator:
    def validate(self, password, user=None):
        checks = [
            bool(re.search(r'[0-9]', password)),          # Skaičius
            bool(re.search(r'[a-z]', password)),          # Mažoji raidė
            bool(re.search(r'[A-Z]', password)),          # Didžioji raidė
            bool(re.search(r'[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~\-\\|]', password)),  # Specialus simbolis
        ]
        passed = sum(checks)
        if passed < 2:
            raise ValidationError(
                _("Slaptažodis turi būti bent 8 simbolių ilgio ir atitikti bent du iš šių kriterijų: skaičius, mažoji raidė, didžioji raidė, specialus simbolis."),

                code='password_too_simple',
            )

    def get_help_text(self):
        return _(
            "Slaptažodis turi atitikti bent 2 iš šių kriterijų: skaičius, mažoji raidė, didžioji raidė, specialus simbolis."
        )
