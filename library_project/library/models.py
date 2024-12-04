# from django.db import models

# class Book(models.Model):
#     title = models.CharField(max_length=255)  # Book title
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # Relationship to Author
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price of the book
#     published_date = models.DateField(blank=True, null=True)  # Publication date
#     created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp for creation
#     description = models.TextField(blank=True, null=True)  # Book description
#     isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)  # ISBN (unique)
#     genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to Genre model
#     language = models.CharField(max_length=50, blank=True, null=True)  # Language in which the book is written
#     publisher = models.CharField(max_length=255, blank=True, null=True)  # Publisher of the book
#     pages = models.PositiveIntegerField(blank=True, null=True)  # Number of pages in the book
#     availability = models.BooleanField(default=True)  # Availability status (available or not)
#     image = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # Book cover image
#     rental_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Rental price

# class Author:

