"""
Generate sample data:
  - 1 post per month from Jan 2000 to Nov 2025
  - 100 posts in December 2025
  - 5 comments from 5 different sample users on the latest post

Safe to run multiple times — skips entirely if posts already exist.

Run standalone:
    python generate_posts.py
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

import random
from datetime import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from blog.models import Comment, Post

# ── Guard ────────────────────────────────────────────────────────────────────
if Post.all_objects.exists():
    print("Posts already exist — skipping sample data generation.")
    exit(0)

# ── Lorem helpers ─────────────────────────────────────────────────────────────
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
    sentences = [
        lorem_words(random.randint(8, 16)).capitalize() + "."
        for _ in range(random.randint(3, 6))
    ]
    return " ".join(sentences)


def lorem_content():
    return "\n\n".join(lorem_paragraph() for _ in range(random.randint(3, 5)))


def random_pub_date(year, month):
    if month == 12:
        days_in_month = 31
    else:
        days_in_month = (datetime(year, month + 1, 1) - datetime(year, month, 1)).days
    return timezone.make_aware(datetime(
        year, month,
        random.randint(1, days_in_month),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    ))


# ── Posts: 1 per month Jan 2000 – Nov 2025 ───────────────────────────────────
posts_to_create = []

for year in range(2000, 2026):
    for month in range(1, 13):
        if year == 2025 and month == 12:
            continue  # handled separately below
        posts_to_create.append(Post(
            title=lorem_title(),
            content=lorem_content(),
            pub_date=random_pub_date(year, month),
        ))

# ── Posts: 100 in December 2025 ───────────────────────────────────────────────
for _ in range(100):
    posts_to_create.append(Post(
        title=lorem_title(),
        content=lorem_content(),
        pub_date=random_pub_date(2025, 12),
    ))

Post.all_objects.bulk_create(posts_to_create, batch_size=500)
print(f"Created {len(posts_to_create)} posts.")

# ── 5 sample users + comments on the latest post ─────────────────────────────
SAMPLE_USERS = ["alice", "bob", "carol", "dave", "eve"]
SAMPLE_PASSWORD = "samplepassword123"

users = []
for username in SAMPLE_USERS:
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(SAMPLE_PASSWORD)
        user.save()
    users.append(user)

latest_post = Post.all_objects.order_by("-pub_date").first()

comments = [
    Comment(
        post=latest_post,
        author=user.username,
        text=lorem_paragraph(),
    )
    for user in users
]
Comment.objects.bulk_create(comments)
print(f"Created {len(comments)} comments on '{latest_post.title}'.")
