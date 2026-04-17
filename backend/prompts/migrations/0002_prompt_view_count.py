from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prompts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prompt',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
