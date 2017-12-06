#include <string>
#include <sstream>
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

string input = "5	1	10	0	1	7	13	14	3	12	8	10	7	12	0	6";

int main() {
    // Parse the input
    string token;
    istringstream iss(input);
    
    vector<int> cells;
    
    while(getline(iss, token, '\t')) {
        cells.push_back(stoi(token));
    }
    
    // We'll do it simple - just keep all records of the past
    vector<vector<int>> history;
    
    while(history.size() < 10000) {
        // Update the history
        vector<int> cells_copy = cells;
        history.push_back(cells_copy);
        
        // Locate the max element
        int max_pos = distance(
            cells.begin(), 
            max_element(cells.begin(), cells.end())
        );
        
        // Reset the current cell
        int to_spread = cells[max_pos];
        cells[max_pos] = 0;
        
        int position = max_pos;
        
        // Spread the contents of the cell across all cells
        while(to_spread) {
          to_spread --;
          position = (position + 1) % cells.size();
          cells[position]++;
        }
        
        // Search the history.
        for(auto const& history_record: history) {
            if(history_record == cells) {
                cout << "Result is " << history.size() << endl;
                return 0; 
            }
        }
    }
    cout << "Failed to find a solution" << endl;
}
