from django.contrib import admin
from .models import Blog, Magazine, Author, Person, Car
from django.utils.translation import ngettext, get_language
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .forms import AuthorForm
from django.utils.translation import gettext_lazy as _


# from django.utils.functional import lazy
# from django.utils.translation import gettext_lazy as _
# mark_safe_lazy = lazy(mark_safe, str)
# example of how to use it
# lazy_string = mark_safe_lazy(_("<p>khaled</p>"))


@admin.display(description=_('Image'))
def display_image(obj):
    return mark_safe('<img src="{}" width="60" />'.format(obj.profile_image.url))


@admin.display(description=_('Name.'))
def colored_name(obj):
    return format_html(
        '<span style="color: #{};">{}</span>',
        '009900',
        obj.name
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = [colored_name, 'email_field', display_image]
    form = AuthorForm
    list_display_links = (colored_name, display_image)
    search_fields = ['name']

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser \
                or (obj is not None and request.user == obj.name) \
                or request.user.has_perm('blog.delete_author'):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser \
                or (obj is not None and request.user == obj.name) \
                or request.user.has_perm('blog.change_author'):
            return True
        return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm('blog.add_author'):
            return True
        return False

    def has_view_permission(self, request, obj=None):
        qs = super().get_queryset(request)
        # exists = qs.filter(name=request.user)
        # if request.user.is_superuser or exists:
        # queryset = Author.objects.get(name=request.user)
        # if request.user.is_superuser or queryset:
        # if request.user.is_superuser or self.get_queryset(request).exists() or request.user.has_perm('blog.view_author'):
        if request.user.is_superuser or request.user.has_perm('blog.view_author'):
            return True
        return False

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser \
    #             or (obj is not None and request.user == obj.name) \
    #             or request.user.has_perm('blog.change_author'):
    #         readonly_fields = ()
    #     else:
    #         readonly_fields = ('name', 'email', 'bio', 'bio_ar', 'profile_image')
    #     return readonly_fields

    @admin.display(description=_('Email'))
    def email_field(self, obj):
        return format_html('<a href="mailto:{}/">{}</a>', obj.email, obj.email)


@admin.display(description=_('Author'))
def colored_author(obj):
    author = obj.author
    return format_html(
        '<span style="color: #{};">{}</span>',
        '009900',
        author,
    )


@admin.display(description=_('Title.'))
def colored_title(obj):
    language = get_language()
    if language == "ar":
        title = obj.title_ar
    else:
        title = obj.title
    return format_html(
        '<span style="color: #{};">{}</span>',
        '009900',
        title
    )


@admin.display(description=_("Publish."), boolean=True)
def published(obj):
    return obj.status == "p"


@admin.display(description=_('Image'))
def display_image(obj):
    return mark_safe('<img src="{}" width="60" />'.format(obj.cover_image.url))


@admin.action(description=_('Mark selected blogs as published'))
def make_published(self, request, queryset):
    updated_blog = queryset.update(status='p')
    self.message_user(request, ngettext(
        '%d blog was successfully marked as published.',
        '%d blogs were successfully marked as published.',
        updated_blog,
    ) % updated_blog, messages.SUCCESS)


@admin.action(description=_('Mark selected blogs as draft'))
def make_draft(self, request, queryset):
    updated_blog = queryset.update(status='d')
    self.message_user(request, ngettext(
        '%d blog was successfully marked as draft.',
        '%d blogs were successfully marked as draft.',
        updated_blog,
    ) % updated_blog, messages.SUCCESS)


@admin.action(description=_('Mark selected blogs as withdrawn'))
def make_withdrawn(self, request, queryset):
    updated_blog = queryset.update(status='w')
    self.message_user(request, ngettext(
        '%d blog was successfully marked as withdrawn.',
        '%d blogs were successfully marked as withdrawn.',
        updated_blog,
    ) % updated_blog, messages.SUCCESS)

@admin.display(description=_('Your blogs'))
def get_my_blogs(obj, request):
    return obj.filter(author_id=request.user.id)

class BlogAdmin(admin.ModelAdmin):
    list_display = [colored_author, colored_title, 'magazine', published, display_image]
    list_display_links = (colored_author, colored_title, display_image)
    # actions = [make_published, make_draft, make_withdrawn]
    exclude = ("id", 'publish_date')
    date_hierarchy = 'publish_date'
    search_fields = ['title']
    list_filter = ['author']

    # def get_queryset(self, request):
    #     qs = super(BlogAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs.all()
    #     return qs.filter(author_id=request.user.id)

    # def get_list_filter(self, request):
    #     if self.get_queryset(request).exists():
    #         return [get_my_blogs]

    def get_actions(self, request, obj=None):
        actions = super().get_actions(request)
        if request.user.is_superuser \
                or (obj is not None and request.user == obj.author.name) \
                or request.user.has_perm("blog.Withdraw_Blog") \
                or request.user.has_perm("blog.Draft_Blog") \
                or request.user.has_perm("blog.Publish_Blog"):
            actions[make_withdrawn.__name__] = (make_withdrawn, make_withdrawn.__name__,
                                                'Mark selected blogs as withdrawn')
            actions[make_draft.__name__] = (make_draft, make_draft.__name__,
                                            'Mark selected blogs as draft')
            actions[make_published.__name__] = (make_published, make_published.__name__,
                                                'Mark selected blogs as published')
        return actions

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser \
                or (obj is not None and request.user == obj.author.name) \
                or request.user.has_perm('blog.change_blog'):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser \
                or (obj is not None and request.user == obj.author.name) \
                or request.user.has_perm('blog.delete_blog'):
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser \
                or (obj is not None and request.user == obj.author.name) \
                or request.user.has_perm('blog.view_blog'):
            return True
        return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm('blog.add_blog'):
            return True
        return False


class BlogInline(admin.StackedInline):
    model = Blog
    extra = 0


class MagazineAdmin(admin.ModelAdmin):
    list_display = ['colored_title', 'publish_date', 'truncated_description']
    list_display_links = ('colored_title', 'truncated_description')
    inlines = (BlogInline,)
    search_fields = ['title']

    @admin.display(description=_('Description.'))
    def truncated_description(self, obj):
        language = get_language()
        if language == "ar":
            result = obj.description_ar[:20] + '...' if len(obj.description) > 50 else obj.description
        else:
            result = obj.description[:20] + '...' if len(obj.description) > 50 else obj.description
        return format_html(
            '<span style="color: #{};">{}</span>',
            '000000',
            result
        )

    @admin.display(description=_('Title.'))
    def colored_title(self, obj):
        language = get_language()
        if language == "ar":
            title = obj.title_ar
        else:
            title = obj.title
        return format_html(
            '<span style="color: #{};">{}</span>',
            '000000',
            title
        )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm('blog.change_magazine'):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm('blog.delete_magazine'):
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm('blog.view_magazine'):
            return True
        return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm('blog.add_magazine'):
            return True
        return False


admin.site.register(Blog, BlogAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(Author, AuthorAdmin)

admin.site.index_title = _("Magazine")
admin.site.site_header = _("Khaled site")
admin.site.site_title = _("Magazine")
