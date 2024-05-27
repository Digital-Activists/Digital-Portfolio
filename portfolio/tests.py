from django.core import validators
from django.forms import forms
from django.test import TestCase
from django.urls import reverse_lazy
from django.views.generic import FormView
from .form_utils import MultipleFileField, CustomFileInput
from .models import *


class TestForm(forms.Form):
    videos = MultipleFileField(label='Видео', validators=[FileExtensionValidator(PostVideo.formats)],
                               widget=CustomFileInput(style_class='input-file',
                                                      hint='Разрешены форматы: {0}'.format(', '.join(PostVideo.formats))))
    images = MultipleFileField(label='Фотографии', validators=[validators.validate_image_file_extension],
                               widget=CustomFileInput(style_class='input-file',
                                                      hint='Разрешены форматы png, jpeg, jpg'))
    files = MultipleFileField(label='Документы', validators=[FileExtensionValidator(PostFile.formats)],
                              widget=CustomFileInput(style_class='input-doc',
                                                     hint='Разрешены форматы: {0}'.format(', '.join(PostFile.formats))))


class TestView(FormView):
    template_name = 'portfolio/plug/plug-form.html'
    form_class = TestForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        form.fields['images'].initial = PostPhoto.objects.all()
        context['videos'] = PostVideo.objects.all()
        context['files'] = PostFile.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        return super(TestView, self).post(request, *args, **kwargs)