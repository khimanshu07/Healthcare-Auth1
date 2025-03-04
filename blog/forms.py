from django import forms
from .models import BlogPost, Category

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the category queryset to only include specific categories
        self.fields['category'].queryset = Category.objects.filter(
            name__in=['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']
        )