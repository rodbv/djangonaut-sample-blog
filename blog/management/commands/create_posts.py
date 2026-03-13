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
            help="Number of comments to add per post (default: 0)",
        )

    def handle(self, *args, **options):
        quantity = options["quantity"]

        user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )

        # use first blog or create one if it doesn't exist
        blog = Blog.objects.first()
        if not blog:
            blog = Blog.objects.create(
                name=lorem.sentence().rstrip(".")[:120],
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
            for _ in range(num_comments):
                Comment.objects.create(
                    post=post,
                    content=lorem.sentence(),
                    created_by=user,
                )

        self.stdout.write(self.style.SUCCESS(f"Created {quantity} posts in '{blog.name}'"))
