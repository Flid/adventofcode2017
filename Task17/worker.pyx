from libc.stdlib cimport malloc, free


cdef struct Node:
    Node* next
    Node* prev
    int value

    
def calculate(n):
    cdef int turns = 2017
    cdef Node *head = <Node *>malloc(sizeof(Node))
    cdef Node *new_node
    
    head.value = 0
    head.next = head
    head.prev = head
    
    for i in range(1, turns + 1):
        #print_list(head)
        for _ in range(n):
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
