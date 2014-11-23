from django.contrib.contenttypes.models import ContentType

from post.signals import  item_updated
from post.models import Item

def update_item(sender, instance, user, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    try:
        item = Item.objects.get(content_type=content_type, object_id=instance.pk)
    except Item.DoesNotExist:
        return

    item.save()

item_updated.connect(update_item)
