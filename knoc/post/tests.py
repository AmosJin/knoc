from django.test import TestCase
from django.contrib.auth.models import User
from post.models import Group, UserGroup, Link, Note
from post.core import update_item


class BasicTest(TestCase):
    fixtures = ['user.json', 'group.json', 'link.json', 'note.json', 'user_group.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()

 
class ItemUpdateTest(BasicTest):
    def setUp(self):
        super(ItemUpdateTest, self).setUp()
        self.group = Group.objects.get(pk=1)

    def test_create_item(self):
        user = self.user
        group = self.group
        link = Link(title="link title", description="some description", 
                link="http://www.shanbay.com", image="http://qstatic.shanbay.com/static//img/logo2.png")
        link.save()
        item = update_item(link, user_id=user.pk, group_id=group.pk)
        self.assertEqual(item.object_id, link.pk)

    def test_update_item(self):
        link = Link.objects.get(id=1)
        item = update_item(link, user_id=self.user.pk, group_id=self.group.id)
        self.assertEqual(item.object_id, link.id)
