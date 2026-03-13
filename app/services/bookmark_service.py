from typing import List, Tuple, Optional
from app.models.bookmark import Bookmark
from app.models.quote import Quote
from app.models.user import User

class BookmarkService:
    async def toggle_bookmark(self, user: User, quote_id: int) -> Tuple[Optional[bool], str]:
        # 명언 존재 확인
        quote = await Quote.get_or_none(id=quote_id)
        if not quote:
            return None, "해당 명언을 찾을 수 없습니다."

        # 북마크 존재 확인
        bookmark = await Bookmark.get_or_none(user=user, quote=quote)

        if bookmark:
            await bookmark.delete()
            return False, "북마크가 해제되었습니다."
        else:
            await Bookmark.create(user=user, quote=quote)
            return True, "북마크에 추가되었습니다."

    async def get_my_bookmarks(self, user: User) -> List[Quote]:
        # 사용자의 북마크를 가져올 때 Quote 정보를 미리 불러옴 (prefetch)
        bookmarks = await Bookmark.filter(user=user).prefetch_related("quote").order_by("-id")
        return [b.quote for b in bookmarks]

bookmark_service = BookmarkService()