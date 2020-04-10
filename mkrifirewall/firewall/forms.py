from django.forms import Form, Textarea, CharField


class NFTablesConfigForm(Form):
    # nft_config = Textarea(initial=NFTables.get_current_configuration())
    nft_config = CharField(widget=Textarea(attrs={"rows": 30, 'class': 'form-control'}), label="")
