from django.contrib.contenttypes.models import ContentType


def update_item(instance, user_id, group_id, tags=""):
    from post.models import Item
    content_type = ContentType.objects.get_for_model(instance)
    try:
        item = Item.objects.get(content_type=content_type, object_id=instance.pk)
    except Item.DoesNotExist:
        item = Item(content_type=content_type, object_id=instance.pk)

    item.author_id = user_id
    item.group_id = group_id
    item.tags = tags
    item.save()
    return item

