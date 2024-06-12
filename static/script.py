s1 = 'zxyzxyz'

left, right, count = 0, 1, 1
new_string = ''
answer_string = ''
while count <= len(s1) - 1:
    new_string += s1[left:right]
    count += 1
    left += 1
    right += 1

print(new_string)


