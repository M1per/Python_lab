def intersect(list1, list2):
    return [item for item in list1 if item in list2]

def intersect_recursive(list1, list2):
    if not list1:
        return []
    if list1[0] in list2:
        return [list1[0]] + intersect_recursive(list1[1:], list2)
    else:
        return intersect_recursive(list1[1:], list2)


print(intersect([1, 2, 3, 4], [2, 3, 4, 6, 8]))
print(intersect([5, 8, 2], [2, 9, 1]))
print(intersect([5, 8, 2], [7, 4]))

print(intersect_recursive([1, 2, 3, 4], [2, 3, 4, 6, 8]))
print(intersect_recursive([5, 8, 2], [2, 9, 1]))
print(intersect_recursive([5, 8, 2], [7, 4]))




