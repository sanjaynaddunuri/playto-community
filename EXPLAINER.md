# 📘 EXPLAINER.md – Playto Community Feed

This document explains the **design decisions, data modeling, and query logic** used in the Playto Community Feed project.  
It directly answers the questions asked in the Playto Engineering Challenge.

---

## 1️⃣ The Tree – Nested Comments Design

### 🔹 How are nested comments modeled?

We used an **adjacency list model**.

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies"
    )
```

- Each comment optionally points to another comment (`parent`)
- This allows **unlimited nesting** (Reddit-style threads)
- The database schema remains simple and scalable

---

### 🔹 How is the comment tree fetched efficiently?

To avoid the **N+1 query problem**, we:

- Fetch all comments for a post in **bulk**
- Build the tree **in memory**, not via recursive SQL queries

```python
Post.objects.prefetch_related(
    Prefetch(
        "comments",
        queryset=Comment.objects.select_related("author").prefetch_related("replies")
    )
)
```

This ensures:
- Loading a post with 50+ nested comments does **not** trigger 50 SQL queries
- The database is hit only a small, predictable number of times

---

### 🔹 How is the tree serialized?

We use a **recursive serializer**:

```python
class RecursiveCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        return RecursiveCommentSerializer(obj.replies.all(), many=True).data
```

The recursion happens in Python memory, not in the database.

---

## 2️⃣ The Math – Leaderboard Calculation (Last 24 Hours)

### 🔹 Design Principle

We **do NOT store daily karma** on the User model.

Instead:
- Each Like is a **transaction/event**
- Karma is calculated dynamically from history

This avoids data inconsistency and supports arbitrary time windows.

---

### 🔹 Karma Rules

- Like on a **Post** → **5 Karma**
- Like on a **Comment** → **1 Karma**

---

### 🔹 Query Used for Leaderboard

```python
last_24h = now() - timedelta(hours=24)

leaderboard = (
    Like.objects
    .filter(created_at__gte=last_24h)
    .annotate(
        karma=Case(
            When(post__isnull=False, then=5),
            When(comment__isnull=False, then=1),
            output_field=IntegerField()
        )
    )
    .values("user__username")
    .annotate(total_karma=Sum("karma"))
    .order_by("-total_karma")[:5]
)
```

### 🔹 Why this works

- Filters likes to **last 24 hours only**
- Assigns karma per like dynamically
- Aggregates using SQL (efficient)
- No denormalized fields or cron jobs needed

---

## 3️⃣ Concurrency – Preventing Double Likes

### 🔹 Problem

Users must not be able to:
- Like the same post twice
- Like the same comment twice
- Inflate karma via race conditions

---

### 🔹 Solution

We enforce correctness at the **database level**.

```python
class Like(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_post_like"
            ),
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_comment_like"
            )
        ]
```

Additionally, likes are created inside a transaction:

```python
with transaction.atomic():
    Like.objects.create(...)
```

This guarantees:
- Even simultaneous requests cannot create duplicate likes
- Database remains the single source of truth

---

## 4️⃣ AI Audit – Example of AI Mistake & Fix

### 🔹 AI-Generated Suggestion (Rejected)

AI initially suggested:
- Storing a `daily_karma` integer field on the User model
- Incrementing it whenever a like occurs

### ❌ Why this is wrong
- Breaks the **last-24-hours** requirement
- Requires background jobs to reset values
- Leads to inconsistency if likes are deleted or backdated

---

### ✅ Corrected Solution

- Store likes as immutable events
- Compute karma dynamically using aggregation queries
- Filter by time window at query time

This approach is:
- More accurate
- Easier to reason about
- Scales naturally

---

## 5️⃣ Summary

| Requirement | Status |
|---|---|
| Threaded comments | ✅ |
| N+1 query avoidance | ✅ |
| Concurrency-safe likes | ✅ |
| Dynamic 24h leaderboard | ✅ |
| No cached karma fields | ✅ |

---

## 🏁 Final Note

This project was designed to prioritize:
- **Correctness**
- **Scalability**
- **Explainability**

Every architectural decision can be explained, debugged, and extended confidently.

---

**Author:** Naddunuri Sanjay  
**Project:** Playto Community Feed
