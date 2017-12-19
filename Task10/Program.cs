using System;
/*
The solution is quite inefficient, but is sort of nice :)
Basically we define a class to store a double-linked list 
with O(1)-cost flipping - changing a direction.

So for every step of the algorythm we cut a piece of the dequeu, 
flip, merge with the original queue. This operation is still linear.

I've got an idea how to do it much faster, I'll implement it better later, and with another language :)
*/

namespace test
{
	class Node
	{
		public Node[] refs;
		public Int32 value;

		public Node(int value) {
			this.refs = new Node[2];
			this.value = value;
		}
	}
	class FlipCircleQueue
	{
		public Node head;

		int next_direction = 1;

		int prev_direction {
			get {
				return (this.next_direction + 1) % 2;
			}
		}

		public FlipCircleQueue() {}

		public FlipCircleQueue(Node start, Node end, int next_direction): this() {
			this.next_direction = next_direction;
			set_prev(start, end);
			this.head = start;
		}
			
		Node get_next(Node node) {
			return node.refs[this.next_direction];
		}

		void set_next(Node node, Node next) {
			node.refs[this.next_direction] = next;
			next.refs [this.prev_direction] = node;
		}

		Node get_prev(Node node) {
			return node.refs[this.prev_direction];
		}

		void set_prev(Node node, Node prev) {
			node.refs[this.prev_direction] = prev;
			prev.refs [this.next_direction] = node;
		}

		public void add_node(int value) {
			Node node = new Node(value);
			add_node (node);
		}

		public void add_node(Node node) {
			if (this.head == null) {
				this.head = node;
				// Make a circle
				set_next (this.head, this.head);
				set_prev (this.head, this.head);
			}
			else {
				Node old_last = get_prev (this.head);
				this.set_prev (node, old_last);
				this.set_prev (this.head, node);
			}
		}

		public FlipCircleQueue cut(Node start, uint len) {
			Node end = n_from_node (start, len - 1);
			Node pre_start = get_prev (start);
			Node post_end = get_next (end);	

			if (start == post_end) {
				this.head = null;
			} else {
				set_prev (post_end, pre_start);
				this.head = post_end;
			}


			FlipCircleQueue new_queue = new FlipCircleQueue (
				start, end, this.next_direction
			);
			return new_queue;

		}

		public void merge(FlipCircleQueue other) {
			Node node = other.head;

			while (true) {

				Node next_node = other.get_next (node);
				this.add_node (node);

				if (next_node == other.head) {
					break;
				}
				node = next_node;
			}
		}

		public Node n_from_node(Node node, uint n) {
			for (int i = 0; i < n; i++) {
				node = get_next (node);
			}
			return node;
		}

		public Node n_from_head(uint n) {
			return n_from_node(this.head, n);
		}

		public void reset_head(Node node) {
			this.head = node;
		}

		public void flip() {
			this.next_direction = this.prev_direction;
		}
	}
	class MainClass
	{
		public static void Main (string[] args)
		{
			// Put your data here
			uint queue_size = 5;
			uint[] input = new uint[] {3, 4, 1, 5};

			FlipCircleQueue fcq = new FlipCircleQueue();
			for (int i = 0; i < queue_size; i++) {
				fcq.add_node (i);
			}

			uint skip_size = 0;

			// Once we move the queue head back and force, we need to keep 
			// track of the original start position for the final calculation.
			long start_pos = 0;

			foreach(uint l in input) {
				if (l > 0) {
					FlipCircleQueue cut = fcq.cut (fcq.head, l);
					cut.flip ();
					cut.reset_head (cut.n_from_head (1));
					fcq.merge (cut);
				}

				fcq.reset_head (fcq.n_from_head (skip_size));
				start_pos = (queue_size + start_pos - l - skip_size) % queue_size;
				skip_size++;
			}


			Console.Write ("Solution: ");
			Node target1 = fcq.n_from_head ((uint)start_pos);
			Node target2 = fcq.n_from_node (target1, 1);
			Console.WriteLine (target1.value * target2.value);
		}
	}
}
