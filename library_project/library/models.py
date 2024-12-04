from django.db import models
# vfcxbdcb

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='author_profiles/', blank=True, null=True)  # Profile image

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=255)  # Book title
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # Relationship to Author
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price of the book
    published_date = models.DateField(blank=True, null=True)  # Publication date
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp for creation
    description = models.TextField(blank=True, null=True)  # Book description
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)  # ISBN (unique)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to Genre model
    language = models.CharField(max_length=50, blank=True, null=True)  # Language in which the book is written
    publisher = models.CharField(max_length=255, blank=True, null=True)  # Publisher of the book
    pages = models.PositiveIntegerField(blank=True, null=True)  # Number of pages in the book
    availability = models.BooleanField(default=True)  # Availability status (available or not)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # Book cover image
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Rental price
    edition = models.PositiveIntegerField(blank=True, null=True)  # Edition as a number

    def __str__(self):
        return self.title

class Plan(models.Model):
     name = models.CharField(max_length=50)  # Plan name (e.g., Basic, Silver, Gold, Platinum)
     price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the plan
     duration_months = models.PositiveIntegerField()  # Duration in months
     created_at = models.DateTimeField(auto_now_add=True)  # Date when the plan was created
     updated_at = models.DateTimeField(auto_now=True)  # Date when the plan was last updated

