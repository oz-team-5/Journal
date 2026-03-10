from tortoise import fields, models


class UserQuestion(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="received_questions", on_delete=fields.CASCADE
    )
    question = fields.ForeignKeyField("models.Question", related_name="assigned_users")
    received_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_questions"
