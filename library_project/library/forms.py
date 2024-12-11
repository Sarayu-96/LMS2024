from django import forms
from django.contrib.auth.models import User  # Built-in User model
from .models import Author, Book, Genre, Plan, Plancategory, Review # Other model imports
from django.forms import modelformset_factory

# Create a formset for PlanCategory

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

class GenreForm(forms.ModelForm):
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
        fields = ['plans', 'genres']

class AddCategoryForm(forms.ModelForm):
    plans = forms.ModelMultipleChoiceField(
        queryset=Plan.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Subscription Plans"
    )

    class Meta:
        model = Genre
        fields = ['name']

    def save(self, commit=True):
        # Save the category instance
        genre = super().save(commit=False)
        if commit:
            genre.save()
        # Add selected plans to the PlanCategory table
        if 'plans' in self.cleaned_data:
            selected_plans = self.cleaned_data['plans']
            for plan in selected_plans:
                Plancategory.objects.create(plan=plan, genre=genre)
        return genre
    

class EditCategoryForm(forms.ModelForm):
    plans = forms.ModelMultipleChoiceField(
        queryset=Plan.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Subscription Plans"
    )

    class Meta:
        model = Genre
        fields = ['name']

    def save(self, commit=True):
        # Save the category instance
        genre = super().save(commit=False)
        if commit:
            genre.save()
        # Add selected plans to the PlanCategory table
        if 'plans' in self.cleaned_data:
            selected_plans = self.cleaned_data['plans']
            for plan in selected_plans:
                Plancategory.objects.create(plan=plan, genre=genre)
        return genre


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']  # Include only rating and review text
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }




