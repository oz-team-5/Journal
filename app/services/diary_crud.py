from app.models.diary import Diary


# 일기 저장
async def create_diary(user_id: int, title: str, content: str):
    return await Diary.create(user_id=user_id, title=title, content=content)


# 일기 수정
async def update_diary(
    diary_id: int, user_id: int, title: str = None, content: str = None
):
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)

    if diary:
        # 값이 들어왔을 때, None이 아닐 때만 수정(수정을 안하는경우)
        if title is not None:
            diary.title = title
        if content is not None:
            diary.content = content

        # 수정본 저장하기(SQLAlchemy = commit()이랑 같음)
        await diary.save()
        return True

    return False


# 일기 삭제
async def delete_diary(diary_id: int, user_id: int):
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)

    if diary:
        await diary.delete()
        return True

    return False


# 일기 목록 조회, 검색/정렬/페이징(1페이지당 10개 노출)


async def get_diaries(user_id: int, keyword: str = None, page: int = 1, size: int = 10):
    # 사용자 id만 필터링
    query = Diary.filter(user_id=user_id)

    # 검색어 키워드 내용에서 찾기
    if keyword:
        query = query.filter(content__contains=keyword)

    # 페이징 계산(ex)1페이지는 1~10, 2페이지는 11~20까지 노출)
    offset = (page - 1) * size

    # 실행순서 : 최신순(-created_at) - 개수제한 - 페이징
    return await query.order_by("-created_at").limit(size).offset(offset)
