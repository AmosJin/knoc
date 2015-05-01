import re
from django.contrib.contenttypes.models import ContentType
from lxml import etree
from io import StringIO
from urlparse import urlparse

def update_item(instance, user_id, group_id, tags=""):
    from post.models import Item
    content_type = ContentType.objects.get_for_model(instance)
    try:
        item = Item.objects.get(content_type=content_type, object_id=instance.pk)
    except Item.DoesNotExist:
        item = Item(content_type=content_type, object_id=instance.pk)

    item.author_id = user_id
    item.group_id = group_id
    item.save()
    if tags:
        tags = tags.split(",")
        if len(tags) == 1:
            tags = tags[0].split()

        item.tags.set(*tags)
    return item

def get_encoding(content):
    match = re.search("charset=([a-z0-9]+)\"", content)
    if match:
        return match.group(1)
    return None


def get_url_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def get_link_info(link, content, encoding="utf8"):
    content = content.decode(encoding)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(content), parser)
    head = tree.find('head')
    title = head.find('title')
    title = title is not None and title.text or ""
    metas = head.findall('meta')
    description = ""
    for meta in metas:
        if meta.get('name') == "description":
            description = meta.get("content")
    data = {"title":title, "description":description}
    for image in tree.iter(tag="img"):
		image = image.get('src')
		if image.startswith("/"):
			if image.startswith("//"):
				image = image
			else:
				domain = get_url_domain(link)
				if domain.endswith("/"):
					domain = domain[:-1]
				image = domain + image
		if not image.startswith("http") and not image.startswith("//"):
			image = "".join([link, image])
		data["image"] =  image
		break
    data["link"] = link
    return data

