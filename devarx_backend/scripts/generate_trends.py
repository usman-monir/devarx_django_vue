import django
import os
import sys
from collections import Counter
from django.utils import timezone
from datetime import timedelta

sys.path.append(os.path.join( os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devarx_backend.settings')
django.setup()

from post.models import Post, Trend

trends = []

for trend in Trend.objects.all():
    trend.delete()

def extract_hastags(text, trends):
    for word in text.split():
        word = word.lower()
        if word[0] == '#':
            trends.append(word[1:])
            print(trends)
    return trends


current_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
day = current_hour - timedelta(hours = 24)


for post in Post.objects.filter(created_at__gte=day):
    extract_hastags(post.body, trends)

for trend in Counter(trends).most_common(10):
    Trend.objects.create(hashtag= trend[0], occurences= trend[1])

