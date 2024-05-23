from django.db import models


class PredResults(models.Model):
    objects = None
    gender = models.CharField(max_length=10)
    age = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    family_history_with_overweight = models.CharField(max_length=3)
    favc = models.CharField(max_length=3)
    fcvc = models.IntegerField()
    ncp = models.FloatField()
    caec = models.CharField(max_length=20)
    smoke = models.CharField(max_length=3)
    ch2o = models.FloatField()
    scc = models.CharField(max_length=3)
    faf = models.FloatField()
    tue = models.IntegerField()
    calc = models.CharField(max_length=20)
    mtrans = models.CharField(max_length=30)
    classification = models.CharField(max_length=50)

    def __str__(self):
        return self.classification
