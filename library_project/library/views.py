from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AddCategoryForm, AuthorForm, BookForm, AddCategoryForm, EditCategoryForm,PlanForm, PlanCategoryForm, ReviewForm
from .models import Author, Genre, Book, Notification, Plan, Plancategory, Rental, Subscription
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib import messages




def landing_page(request):
    return render(request, 'landing_page.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Check role (using groups or a profile model)
            if user.groups.filter(name="Librarian").exists():
                return redirect('librarian_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('view_books')


@login_required
def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html', {'user': request.user})

@login_required
def student_dashboard(request):
    books = Book.objects.all()
    return render(request, 'student_dashboard.html', {'user': request.user, 'books':books})


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            User.objects.create_user(username=username, password=password)
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

def subscription_plan_view(request):
    is_authenticated = request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('register')  # Redirect to the registration page if not logged in
    
    # Your subscription plan logic here
    return render(request, 'membership_plans.html', {'is_authenticated': is_authenticated})

def add_book(request):
    authors = Author.objects.all()  # Fetch all authors from the database
    genres = Genre.objects.all()  # Fetch all genres from the database

    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        price = request.POST.get('price')
        published_date = request.POST.get('published_date')
        isbn = request.POST.get('isbn')
        description = request.POST.get('description')
        language = request.POST.get('language')
        publisher = request.POST.get('publisher')
        genre_id = request.POST.get('genre')
        image = request.FILES.get('image')
        rental_price = request.POST.get('rental_price')
        edition = request.POST.get('edition')
        pages = request.POST.get('pages')
        stock = request.POST.get('stock')  # New stock field
        pdf = request.FILES.get('pdf')  # New pdf field

        # Save the new book
        author = Author.objects.get(id=author_id)
        genre = Genre.objects.get(id=genre_id)

        book = Book(
            title=title,
            author=author,
            price=price,
            published_date=published_date,
            isbn=isbn,
            description=description,
            language=language,
            publisher=publisher,
            genre=genre,
            image=image,
            rental_price=rental_price,
            edition=edition,
            pages=pages,
            stock=stock,
            pdf=pdf
        )
        book.save()

        return redirect('list_books')  # Redirect to the book list page

    return render(request, 'add_book.html', {'authors': authors, 'genres': genres})



def list_books(request):
    search_query = request.GET.get('q', '')  # Get the search query from the request
    books = Book.objects.all()

    if search_query:
        # Filter books based on title, author name, or genre name
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(genre__name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(books, 10)  # 10 books per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'list_view_book.html',
        {
            'page_obj': page_obj,
            'search_query': search_query,
        }
    )
def view_books(request):
    books = Book.objects.all()
    return render(request, 'home_page.html', {'books': books, 'user': request.user})

def view_book_details(request,book_id):
    # print(book_id)
    book = get_object_or_404(Book, id=book_id)
    author = book.author 
    allbooks = author.books.all()
    return render(request, 'view_book_details.html', {'author': author, 'books': allbooks ,'book': book, 'user': request.user})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()
    genres = Genre.objects.all()

    if request.method == 'POST':
        # Handle form submission and update book details
        book.title = request.POST['title']
        book.author = Author.objects.get(id=request.POST['author'])
        book.price = request.POST['price']
        book.published_date = request.POST['published_date']
        book.language = request.POST['language']
        book.pages = request.POST['pages']
        book.isbn = request.POST['isbn']
        book.publisher = request.POST['publisher']
        book.description = request.POST['description']
        book.genre = Genre.objects.get(id=request.POST['genre'])
        book.rental_price = request.POST['rental_price']
        book.edition = request.POST['edition']
        book.stock = request.POST['stock']  # Update stock

       # Handle image upload and save
        if 'image' in request.FILES:
            book.image = request.FILES['image']
            # Handle PDF upload and save
        if 'pdf' in request.FILES:
            book.pdf = request.FILES['pdf']
            
        book.save()
        return redirect('list_books')

    return render(request, 'edit_book.html', {
        'book': book,
        'authors': authors,
        'genres': genres
    })


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')  # Redirect to the list page after deletion
    

def view_authors(request):
    form = AuthorForm()
    search_query = request.GET.get('q', '')  # Get search query from the URL parameter

    authors = Author.objects.all()  # Fetch all authors

    if search_query:
        # Filter authors based on the search query in their name
        authors = authors.filter(
            Q(name__icontains=search_query)
        )

    paginator = Paginator(authors, 10)  # 10 authors per page
    page_number = request.GET.get('page', 1)  # Get the current page number, default to 1
    page_obj = paginator.get_page(page_number)

    return render(request, 'view_authors.html', {
        'page_obj': page_obj,  # Pass the paginated authors to the template
        'form': form,  # Pass the form to the template
        'search_query': search_query  # Pass the search query back to the template for persistence
    })

def book_search(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


    

    
    return render(request, 'membership_plans.html', {'plans': plans, 'user': request.user})


    if search_query:
        # Filter authors by name (case-insensitive) and order them
        authors = Author.objects.filter(name__icontains=search_query).order_by('name')
    else:
        # If no search query, return all authors ordered by name
        authors = Author.objects.all().order_by('name')

    # Set up pagination: Show 10 authors per page
    paginator = Paginator(authors, 10)
    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the authors for the current page

    return render(request, 'view_authors.html', {
        'page_obj': page_obj,  # Pass the paginated object to the template
        'search_query': search_query,  # Pass the search query to keep it in the input field
        'form': form  # Pass the form to the template for rendering in the modal
    })


# Add a new author

def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()

            # If it's an AJAX request (from the modal form submission)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                authors = Author.objects.all().order_by('name')
                # Render only the authors' list to be updated dynamically in the modal
                authors_html = render_to_string('view_authors', {'authors': authors})
                return JsonResponse({'success': True, 'authors_html': authors_html})

            # If it's a normal form submission (non-AJAX), you could redirect or respond appropriately
            return JsonResponse({'success': True})

        # If the form is not valid, return form errors as a JSON response
        return JsonResponse({'error': form.errors}, status=400)

    # If the request is not a POST (GET request), you don't need to render anything
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Update an existing author
def update_author(request, author_id):
    author = get_object_or_404(Author,id=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('view_authors')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'update_author.html', {'form': form, 'author': author})


# Delete an author
def delete_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        author.delete()
        return redirect('view_authors')
    return render(request, 'delete_author.html', {'author': author})


def view_categories(request):
    categories = Genre.objects.all()  # Fetch all categories
    plans_by_category = {}

    # Fetch the plans associated with each category (Genre)
    for category in categories:
        # Using the Plancategory relationship to fetch associated plans for each genre
        plans = Plan.objects.filter(plans__genre=category)  # Filter plans by genre (category)
        plans_by_category[category.id] = plans

    return render(request, 'view_categories.html', {'categories': categories, 'plans_by_category': plans_by_category})


# Delete a category
def delete_category(request, genre_id):
    category = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        category.delete()
        return redirect('view_categories')
    return render(request, 'delete_category.html', {'category': category})


def add_modal_author(request):
    if request.method == "POST":
        new_author_name = request.POST.get('new-author')

        # Create and save the new author
        new_author = Author.objects.create(name=new_author_name)

        # Return the newly added author as a JSON response
        return JsonResponse({
            'status': 'success',
            'author': {
                'id': new_author.id,
                'name': new_author.name,
            }
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def view_plans(request):
    form = PlanForm()
    plangenre_form = PlanCategoryForm()
    plans = Plan.objects.all()
    return render(request, 'view_plans.html', {'plans': plans, 'form': form, 'plangenre_form': plangenre_form})


def add_plan(request):
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #     authors = Author.objects.all().order_by('name')
            #     # Render only the authors' list to be updated dynamically in the modal
            #     authors_html = render_to_string('view_authors', {'authors': authors})
            # return JsonResponse({'success': True, 'authors_html': authors_html})

            # If it's a normal form submission (non-AJAX), you could redirect or respond appropriately
        return JsonResponse({'success': True})

        # If the form is not valid, return form errors as a JSON response
    return JsonResponse({'error': form.errors}, status=400)


def edit_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    all_genres = Genre.objects.all()
    associated_genres = Plancategory.objects.filter(plan=plan).values_list('genre_id', flat=True)
    plan_category_form = PlanCategoryForm(request.POST)

    if request.method == 'POST':
        # Update plan fields
        plan.name = request.POST['name']
        plan.price = request.POST['price']
        plan.duration_days = request.POST['duration_days']
        plan.description = request.POST['description']
        plan.max_books_allowed = request.POST['max_books_allowed']
        plan.max_rent_duration = request.POST['max_rent_duration']
        plan.save()

        # Update associated genres
        selected_genres = request.POST.getlist('genres')
        Plancategory.objects.filter(plan=plan).delete()  # Clear existing associations
        for genre_id in selected_genres:
            genre = Genre.objects.get(id=genre_id)
            Plancategory.objects.create(plan=plan, genre=genre)

        return JsonResponse({'success': True})

    return render(request, 'view_plans.html', {
        'plan': plan,
        'all_genres': all_genres,
        'associated_genres': associated_genres,
        'plan_category_form' : plan_category_form
    })


def delete_plan(request, plan_id):
    # Fetch the plan object from the database
    plan = get_object_or_404(Plan, id=plan_id)
    
    if request.method == 'POST':
        # Delete the plan
        plan.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = AddCategoryForm()
    return render(request, 'add_category.html', {'form': form})


def edit_category(request,genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST or None,request.FILES or None, instance=genre) 
        if form.is_valid():
            form.save()
            return redirect('view_categories')
        else:
            print(form.errors)
    else:
        form = EditCategoryForm(instance=genre)
    return render(request, 'edit_category.html', {'form': form})




# def author_list(request):
#     search_query = request.GET.get('q', '')  # Get the search query from the URL
#     if search_query:
#         # Filter authors by name, case-insensitive search
#         authors = Author.objects.filter(name__icontains=search_query)
#     else:
#         # If no search query, show all authors
#         authors = Author.objects.all()

#     return render(request, 'view_authors.html', {
#         'authors': authors,
#         'search_query': search_query  # Passing the query to keep it in the search box
#     })


def subscribe_plan(request, id):
    pass

def view_membership_plans(request):
    pass


def subscription_expiry_notifications(request):
    pass


def check_subscription_expiry():
    # Get all active subscriptions
    subscriptions = Subscription.objects.filter(status='active')
    
    for subscription in subscriptions:
        days_remaining = (subscription.end_date - now()).days
        if days_remaining <= 7:  # 7 days before expiration
            # Create a notification
            Notification.objects.create(
                user=subscription.user,
                message=f"Your subscription to the {subscription.plan.name} plan will expire in {days_remaining} days. Renew now!",
            )
            # Optionally, send an email
            send_mail(
                'Subscription Expiration Reminder',
                f'Your subscription to the {subscription.plan.name} plan will expire in {days_remaining} days. Renew now!',
                'no-reply@yourdomain.com',
                [subscription.user.email],
                fail_silently=False,
            )

def notify_new_book(sender, instance, created, **kwargs):
    if created:  # Only notify on new book creation
        users = User.objects.all()  # Notify all users
        message = f"New Book Alert: '{instance.title}' by {instance.author.name} is now available in our library!"
        for user in users:
            Notification.objects.create(user=user, message=message)


def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification.html', {'notifications': notifications})

def subscription_expiry_notifications(request):
    """Notify users whose subscriptions are about to expire."""
    user = request.user
    subscriptions = Subscription.objects.filter(user=user, end_date__lte=now() + timedelta(days=7))
    
    notifications = [
        {
            "message": f"Your subscription for {sub.plan.name} is about to expire on {sub.end_date}.",
            "expiry_date": sub.end_date
        }
        for sub in subscriptions
    ]

    return render(request,"notification.html",{"notifications": notifications})


def new_book_notifications(request):
    """Notify users about new book releases."""
    recent_books = Book.objects.filter(created_at__gte=now() - timedelta(days=30))  # Books added in the last 30 days
    
    notifications = [
        {
            "title": book.title,
            "author": book.author.name,
            "release_date": book.created_at,
            "description": book.description
        }
        for book in recent_books
    ]

    return render(request,"notification.html",{"notifications": notifications})


def all_notifications(request):
    """Aggregate all types of notifications."""
    subscription_notifications = subscription_expiry_notifications(request).content
    book_notifications = new_book_notifications(request).content

    return render(request,"notification.html",{
        "subscription_notifications": subscription_notifications,
        "book_notifications": book_notifications,
    })


@login_required
def user_dashboard(request):
    # Fetch active rentals for the user
    rentals = Rental.objects.filter(user=request.user, status='active')
    books = Book.objects.filter(availability=True)
    return render(request, 'dashboard.html', {'rentals': rentals, 'books': books})

@login_required
def rent_book(request, book_id):
    # Fetch the book to be rented
    book = get_object_or_404(Book, id=book_id, availability=True)

    # Check if the user has an active subscription
    subscription = Subscription.objects.filter(user=request.user, status='active').first()
    if not subscription:
        messages.error(request, "You need an active subscription to rent a book.")
        return redirect('user_dashboard')

    # Check if the user exceeds the max_books_allowed
    active_rentals = Rental.objects.filter(user=request.user, status='active').count()
    if active_rentals >= subscription.plan.max_books_allowed:
        messages.error(request, "You have reached the maximum allowed rentals for your plan.")
        return redirect('user_dashboard')

    # Create the rental record
    rental = Rental.objects.create(
        user=request.user,
        book=book,
        end_date=now() + timedelta(days=subscription.plan.max_rent_duration),
        status='active'
    )
    # Update book availability
    book.availability = False
    book.save()

    messages.success(request, f"You have successfully rented '{book.title}'.")
    return redirect('user_dashboard')

def rentals(request):
    user_rentals = Rental.objects.filter(user=request.user)
    return render(request, 'rentals.html', {'rentals': user_rentals})





