import time
def log_blog_view(blog_id: int, username: str):
    with open("blog_views.log", "a") as f:
        f.write(f"[{time.ctime()}] Blog {blog_id} viewed by {username}\n")