from django import forms

from entry.models import Entry


class EntryForm(forms.ModelForm):
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Entry
        fields = ['title', 'content']

    def set_user(self, user):
        self.user = user

    def save(self, commit=True):
        entry = super().save(commit=False)
        if not entry.id:
            entry.user = self.user
        entry.save()
        return entry
