from tortoise import fields, models


class Quote(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.CharField(max_length=100, default="Unknown")

    class Meta:
        table = "quotes"
