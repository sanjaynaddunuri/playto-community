from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from community.models import Post, Comment, Like
from django.utils.timezone import now, timedelta
import random


class Command(BaseCommand):
    help = "Seed database with demo data"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding database...")

        # USERS
        users = []
        for i in range(1, 21):
            user, _ = User.objects.get_or_create(username=f"user{i}")
            users.append(user)

        self.stdout.write("✅ 20 users")

        # POSTS
        posts = []
        for i in range(1, 26):
            post = Post.objects.create(
                author=random.choice(users),
                content=f"Demo post {i}: This is a realistic community discussion post."
            )
            posts.append(post)

        self.stdout.write("✅ 25 posts")

        # COMMENTS + REPLIES
        comments = []
        for post in posts:
            for _ in range(3):
                parent = Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content="This is a top-level comment."
                )
                comments.append(parent)

                for _ in range(2):
                    reply = Comment.objects.create(
                        post=post,
                        author=random.choice(users),
                        parent=parent,
                        content="This is a reply."
                    )
                    comments.append(reply)

        self.stdout.write("✅ Nested comments")

        # LIKES (FOR LEADERBOARD)
        for user in users:
            for post in random.sample(posts, 5):
                like, created = Like.objects.get_or_create(
                    user=user,
                    post=post
                )
                like.created_at = now() - timedelta(hours=random.randint(0, 10))
                like.save()

            for comment in random.sample(comments, 4):
                like, created = Like.objects.get_or_create(
                    user=user,
                    comment=comment
                )
                like.created_at = now() - timedelta(hours=random.randint(0, 10))
                like.save()

        self.stdout.write(self.style.SUCCESS("🎉 DATABASE SEEDED SUCCESSFULLY"))
