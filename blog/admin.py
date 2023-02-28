from django.contrib import admin
from .models import Blog, Magazine, Author
from django.utils.translation import ngettext
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .forms import AuthorForm
from .templatetags.blog_extras import truncatechars


@admin.display(description='Author')
def colored_author(obj):
    return format_html(
        '<span style="color: #{};">{}</span>',
        '009900',
        obj.author,
    )


@admin.display(description='Title')
def colored_title(obj):
    return format_html(
        '<span style="color: #{};">{}</span>',
        '009900',
        obj.title
    )


@admin.display(boolean=True)
def published(obj):
    return obj.status == "p"


@admin.display(description='Image')
def display_image(obj):
    return mark_safe('<img src="{}" width="60" />'.format(obj.cover_image.url))


@admin.action(description='Mark selected blogs as published')
def make_published(self, request, queryset):
    updated_blog = queryset.update(status='p')
    self.message_user(request, ngettext(
        '%d blog was successfully marked as published.',
        '%d blogs were successfully marked as published.',
        updated_blog,
    ) % updated_blog, messages.SUCCESS)


@admin.action(description='Mark selected blogs as draft')
def make_draft(self, request, queryset):
    updated_blog = queryset.update(status='d')
    self.message_user(request, ngettext(
        '%d blog was successfully marked as draft.',
        '%d blogs were successfully marked as draft.',
        updated_blog,
    ) % updated_blog, messages.SUCCESS)


@admin.action(description='Mark selected blogs as withdrawn')
def make_withdrawn(self, request, queryset):
    updated_blog = queryset.update(status='w')
    self.message_user(request, ngettext(
        '%d blog was successfully marked as withdrawn.',
        '%d blogs were successfully marked as withdrawn.',
        updated_blog,
    ) % updated_blog, messages.SUCCESS)


class BlogAdmin(admin.ModelAdmin):
    list_display = [colored_author, colored_title, 'magazine', published, display_image]
    list_display_links = (colored_author, colored_title, display_image)
    actions = [make_published, make_draft, make_withdrawn]
    fields = [field.name for field in Blog._meta.get_fields()]
    readonly_fields = ('id', 'publish_date')
    date_hierarchy = 'publish_date'
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(BlogAdmin, self).get_queryset(request)
        if request.user.is_staff:
            return qs.all()
        return qs.filter(author_id=request.user.id)


class BlogInline(admin.StackedInline):
    model = Blog
    extra = 0


class MagazineAdmin(admin.ModelAdmin):
    list_display = ['id', 'colored_title', 'publish_date', 'truncated_description']
    list_display_links = ('colored_title', 'truncated_description')
    inlines = (BlogInline,)
    readonly_fields = ('id', 'publish_date')
    search_fields = ['title']

    @admin.display(description='Description')
    def truncated_description(self, obj):
        result = obj.description[:20] + '...' if len(obj.description) > 50 else obj.description
        return format_html(
            '<span style="color: #{};">{}</span>',
            '000000',
            result
        )

    @admin.display(description='Title')
    def colored_title(self, obj):
        return format_html(
            '<span style="color: #{};">{}</span>',
            '000000',
            obj.title
        )


@admin.display(description='Image')
def display_image(obj):
    return mark_safe('<img src="{}" width="60" />'.format(obj.profile_image.url))


@admin.display(description='Name')
def colored_name(obj):
    return format_html(
        '<span style="color: #{};">{}</span>',
        '009900',
        obj.name
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', colored_name, 'email_field', display_image]
    form = AuthorForm
    list_display_links = (colored_name, display_image)
    readonly_fields = ('id',)
    search_fields = ['name']

    @admin.display(description='Email')
    def email_field(self, obj):
        return format_html('<a href="mailto:{}/">{}</a>', obj.email, obj.email)



admin.site.register(Blog, BlogAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(Author, AuthorAdmin)

admin.site.index_title = "Magazine"
admin.site.site_header = "Khaled site"
admin.site.site_title = "Magazine"
