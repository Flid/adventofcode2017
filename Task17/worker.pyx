from libc.stdlib cimport malloc, free


cdef struct Node:
    Node* next
    Node* prev
    int value

    
def calculate_part1(n, turns):
    cdef Node *head = <Node *>malloc(sizeof(Node))
    cdef Node *new_node
    cdef int i, j, _turns, _n
    _n = n
    _turns = turns
    
    head.value = 0
    head.next = head
    head.prev = head
    
    for i in range(1, _turns + 1):
        for j in range(_n):
            head = head.next
        
        new_node = <Node *>malloc(sizeof(Node))
        new_node.value = i
        
        # Build the links
        new_node.next = head.next
        new_node.prev = head
        
        new_node.next.prev = new_node
        head.next = new_node
        
        # Step forward
        head = head.next
        
    return head.next.value


def calculate_part2(n, turns):
    # It's easier here. We don't need to know any 
    # values other than what's directly after zero.
    cdef int after_zero, count, current_pos, _n, _turns, i
    _n = n
    _turns = turns
    current_pos = 0
    count = 1
    after_zero = 0
    
    for i in range(1, _turns + 1):
        current_pos = (current_pos + _n) % count
        
        if current_pos == 0:
            after_zero = i
        
        count += 1
        current_pos += 1  # never exceedes `count`
        
        
        
    return after_zero
