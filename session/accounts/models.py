from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    # 소프트 삭제 여부
    is_deleted = models.BooleanField(default=False)
    # 삭제 일시
    deleted_at = models.DateTimeField(null=True, blank=True)
    restore_answer = models.CharField(max_length=100, default="restore_answer")

    @staticmethod
    def get_user_or_none_by_username(username):
        try:
            return User.objects.get(username=username)
        except:
            return None

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, restore_answer):
        if self.restore_answer != restore_answer:
            return False
        self.is_deleted = False
        self.deleted_at = None
        self.restore_answer = None
        self.save()
