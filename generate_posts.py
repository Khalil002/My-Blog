"""
Generate script: creates ~50 lorem-ipsum posts per month for every month
between Jan 2020 and Dec 2025 (6 years x 12 months x 50 = 3,600 posts).

Run with:
    python3 manage.py shell < generate_posts.py
"""

import random
from datetime import datetime
from django.utils import timezone
from blog.models import Post

LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua ut enim ad minim "
    "veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat duis aute irure dolor in reprehenderit in voluptate "
    "velit esse cillum dolore eu fugiat nulla pariatur excepteur sint "
    "occaecat cupidatat non proident sunt in culpa qui officia deserunt "
    "mollit anim id est laborum"
).split()


def lorem_words(n):
    return " ".join(random.choice(LOREM_WORDS) for _ in range(n))


def lorem_title():
    return lorem_words(random.randint(4, 8)).capitalize()


def lorem_paragraph():
    sentence_count = random.randint(3, 6)
    sentences = []
    for _ in range(sentence_count):
        sentence = lorem_words(random.randint(8, 16))
        sentences.append(sentence.capitalize() + ".")
    return " ".join(sentences)


def lorem_content():
    paragraph_count = random.randint(3, 5)
    return "\n\n".join(lorem_paragraph() for _ in range(paragraph_count))


POSTS_PER_MONTH = 1

posts_to_create = []

for year in range(2000, 2026):
    for month in range(1, 13):
        # number of days in this month
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        days_in_month = (next_month - datetime(year, month, 1)).days

        for _ in range(POSTS_PER_MONTH):
            day = random.randint(1, days_in_month)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            pub_date = timezone.make_aware(
                datetime(year, month, day, hour, minute, second)
            )
            posts_to_create.append(
                Post(
                    title=lorem_title(),
                    content=lorem_content(),
                    pub_date=pub_date,
                )
            )

Post.objects.bulk_create(posts_to_create, batch_size=500)
print(f"Created {len(posts_to_create)} posts.")
