from django.db import models


class ExpressionHistory(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    expression = models.TextField()
    result = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=7, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.expression
