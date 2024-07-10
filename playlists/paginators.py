from rest_framework.pagination import LimitOffsetPagination

from playlists.constants import (
    USER_PLAYLIST_LIST_PAGINATE_BY,
    USER_PLAYLIST_SONG_LIST_PAGINATE_BY,
)


class UserPlaylistPageLimitOffsetPagination(LimitOffsetPagination):
    default_limit = USER_PLAYLIST_LIST_PAGINATE_BY


class UserPlaylistSongPageLimitOffsetPagination(LimitOffsetPagination):
    default_limit = USER_PLAYLIST_SONG_LIST_PAGINATE_BY
