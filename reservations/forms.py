from django.forms import CharField, Form


class NameForm(Form):
    name = CharField(max_length=128)


if __name__ == '__main__':
    pass
