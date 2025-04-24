from django.db import models
from django.contrib.postgres.fields import ArrayField

topicsList = ['language_learning','mathematics', 'statistics', 'natural_sciences', 'computer_science_fundamentals','electrical_engineering', 'computer_science_(advanced_topics)', 'tutorials', 'blog','miscellaneous']

class TopicsTextChoices(models.TextChoices):
  (0, topicsList[0])
  (1, topicsList[1])
  (2, topicsList[2])
  (3, topicsList[3])
  (4, topicsList[4])
  (5, topicsList[5])
  (6, topicsList[6])
  (7, topicsList[7])
  (8, topicsList[8])
  (9, topicsList[9])  

class Sources(models.Model):    
  id = models.AutoField("id", primary_key=True, serialize=True)
  topic = ArrayField(models.TextField(choices=TopicsTextChoices), null=False)
  content = models.TextField("content", unique=False, null=False)