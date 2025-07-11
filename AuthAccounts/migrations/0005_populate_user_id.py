from django.db import migrations, IntegrityError
import secrets

def generate_user_id():
    return secrets.token_hex(9).upper()

def populate_user_ids(apps, schema_editor):
    User = apps.get_model('AuthAccounts', 'User')
    for user in User.objects.all():
        while True:
            try:
                user.user_id = generate_user_id()
                user.save()
                break
            except IntegrityError:
                # If we hit a duplicate, try again
                continue

class Migration(migrations.Migration):
    dependencies = [
        ('AuthAccounts', '0004_add_user_id_field'),
    ]

    operations = [
        migrations.RunPython(populate_user_ids),
    ]