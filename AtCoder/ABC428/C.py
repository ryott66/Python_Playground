# def main():
#     q = int(input())
#     stack = [(0, 0)]


#     for _ in range(q):
#         pre_stack_pos = stack[-1][0]
#         pre_stack_min = stack[-1][1]
#         query = input().rstrip()
#         if query == "1 (":
#             stack.append((pre_stack_pos + 1, pre_stack_min))
#         elif query == "1 )":
#             stack.append((pre_stack_pos - 1, min(pre_stack_min, pre_stack_pos - 1)))
#         else:
#             stack.pop()
#         if stack[-1][1] < 0:
#             print("No")
#         elif stack[-1][0] == 0:
#             print("Yes")
#         else:
#             print("No")



#         # print(good_kakko(s))

# # ======括弧問題の基本はスタックだけど、今回は文字列生成ごとにこれやると計算量が多い！
# # def good_kakko(s):
# #     stack = []
# #     for c in s:
# #         if c == "(":
# #             stack.append("(")
# #         else:
# #             if not stack:
# #                 return("No")
# #             stack.pop()
# #     if not stack:
# #         return("Yes")
# #     else:
# #         return("No")

# if __name__ == "__main__":
#     main()


# ========stdinはやすぎ！！！=========
from sys import stdin
input = stdin.readline

def main():
    q = int(input())

    # stack[i] = (累積値 sum, その位置までの最小値 min_sum)
    stack = [(0, 0)]

    for _ in range(q):
        query = input().strip()

        curr_sum, curr_min = stack[-1]

        if query == "1 (":
            new_sum = curr_sum + 1
            new_min = curr_min  # ( は min を下げない
            stack.append((new_sum, new_min))

        elif query == "1 )":
            new_sum = curr_sum - 1
            new_min = min(curr_min, new_sum)
            stack.append((new_sum, new_min))

        else:  # "2"
            stack.pop()

        sum_now, min_now = stack[-1]

        if min_now < 0:
            print("No")
        elif sum_now == 0:
            print("Yes")
        else:
            print("No")


if __name__ == "__main__":
    main()
