from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now # Import timezone for date-time operations

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

class Plan(models.Model):
     name = models.CharField(max_length=50)  # Plan name (e.g., Basic, Silver, Gold, Platinum)
     price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the plan
     duration_days = models.PositiveIntegerField()  # Duration in months
     description = models.TextField(null=True, blank=True)
     max_books_allowed = models.PositiveIntegerField(default=5, help_text="Maximum number of books a user can rent")
     max_rent_duration = models.PositiveIntegerField(default=30, help_text="Maximum duration (in days) to rent books")
     created_at = models.DateTimeField(auto_now_add=True)  # Date when the plan was created
     updated_at = models.DateTimeField(auto_now=True)  # Date when the plan was last updated
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
    stock = models.PositiveIntegerField(default=0)  # Number of books available in stock
    pdf = models.FileField(upload_to='book_pdfs/', blank=True, null=True)  # PDF file for the book

    def __str__(self):
        return self.title
    
class Plancategory(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plans')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='plans')

    def __str__(self):
        return f"{self.plan.name}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)  # Subscription start date
    end_date = models.DateTimeField()  # Subscription end date
    status = models.CharField(
        max_length=20,
        default='active'  # Default value is 'active'
    )
    

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = now()
        # Automatically set the end_date based on the plan's duration when creating a subscription
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_active(self):
    # Check if the subscription is still active
        return self.status == 'active' and self.end_date > now()
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    rental_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='active')

    def save(self, *args, **kwargs):
        # Get the user's current subscription
        subscription = Subscription.objects.filter(user=self.user, status='active').first()

        if not subscription:
            raise ValueError("User does not have an active subscription.")

        # Set the return_date based on the subscription's plan's max_rent_duration
        if not self.return_date:
            self.end_date = self.rental_date + timedelta(days=subscription.plan.max_rent_duration)

        super().save(*args, **kwargs)

    def is_active(self):
        return self.status == 'active' and self.end_date > now()

    def __str__(self):
        return f"Rental: {self.user.username} - {self.book.title}"







    





     