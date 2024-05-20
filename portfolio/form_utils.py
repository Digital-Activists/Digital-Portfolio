from django import forms


class ProfileAvatarImageWidget(forms.ClearableFileInput):
    template_name = 'portfolio/widgets/custom_image_widget.html'


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CustomRadioSelect(forms.RadioSelect):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value:
            instance = self.choices.queryset.get(pk=value)
            option['attrs']['data-description'] = instance.description
        return option


class CustomFileInput(forms.FileInput):
    template_name = 'portfolio/widgets/post_file_widget.html'
    allow_multiple_selected = True

    def __init__(self, style_class, hint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_class = style_class
        self.hint = hint

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['hint'] = self.hint
        context['widget']['style_class'] = self.style_class
        return context