from tortoise import fields, models


class Question(models.Model):
    id = fields.IntField(pk=True)
    question_text = fields.CharField(max_length=500)

    class Meta:
        table = "questions"
