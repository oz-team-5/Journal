from tortoise import fields, models


class Diary(models.Model):
    id = fields.IntField(pk=True)
    # 외래키: User와 연결 (1:N 관계)
    user = fields.ForeignKeyField(
        "models.User", related_name="diaries", on_delete=fields.CASCADE
    )
    title = fields.CharField(max_length=200)
    content = fields.TextField(min_length=1)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True) #updated_at 변수명 변경

    class Meta:
        table = "diaries"
        indexes = (("user_id", "id"),)  # SQL의 idx_user_diary 반영
