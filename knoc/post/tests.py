from django.test import TestCase
from django.test.client import Client 
from django.contrib.auth.models import User

from post.models import Group, UserGroup, Link, Note
from post import core


class BasicTest(TestCase):
    fixtures = ['user.json', 'group.json', 'link.json', 'note.json', 'user_group.json', 'item.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()

 
class LinkInfoTest(BasicTest):
    def test_get_encoding(self):
		print 'test get_encoding ...'
		content = """ 
				<!DOCTYPE html>
                  <html id="spLianghui">\n<head>\n<meta http-equiv="Content-Type" 
                  content="text/html; charset=gb2312" /
				  """

		encode = core.get_encoding(content)
		self.assertEqual(encode, "gb2312")

    def test_get_domain(self):
		print 'test get_domain ...'
		domain = core.get_url_domain("http://www.shanbay.com/test/more")
		self.assertEqual("http://www.shanbay.com/", domain)

		domain = core.get_url_domain("http://www.scipark.net/news/sci_xp542.html")
		self.assertEqual("http://www.scipark.net/", domain)

    def test_link_info(self):
		print 'test link info...'
		content = """ 
            <html>
                <head>
                    <title>title</title>
                    <meta name="copyright" content="shanbay">
                    <meta name="description" content="description">
                </head>
                <body>
                    <div>some text</div>
                    <img src="http://qstatic.shanbay.com/static/img/landing_page_logo.png"/>
                </body>
            </html>
			"""
		data = core.get_link_info("http://www.shanbay.com", content)
		self.assertEqual("title", data["title"])
		self.assertEqual("description", data["description"])
		self.assertEqual("http://qstatic.shanbay.com/static/img/landing_page_logo.png", data["image"])
		# img url alter to "//qstatic.shanbay.com/..."
		# this equals to "http://qstatic.shanbay.com/..."
		content = """ 
            <html>
                <head>
                    <title>title</title>
                    <meta name="copyright" content="shanbay">
                    <meta name="description" content="description">
                </head>
                <body>
                    <div>some text</div>
                    <img src="//qstatic.shanbay.com/static/img/landing_page_logo.png"/>
                </body>
            </html>
			"""
		self.assertEqual("http://qstatic.shanbay.com/static/img/landing_page_logo.png", data["image"])

class ItemUpdateTest(BasicTest):
    def setUp(self):
		print 'test ItemUpdate...'
		super(ItemUpdateTest, self).setUp()
		self.group = Group.objects.get(pk=1)

    def test_create_item(self):
		print 'test create_item...'
		user = self.user
		group = self.group
		link = Link(title="link title", description="some description", 
                link="http://www.shanbay.com", image="http://qstatic.shanbay.com/static/img/logo2.png")
		link.save()
		item = core.update_item(link, user_id=user.pk, group_id=group.pk)
		self.assertEqual(item.object_id, link.pk)

    def test_update_item(self):
		print 'test update_item...'
		link = Link.objects.get(id=1)
		item = core.update_item(link, user_id=self.user.pk, group_id=self.group.id)
		self.assertEqual(item.object_id, link.id)

class ApiViewTest(BasicTest):
	def setUp(self):
		print 'test ApiView...'
		self.client = Client()
		self.client.login(username='test_user', password='1234567')

	def test_group_view(self):
		print 'testing group view...'
		print 'testing group get method...'
		res = self.client.get('/api/post/group/')
		self.assertEqual(len(res.data['data']), 4)
		groups = set(['shanbay', 'py', 'Android', 'iOS'])
		assert_groups = set([data['name'] for data in res.data['data']])
		self.assertEqual(groups, assert_groups)

	def test_item_view(self):
		print 'testing item view...'
		print 'testing item get method...'
		res = self.client.get('/api/post/item/3/')
		self.assertEqual(len(res.data['data']['items']), 1)
		self.assertEqual(res.data['data']['items'][0]['title'], 'Writing your first patch for Django')
		self.assertEqual(res.data['data']['items'][0]['item_type'], 'note')
		author_info = {'username': 'test_user', 'id': 1}
		self.assertEqual(res.data['data']['items'][0]['author_info'], author_info)

	def test_link_post(self):
		print 'testing link view...'
		print 'testing link post method...'
		link_data = {
				'link': u'http://www.baidu.com/'
				}
		res = self.client.post('/api/post/link/3/', link_data)
		self.assertEqual(res.data['status_code'], 0)
		self.assertEqual(res.data['data']['author_info']['username'], 'test_user')
		link = list(Link.objects.all())[-1]
		self.assertEqual(link_data['link'], link.link)

	def test_note_post(self):
		print 'testing note view...'
		print 'testing note post...'
		note_form = {
				'title': 'note_test',
				'summary': 'note summary',
				'content': 'note content'
				}
		res = self.client.post('/api/post/note/1/', {})
		self.assertEqual(res.data['status_code'], 1)
		res = self.client.post('/api/post/note/1/', note_form)
		self.assertEqual(res.data['status_code'], 0)
		self.assertEqual(res.data['data']['title'], 'note_test')
		self.assertEqual(res.data['data']['item_type'], 'note')
		self.assertEqual(res.data['data']['author_info']['username'], 'test_user')
