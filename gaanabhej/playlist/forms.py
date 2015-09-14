from django		import forms

class PlayListForm(forms.Form):

	songName	= forms.CharField(
					help_text='Name of the song to be suggested',
					required=True,
					widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your suggestion here'})
					)