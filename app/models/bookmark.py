from tortoise import fields, models


class Bookmark(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="bookmarks", on_delete=fields.CASCADE
    )
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarked_by")

    class Meta:
        table = "bookmarks"
