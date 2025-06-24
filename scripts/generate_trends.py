import django
import os
import sys
from collections import Counter
from django.utils import timezone
from datetime import timedelta

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
django.setup()


from post.models import Post, Trends


def extract_tag(text, trends):
    for word in text.split():
        if word[0] == '#':
            trends.append(word[1:])
            
    return trends

for trend in Trends.objects.all():
    trend.delete()

trends = []
this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)

for post in Post.objects.filter(created_at__gte=twenty_four_hours).filter(is_private=False):
    extract_tag(post.body, trends)

for trend in Counter(trends).most_common(10):
    Trends.objects.create(title=trend[0], accurences=trend[1])