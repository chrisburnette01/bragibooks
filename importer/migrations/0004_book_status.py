# Generated by Django 4.1.4 on 2023-03-30 20:43

from django.db import migrations, models
import django.db.models.deletion

from importer.models import StatusChoices

def create_add_status(apps, _):
    Book = apps.get_model("importer", "Book")
    Status = apps.get_model("importer", "Status")

    for book in Book.objects.all():
        book.status = Status.objects.create(status=StatusChoices.DONE)
        book.save()

class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0003_delete_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('Done', 'Done'), ('Error', 'Error')], max_length=10)),
                ('message', models.TextField()),
            ],
        ),

        migrations.AddField(
            model_name='book',
            name='status',
            field=models.OneToOneField(to='importer.status', on_delete=django.db.models.deletion.CASCADE, null=True, default=None),
            preserve_default=False,
        ),

        migrations.RunPython(create_add_status, migrations.RunPython.noop),

        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.OneToOneField(to='importer.status', on_delete=django.db.models.deletion.CASCADE, null=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='dest_path',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='src_path',
            field=models.TextField(),
        ),
    ]
