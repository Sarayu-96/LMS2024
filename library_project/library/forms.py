from django import forms
from django.contrib.auth.models import User  # Built-in User model
from .models import Author, Book, Genre, Plan, Plancategory # Other model imports
from django.forms import modelformset_factory

# Create a formset for PlanCategory
PlanCategoryFormSet = modelformset_factory(Plancategory, fields=('plan', 'genre'), extra=1)


class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'password', widget = forms.PasswordInput
    )
    password2 = forms.CharField(
        label = 'comfirm password', widget = forms.PasswordInput
    )

    # since inheritance from modelform
    # i can use the model to declare the fields

    class Meta:
        model=User
        fields = ('username','first_name','email','password')

        # overiding a inbuilt method to check the
        # password = confirm password
        # clean_<fieldname>

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password']!=cd['password']:
                raise forms.ValidationError('password does not match')
            
            return cd['password2']
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'price', 'published_date', 'description', 
            'isbn', 'genre', 'language', 'publisher', 'pages', 'availability', 
            'image', 'rental_price', 'edition'
        ]
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'profile_image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields =  ['name', 'price', 'duration_days','description','max_books_allowed','max_rent_duration']

# class PlanCategoryForm(forms.ModelForm):
#     class Meta:
#         model = Plancategory
#         fields = ['plan', 'genre'] 

class PlanCategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Category Name"
    )
    plans = forms.ModelMultipleChoiceField(
        queryset=Plan.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Plans"
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Genres"
    )

    class Meta:
        model = Plancategory  # Assuming Category is the model to which plans and genres are related
        fields = ['name', 'plans', 'genres']


