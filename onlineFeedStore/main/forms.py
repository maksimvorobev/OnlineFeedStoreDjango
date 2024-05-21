import re
from django import forms

from main.models import Feedback


class CreateFeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ("first_name", "email", "phone_number", "subject", "content")

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]

        pattern = re.compile(
            r"^(^8|7|\+7)((\d{10})|(\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}))$"
        )
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера.")

        return data
