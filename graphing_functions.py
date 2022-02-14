def convert_to_number(n):
    if not n:
        return 0.0
    try:
        return float(n)
    except ValueError:
        return False


# def convert_to_polar(x_val, y_val):
#     angle = (x_val + 90) % 360
#     new_x = math.cos(math.radians(angle)) * y_val
#     new_y = math.sin(math.radians(angle)) * y_val
#     return new_x, new_y
#
#
# def convert_lists_to_polar(x_val, y_val):
#     return_list_x = []
#     return_list_y = []
#     for section in zip(x_val, y_val):
#         return_list_x.append([])
#         return_list_y.append([])
#         for x_val, y_val in zip(section[0], section[1]):
#             x_val, y_val = convert_to_polar(x_val, y_val)
#             return_list_x[-1].append(x_val)
#             return_list_y[-1].append(y_val)
#     return return_list_x, return_list_y
