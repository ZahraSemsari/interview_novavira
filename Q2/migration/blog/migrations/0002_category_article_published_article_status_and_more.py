import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

def change_charfield_to_user(apps , schema_editor):
    Article = apps.get_model("blog" , "Article")
    User = apps.get_model( "account" , "User")
    for article in Article.objects.all():
        user = User.objects.get(username=article.author)
        article.author = str(user.pk)
        article.save(update_fields=["author"])

def get_exist_category(apps, schema_editor):
    Article = apps.get_model("blog", "Article")
    Category = apps.get_model("blog", "Category")

    for article in Article.objects.all():
        category_title = article.category
        if not category_title:
            article.category = None
            article.save(update_fields=["category"])
            continue

        new_category, created = Category.objects.get_or_create(title=category_title)

        article.category = str(new_category.pk)
        article.save(update_fields=["category"])


def set_old_articles_datetime(apps, schema_editor):
    Article = apps.get_model("blog", "Article")

    Article.objects.update(
        updated=models.F("created"),
        published=models.F("created"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            
            field=models.CharField(max_length=1,choices=[('p', 'publish'), ('d', 'draft')], default='p'),
        ),
        # migrations.AlterField(
        #     model_name='article',
        #     name='author',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        # ),
        # migrations.AlterField(
        #     model_name='article',
        #     name='category',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category'),
        # ),

        migrations.AddField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),

        migrations.RunPython(
            set_old_articles_datetime,
            migrations.RunPython.noop,
        ),

        migrations.RunPython(
            change_charfield_to_user,
            migrations.RunPython.noop,
        ),

        migrations.RunPython(
            get_exist_category,
            migrations.RunPython.noop,
        ),

        migrations.AlterField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        migrations.AlterField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.category",
            ),
        ),
    ]
