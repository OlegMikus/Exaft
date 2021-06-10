from django.db import models


class Organization(models.Model):
    title = models.CharField(max_length=100)
    creation_date = models.DateField(null=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


class Links(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    inst = models.URLField(null=True)
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    off_site = models.URLField(null=True)


class AreasOfActivity(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


class TopManagers(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
