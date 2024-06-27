from django import forms

class myForm(forms.Form):
    file = forms.FileField(
        label='Image',
    )
    caption = forms.CharField(
        label='Caption',
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'rows': 4, 
                'cols': 40,
                'placeholder': 'Enter your caption here...',
            }
        ))

class formSet(forms.Form):
    usrname = forms.CharField(label='Username',max_length=50)
    slToken = forms.CharField(label='Access Token', max_length=300)
    fbPgId = forms.IntegerField(label='FB Page ID')
    appId = forms.IntegerField(label='App ID')
    appSecret = forms.CharField(label='App Secret',max_length=150)