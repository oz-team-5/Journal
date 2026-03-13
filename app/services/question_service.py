import random
from typing import Optional


class QuestionService:
    # 서비스 코드 내부에 질문 리스트를 미리 선언합니다.
    # 나중에 질문이 많아지면 별도의 JSON 파일로 분리해도 좋습니다.
    QUESTIONS = [
        "오늘 당신의 마음을 가장 편안하게 해준 순간은 언제였나요?",
        "오늘 하루 중 가장 기억에 남는 대화는 무엇이었나요?",
        "지금 이 순간, 당신이 가장 감사하게 느끼는 것 세 가지는?",
        "오늘의 당신에게 점수를 준다면 몇 점인가요? 그 이유는?",
        "어떤 일이 당신을 오늘 가장 많이 웃게 만들었나요?",
        "오늘 마주한 도전 중 당신을 가장 성장시킨 것은 무엇인가요?",
        "내일의 나에게 꼭 해주고 싶은 격려의 한마디는?",
        "오늘 하루 동안 당신이 발견한 작은 아름다움은 무엇인가요?",
        "오늘 본인 스스로가 가장 자랑스러웠던 순간이 있었나요?",
        "지금 당신의 기분을 한 단어로 표현한다면 무엇인가요?"
    ]

    async def get_random_question(self) -> Optional[str]:
        """
        리스트에 정의된 질문 중 하나를 무작위로 선택하여 반환
        """
        if not self.QUESTIONS:
            return None

        # random.choice를 사용하면 리스트에서 하나를 랜덤으로 뽑기
        return random.choice(self.QUESTIONS)


question_service = QuestionService()