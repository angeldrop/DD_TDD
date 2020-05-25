from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html1(self):
        response=self.client.get('/')
        
        html=response.content.decode('utf8')
        self.assertTemplateUsed(response,'lists/home.html')