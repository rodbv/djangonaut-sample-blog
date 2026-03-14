import random

import lorem
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tqdm import tqdm

from blog.models import Blog, Comment, Post

User = get_user_model()


class Command(BaseCommand):
    help = "Create N lorem ipsum posts for the first available blog"

    def add_arguments(self, parser):
        parser.add_argument(
            "-q",
            "--quantity",
            type=int,
            default=5,
            help="Number of posts to create (default: 5)",
        )
        parser.add_argument(
            "-c",
            "--comments",
            type=int,
            default=0,
            help="Maximum number of comments per post; each post gets a random number from 1 to N (default: 0)",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Remove the first existing blog before creating posts",
        )

    def handle(self, *args, **options):
        quantity = options["quantity"]

        user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )

        # use first blog or create one if it doesn't exist
        blog = Blog.objects.first()
        if options["clean"] and blog:
            blog_name = blog.name
            blog.delete()
            self.stdout.write(f"Deleted existing blog: {blog_name}")
            blog = None

        if not blog:
            blog = Blog.objects.create(
                name="First Blog",
                description=lorem.paragraph(),
                created_by=user,
            )
            self.stdout.write(f"Created new blog: {blog.name}")

        num_comments = options["comments"]

        # create posts with progress bar
        for _ in tqdm(range(quantity), desc="Creating posts"):
            post = Post.objects.create(
                blog=blog,
                title=lorem.sentence().rstrip(".")[:300],
                content=lorem.text(),
                created_by=user,
            )
            comments_for_post = (
                random.randint(1, num_comments) if num_comments > 0 else 0
            )
            for _ in range(comments_for_post):
                Comment.objects.create(
                    post=post,
                    content=lorem.sentence(),
                    created_by=user,
                )

        self.stdout.write(
            self.style.SUCCESS(f"Created {quantity} posts in '{blog.name}'")
        )
