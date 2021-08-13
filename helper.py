def get_right(point, data):
    board_width = data['board']['width']
    if point[0] == board_width-1:
        return -1
    return [point[0]+1, point[1]]


def get_left(point, data):
    if point[0] == 0:
        return -1
    return [point[0]-1, point[1]]


def get_up(point, data):
    if point[1] == 0:
        return -1
    return [point[0], point[1]-1]


def get_down(point, data):
    board_height = data['board']['height']
    if point[1] == board_height-1:
        return -1
    return [point[0], point[1]+1]