# -*- coding: utf-8 -*-
"""
翻转一个链表
挑战 ：在原地一次翻转完成
Definition of ListNode

class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""


class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

L = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))


# def reverse(head):
#   temp = None     # 创建临时链表
#   while head:
#    cur = head.next    # 指针指向链表的下一个节点   或者  保存 2-3 的状态
#    head.next = temp   # 摘除当前链表
#    temp = head        # 让head指向临时列表
#    head = cur         # 摘除之后的指针状态
#   return temp
#


# 方法二
def reverse(head):
    dummy = ListNode(-1)    # -1 -> None
    dummy.next = head       # -1 -> 1 -> 2 -> 3 -> None
    # print(dummy.next.next.val)
    pre, cur = head, head.next  # pre: 1 -> 2 -> 3 -> None   cur: 2 -> 3 -> None
    while cur:              # cur: 2 -> 3 -> None      3 -> None
        temp = cur          # temp: 2 -> 3 -> None     3 -> None
        # 把摘链的地方连起来
        pre.next = cur.next  # pre: 1-> 3 -> None      1-> None
        cur = pre.next       # cur: 3 -> None           None
        temp.next = dummy.next  # temp: 2 -> 1 -> 2 -> 3 -> None   3 ->
        dummy.next = temp       # dummy.next: 2 -> 1 -> 2 -> 3 -> None
        return dummy.next

# x = reverse(L)
# while x:
#     print(x.val)
#     x = x.next


def print_ll(head):
    tmp = head
    lis = "当前链子："
    while tmp:
        lis += str(tmp.val)
        tmp=tmp.next
    return lis


def reverse_linkedlist4(head):  # 1234, 234, 23, 4
    print("head:", print_ll(head))
    if head is None or head.next is None:
        return head
    else:
        newhead=reverse_linkedlist4(head.next)  # 4
        print("new1", print_ll(newhead))
        print("head2:", print_ll(head))
        head.next.next = head  #
        head.next = None
        print("new2", print_ll(newhead))
        print("head3:", print_ll(head))
    return newhead

reverse_linkedlist4(L)


# head: 4-None    return 4-None
# head: 3-4       newhead=4-None
# head: 2-3-4     newhead=???
# head: 1-2-3-4   newhead=？？？