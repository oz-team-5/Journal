from tortoise import fields, models


class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=500, index=True, unique=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="blacklisted_tokens", on_delete=fields.CASCADE
    )
    expired_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "token_blacklist"
