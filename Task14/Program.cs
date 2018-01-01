using System;

namespace knot
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

		public Node get_next(Node node) {
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
		public const uint QUEUE_SIZE = 256;

		static byte[] get_length_seq(string input) {
			byte[] end_bytes = { 17, 31, 73, 47, 23 };
			byte[] input_bytes = new byte[input.Length + end_bytes.Length];

			for (int i = 0; i < input.Length; i++) {
				input_bytes [i] = Convert.ToByte(input [i]);
			}
			for (int i = 0; i < end_bytes.Length; i++) {
				input_bytes [input.Length + i] = end_bytes [i];
			}
			return input_bytes;
		}

		static FlipCircleQueue apply_operations(byte[] input_bytes) {
			FlipCircleQueue fcq = new FlipCircleQueue();
			for (int i = 0; i < QUEUE_SIZE; i++) {
				fcq.add_node (i);
			}
			uint skip_size = 0;

			// Once we move the queue head back and force, we need to keep 
			// track of the original start position for the final calculation.
			long start_pos = 0;

			for (int iteration = 0; iteration < 64; iteration++) {
				foreach (uint l in input_bytes) {
					if (l > 0) {
						FlipCircleQueue cut = fcq.cut (fcq.head, l);
						cut.flip ();
						cut.reset_head (cut.n_from_head (1));
						fcq.merge (cut);
					}

					fcq.reset_head (fcq.n_from_head (skip_size));
					start_pos = (QUEUE_SIZE + start_pos - l - skip_size) % QUEUE_SIZE;
					skip_size++;
				}
			}

			// Calculate the hash
			start_pos = (start_pos + QUEUE_SIZE) % QUEUE_SIZE;

			fcq.reset_head (fcq.n_from_head ((uint)start_pos));
			return fcq;
		}

		static byte[] extract_hash(FlipCircleQueue fcq) {
			
			Node node = fcq.head;

			byte[] sums = new byte[QUEUE_SIZE / 16];

			for (int i = 0; i < QUEUE_SIZE; i++) {
				sums [i / 16] = (byte)(sums [i / 16] ^ (byte)node.value);

				node = fcq.get_next (node);
			}
			return sums;
		}

		static byte[] calculate_hash(string input) {
			byte[] input_bytes = get_length_seq (input);

			// Initialize the queue
			FlipCircleQueue fcq = apply_operations(input_bytes);
			return extract_hash (fcq);
		}

		static uint number_of_set_bits(byte i)
		{
			i -= (byte)((i >> 1) & 0x55);
			i = (byte)((i & 0x33) + ((i >> 2) & 0x33));
			return (uint)(((i + (i >> 4)) & 0x0F) * 0x01);
		}
		
		public static void Main (string[] args)
		{
			// Put your data here
			string input = "flqrgnkx";
			uint sum = 0;

			for(int i =0; i<QUEUE_SIZE/2; i++) {
				byte[] hash = calculate_hash (input + "-" + i.ToString ());

				for (int j = 0; j < QUEUE_SIZE / 16; j++) {
					sum += number_of_set_bits (hash[j]);
				}
			}

			Console.WriteLine (sum);
		}
	}
}
 
