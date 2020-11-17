from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class TelegramUser(models.Model):
    bot_chatid   = models.PositiveIntegerField(unique=True, primary_key=True)
    bot_state    = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=1)
    object_score = models.PositiveIntegerField(validators=[MaxValueValidator(10)], default=0)
    #https://api.telegram.org/file/bot<token>/<file_path>
    photo_path   = models.CharField(max_length=512, default='file_path')
    comment      = models.TextField(default='')

    def __str__(self):
        return "chatid " + str(self.bot_chatid)
