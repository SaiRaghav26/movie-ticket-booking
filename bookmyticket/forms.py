from django import forms
from .models import Seat
from .utils import SeatCreator

class SeatAdminForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        show = kwargs.pop('show', None)  # Extract the 'show' from kwargs
        
        super().__init__(*args, **kwargs)

        if show:
            seat_creator = SeatCreator(show)
            seat_creator.run()  # Creates seats dynamically if not already created

            # Dynamically generate form fields for seats
            rows = show.rows  # Fetch rows from ShowTimings
            cols = show.columns  # Fetch columns from ShowTimings

            for row in range(1, rows + 1):
                for col in range(1, cols + 1):
                    field_name = f'seat_{chr(64+row)}{col}'
                    self.fields[field_name] = forms.BooleanField(required=False, label=f'{chr(64+row)}{col}')
