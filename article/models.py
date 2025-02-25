from django.db import models

# Create your models here.
class Article(models.Model):
    qiita_id = models.CharField(max_length=100, unique=True)  # 🔹 Qiita API の記事ID（ユニーク）
    title = models.CharField(max_length=255)
    url = models.TextField()
    tag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title