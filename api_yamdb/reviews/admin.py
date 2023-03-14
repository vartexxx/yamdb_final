from django.contrib import admin

from .models import Comment, Review, Category, Title, Genre, GenreTitle


admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(GenreTitle)
