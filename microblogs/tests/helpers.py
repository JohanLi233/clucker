from django.urls import reverse
from microblogs.models import Post

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

def create_post(author, from_count, to_count):
    for count in range (from_count, to_count):
        text = f'Post__{count}'
        post = Post(author=author, text=text)
        post.save()
