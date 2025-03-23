from django.db import models
from django.contrib.postgres.fields import ArrayField

class TopicsTextChoices(models.TextChoices):
  (0, 'language_learning')
  (1, 'mathematics')
  (2, 'statistics')
  (3, 'natural_sciences')
  (4, 'computer_science_fundamentals')
  (5, 'electrical_engineering')
  (6,'computer_science_(advanced_topics)')
  (7, 'tutorials')
  (8, 'blog')
  (9, 'miscellaneous')  

class Sources(models.Model):    
  id = models.AutoField("id", primary_key=True, serialize=True)
  topic = ArrayField(models.TextField(choices=TopicsTextChoices), null=False)
  content = models.TextField("content", unique=False, null=False)
  removeLater = models.BooleanField("remove later", default=False)