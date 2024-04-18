from rest_framework.pagination import LimitOffsetPagination

from lyrics.constants import LYRIC_LINE_TIMECODES_PAGINATE_BY


class LyricLineTimecodePageLimitOffsetPagination(LimitOffsetPagination):
    default_limit = LYRIC_LINE_TIMECODES_PAGINATE_BY
