from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label="検索ワード",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "検索ワードを入力"})
    )
