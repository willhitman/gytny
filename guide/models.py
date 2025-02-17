from django.db import models
from AuthAccounts.models import User


class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)  # Changed to ForeignKey

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} {self.address}'


class Route(models.Model):
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)  # Changed to ForeignKey

    taxi_rank_name = models.CharField(max_length=200)
    bus_stop = models.CharField(max_length=100)
    distance = models.FloatField()
    fare = models.FloatField()

    likes = models.ManyToManyField('Like', related_name='route_likes')
    dislikes = models.ManyToManyField('DisLike', related_name='route_dislikes')
    shares = models.ManyToManyField('Share', related_name='route_shares')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.user.username} {self.taxi_rank_name}'  # Updated to access the username through the Guide model


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.username


class DisLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dislikes')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shares')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    country = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    surburd = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.country} {self.province}'
