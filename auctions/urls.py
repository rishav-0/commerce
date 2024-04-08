from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListing,name='create'),
    path("category",views.displaycategory,name='category'),
    path('listing/<int:id>/',views.listing,name='listing'),  #displays individual listing page
    path('removeFromWatchlist/<int:id>/',views.removeFromWatchlist,name="removeFromWatchlist"),
    path('addtoWatchlist/<int:id>/',views.addtoWatchlist,name="addtoWatchlist"),
    path('watchlist',views.watchList,name="watchlist"),
    path('addComment/<int:id>',views.addComment,name="addComment"),
    path('addBid/<int:id>',views.addBid,name="addBid"),
    path('closeAuction/<int:id>',views.closeAuction,name="closeAuction"),
]
