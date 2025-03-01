from django.urls import path
from . import views
from .views import add_book

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.landing_page, name='dashboard'),  # Redirect to this after login, if role isn't used yet
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('librarian-dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('add/', views.add_book, name='add_book'),
    path('books/', views.list_books, name='list_books'),
    path('books/view/<int:book_id>', views.view_book_details, name='view_book_details'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('authors/', views.view_authors, name='view_authors'),
    path('authors/add/', views.add_author, name='add_author'),
    path('authors/update/<int:author_id>/', views.  update_author, name='update_author'),
    path('authors/delete/<int:author_id>/', views.delete_author, name='delete_author'),
    path('categories/', views.view_categories, name='view_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/update/<int:genre_id>/', views.edit_category, name='update_category'),
    path('categories/delete/<int:genre_id>/', views.delete_category, name='delete_category'),
    path('add-modal_author/', views.add_modal_author, name='add_modal_author'),
    path('plans/', views.view_plans, name='view_subscriptionplan'),
    path('plan/add', views.add_plan, name='add_plan'),
    path('plan/edit/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('plan/delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('home/', views.view_books, name='view_books'),
    path('search/', views.book_search, name='book_search'),
    path('membership-plans/', views.view_membership_plans, name='membership_plans'),
    path('logout/', views.logout_view, name='logout'),
    path('subscription/', views.subscription_plan_view, name='subscription_plan_view'),
    path('subscribe/<int:plan_id>/', views.subscribe_plan, name='subscribe_plan'),
    path('check_subscription_expiry/', views.check_subscription_expiry, name='check_subscription_expiry'),
    path('notifications/subscription-expiry/', views.subscription_expiry_notifications, name='subscription_expiry_notifications'),
    path('notifications/', views.new_book_notifications, name='new_book_notifications'),
    path('notifications/', views.all_notifications, name='all_notifications'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('rent/<int:book_id>/', views.rent_book, name='rent_book'),
    path('rentals/', views.rentals, name='rentals'),
    # path('return/<int:rental_id>/', views.return_book, name='return_book'),
    # path('renew/<int:rental_id>/', views.renew_rental, name='renew_rental')
    
    
]
