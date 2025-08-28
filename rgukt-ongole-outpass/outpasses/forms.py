from django import forms
from .models import Outpass
from accounts.models import User

class OutpassForm(forms.ModelForm):
    # allow selecting wardens or faculty if wardens empty
    warden = forms.ModelChoiceField(
        queryset=User.objects.filter(role__in=['warden','faculty']),
        required=False,
        empty_label="-- Select Warden/Faculty --"
    )
    class Meta:
        model = Outpass
        fields = ['warden','reason','attachment','date','time']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'time': forms.TimeInput(attrs={'type':'time','class':'form-control'}),
            'reason': forms.Textarea(attrs={'class':'form-control','rows':4, 'placeholder':'Why do you need to go out?'}),
            'attachment': forms.FileInput(attrs={'class':'form-control'}),
        }

