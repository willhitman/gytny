import secrets

from django.db import migrations

def generate_chat_id():
    return secrets.token_hex(4).upper()  # 8-char hex → 16-char when uppercase

def populate_ids(apps, schema_editor):
    ChatRoom = apps.get_model('community', 'ChatRoom')
    for room in ChatRoom.objects.all():
        if room.group_id == 'TEMP_ID':
            room.chat_id = generate_chat_id()
            room.save()

class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_remove_chatroom_group_id_chatroom_chat_id'),
    ]

    operations = [
        migrations.RunPython(populate_ids),
    ]
