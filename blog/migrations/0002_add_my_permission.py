from django.db import migrations
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def create_my_permission1(blog, schema_editor):
    model = blog.get_model('blog', 'Blog')
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.create(
        codename='Publish_Blog',
        name='Can Publish Blog',
        content_type=content_type,
    )


def create_my_permission2(blog, schema_editor):
    model = blog.get_model('blog', 'Blog')
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.create(
        codename='Draft_Blog',
        name='Can Draft Blog',
        content_type=content_type,
    )


def create_my_permission3(blog, schema_editor):
    model = blog.get_model('blog', 'Blog')
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.create(
        codename='Withdraw_Blog',
        name='Can Withdrawn Blog',
        content_type=content_type,
    )


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_my_permission1),
        migrations.RunPython(create_my_permission2),
        migrations.RunPython(create_my_permission3),
    ]
