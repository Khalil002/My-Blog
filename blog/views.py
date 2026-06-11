import calendar

from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from .models import Post

POSTS_PER_MONTH_PREVIEW = 5
POSTS_PER_PAGE = 10

# SQLite (and most DBs) store integers as signed 64-bit values. URL
# converters like <int:...> only guarantee a non-negative number, so very
# large values (e.g. /blog/post/999999999999999999999999/) must be rejected
# before they ever reach the database to avoid an OverflowError -> 500.
MAX_SAFE_INT = 2**63 - 1

def _earliest_year():
    """Return the earliest year that has a post, or None if there are no posts."""
    first = Post.objects.dates("pub_date", "year", order="ASC").first()
    return first.year if first else None

def index(request):
    latest_post_list = Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    context = {"latest_post_list": latest_post_list}
    return render(request, "blog/index.html", context)

def archive_index(request):
    """Top-level archive: list of years that have posts, with post counts."""
    years = Post.objects.dates("pub_date", "year", order="DESC")

    year_data = []
    for year_date in years:
        year = year_date.year
        count = Post.objects.filter(pub_date__year=year).count()
        display_count = "9999+" if count > 9999 else str(count)
        year_data.append({"year": year, "count": count, "display_count": display_count})

    context = {"year_data": year_data}
    return render(request, "blog/archive_index.html", context)

def not_found(request, message):
    """Render a friendly 'does not exist' page with a 404 status."""
    return render(request, "blog/not_found.html", {"message": message}, status=404)

def archive_year(request, year):
    """All posts published in a given year, grouped by month."""
    if year > MAX_SAFE_INT:
        return not_found(request, "The archive does not exist.")

    earliest_year = _earliest_year()
    current_year = timezone.now().year
    if earliest_year is None or year < earliest_year or year > current_year:
        return not_found(request, "The archive does not exist.")

    posts = Post.objects.filter(pub_date__year=year).order_by("-pub_date")

    months = Post.objects.filter(pub_date__year=year).dates(
        "pub_date", "month", order="DESC"
    )

    grouped = []
    for month_date in months:
        month_posts = [p for p in posts if p.pub_date.month == month_date.month]
        grouped.append({
            "month_date": month_date,
            "posts": month_posts[:POSTS_PER_MONTH_PREVIEW],
            "has_more": len(month_posts) > POSTS_PER_MONTH_PREVIEW,
        })

    context = {
        "year": year,
        "grouped": grouped,
        "post_count": posts.count(),
    }
    return render(request, "blog/archive_year.html", context)

def archive_month(request, year, month):
    """All posts published in a given year and month, paginated."""
    if year > MAX_SAFE_INT or month > MAX_SAFE_INT:
        return not_found(request, "The archive does not exist.")

    earliest_year = _earliest_year()
    current_year = timezone.now().year
    if earliest_year is None or year < earliest_year or year > current_year:
        return not_found(request, "The archive does not exist.")

    if month < 1 or month > 12:
        return not_found(request, "The archive does not exist.")

    posts = Post.objects.filter(
        pub_date__year=year, pub_date__month=month
    ).order_by("-pub_date")

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current = page_obj.number
    last = paginator.num_pages
    page_numbers = sorted({1, current - 1, current, current + 1, last} & set(range(1, last + 1)))

    # Build the list of items to render, inserting "..." for gaps.
    page_links = []
    for i, num in enumerate(page_numbers):
        if i > 0 and num != page_numbers[i - 1] + 1:
            page_links.append("...")
        page_links.append(num)

    context = {
        "year": year,
        "month": month,
        "posts": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "page_links": page_links,
    }
    return render(request, "blog/archive_month.html", context)

def archive_day(request, year, month, day):
    """All posts published on a given day."""
    if year > MAX_SAFE_INT or month > MAX_SAFE_INT or day > MAX_SAFE_INT:
        return not_found(request, "The archive does not exist.")

    earliest_year = _earliest_year()
    current_year = timezone.now().year
    if earliest_year is None or year < earliest_year or year > current_year:
        return not_found(request, "The archive does not exist.")

    if month < 1 or month > 12:
        return not_found(request, "The archive does not exist.")

    days_in_month = calendar.monthrange(year, month)[1]
    if day < 1 or day > days_in_month:
        return not_found(request, "The archive does not exist.")

    posts = Post.objects.filter(
        pub_date__year=year, pub_date__month=month, pub_date__day=day
    ).order_by("-pub_date")

    context = {
        "year": year,
        "month": month,
        "day": day,
        "posts": posts,
    }
    return render(request, "blog/archive_day.html", context)

def detail(request, post_id):
    if post_id > MAX_SAFE_INT:
        return not_found(request, "This post does not exist.")

    post = Post.objects.filter(pk=post_id, pub_date__lte=timezone.now()).first()
    if post is None:
        return not_found(request, "This post does not exist.")

    comments = post.comment_set.order_by("created_date")

    prev_post = (
        Post.objects.filter(pub_date__lt=post.pub_date,  pub_date__lte=timezone.now()).order_by("-pub_date").first()
    )
    next_post = (
        Post.objects.filter(pub_date__gt=post.pub_date,  pub_date__lte=timezone.now()).order_by("pub_date").first()
    )

    context = {
        "post": post,
        "comments": comments,
        "prev_post": prev_post,
        "next_post": next_post,
    }
    return render(request, "blog/detail.html", context)




