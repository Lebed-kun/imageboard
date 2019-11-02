# Moder priveleges

GET_REPORTS = 'get_reports'
DELETE_REPORTS = 'delete_reports'

DELETE_POSTS = 'delete_posts'
EDIT_POSTS = 'edit_posts'

BAN_POSTERS = 'ban_posters'

GET_BANS = 'get_bans'
EDIT_BANS = 'edit_bans'
DELETE_BANS = 'delete_bans'

GET_MODER_BOARDS = 'get_moder_boards'

MODER_PRIVELEGES = [
    GET_REPORTS, DELETE_REPORTS, DELETE_POSTS, EDIT_POSTS,
    BAN_POSTERS, GET_BANS, EDIT_BANS, DELETE_BANS,
    GET_MODER_BOARDS
]

EDIT_THREADS = 'edit_threads'
DELETE_THREADS = 'delete_thread'

GET_ADMIN_BOARDS = 'get_admin_boards'
DELETE_BOARDS = 'delete_board'

ADMIN_PRIVELEGES = MODER_PRIVELEGES + [
    GET_ADMIN_BOARDS, DELETE_BOARDS
]