from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre
    extra = 2


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "category",
    )
    list_editable = (
        "year",
        "description",
        "category",
    )
    list_filter = ("year",)
    search_fields = (
        "name",
        "description",
    )
    list_display_links = ("name",)
    inlines = [
        TitleGenreInline,
    ]
    filter_horizontal = ("genre",)


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    inlines = (TitleInline,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "author", "score", "pub_date")

    list_editable = ("text", "author", "score")
    list_filter = ("title", "author", "score")
    inlines = [CommentInline]
    search_fields = ("title__name", "author__username", "text")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "text", "review", "pub_date")

    list_editable = ("text", "author")
    search_fields = ("review__text", "author__username", "text")
    list_display_links = ("review",)
    list_filter = ("review__title",)
