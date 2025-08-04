from django import forms
from .models import Article, Category, Tag, Source, AuthorProfile, ArticleImage
from django_tiptap.widgets import TipTapWidget


# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = [
#             'title',
#             'slug',
#             'abstract',
#             'content',
#             'version',
#             'is_draft',
#             'categories',
#             'tags',
#             'image',
#             'sources',
#         ]
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
#             'slug': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
#             'abstract': TipTapWidget(),
#             'content': TipTapWidget(),
#             'version': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
#             'is_draft': forms.CheckboxInput(attrs={'class': 'mr-2'}),
#             'categories': forms.CheckboxSelectMultiple(),
#             'tags': forms.CheckboxSelectMultiple(),
#             'sources': forms.CheckboxSelectMultiple(),
#             'image': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Queryset filtering and label customization
#         self.fields['categories'].queryset = Category.objects.all().distinct()
#         self.fields['tags'].queryset = Tag.objects.all().distinct()
#         self.fields['sources'].queryset = Source.objects.all().distinct()
#         self.fields['image'].queryset = ArticleImage.objects.all().distinct()
#
#         self.fields['categories'].label_from_instance = lambda obj: obj.name
#         self.fields['tags'].label_from_instance = lambda obj: obj.name
#         self.fields['sources'].label_from_instance = lambda obj: obj.name
#         self.fields['image'].label_from_instance = lambda obj: obj.name or f"Image {obj.id}"



# class SourceForm(forms.ModelForm):
#     class Meta:
#         model = Source
#         fields = ['title', 'creator', 'publication_date', 'type', 'url']
#         widgets = {
#             'publication_date': forms.DateInput(attrs={'type': 'date'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # ensure empty label for blank choices
#         self.fields['type'].empty_label = None
#
#
# class AuthorProfileForm(forms.ModelForm):
#     # Add user-related fields manually
#     first_name = forms.CharField(
#         max_length=150,
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'w-full px-4 py-2 border rounded-md',
#         })
#     )
#     last_name = forms.CharField(
#         max_length=150,
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'w-full px-4 py-2 border rounded-md',
#         })
#     )
#     email = forms.EmailField(
#         required=False,
#         widget=forms.EmailInput(attrs={
#             'class': 'w-full px-4 py-2 border rounded-md',
#         })
#     )
#     username = forms.CharField(
#         max_length=150,
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'w-full px-4 py-2 border rounded-md',
#         })
#     )
#
#     class Meta:
#         model = AuthorProfile
#         fields = ['bio', 'profile_picture']
#         widgets = {
#             'bio': forms.Textarea(attrs={
#                 'class': 'w-full px-4 py-2 border rounded-md',
#                 'rows': 4,
#             }),
#             'profile_picture': forms.ClearableFileInput(attrs={
#                 'class': 'w-full px-4 py-2 border rounded-md',
#             }),
#         }
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user", None)
#         super().__init__(*args, **kwargs)
#
#         # Populate initial user field values
#         if user:
#             self.fields['first_name'].initial = user.first_name
#             self.fields['last_name'].initial = user.last_name
#             self.fields['email'].initial = user.email
#             self.fields['username'].initial = user.username
#             self.user_instance = user
#
#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         # Save user fields separately
#         user = self.user_instance
#         user.first_name = self.cleaned_data.get("first_name")
#         user.last_name = self.cleaned_data.get("last_name")
#         user.email = self.cleaned_data.get("email")
#         user.username = self.cleaned_data.get("username")
#         if commit:
#             user.save()
#             profile.user = user
#             profile.save()
#         return profile
#
#
# class ArticleImageForm(forms.ModelForm):
#     class Meta:
#         model = ArticleImage
#         fields = ['title', 'slug', 'file', 'source']
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border rounded-md',
#                 'placeholder': 'Enter image title...'
#             }),
#             'slug': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border rounded-md',
#                 'placeholder': 'Custom slug (optional)...'
#             }),
#             'file': forms.ClearableFileInput(attrs={
#                 'class': 'w-full px-4 py-2 border rounded-md'
#             }),
#             'source': forms.Select(attrs={
#                 'class': 'w-full px-4 py-2 border rounded-md'
#             }),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Optional: Customize source dropdown
#         self.fields['source'].queryset = Source.objects.all().distinct()
#         self.fields['source'].label_from_instance = lambda obj: obj.name if hasattr(obj, 'name') else str(obj)


