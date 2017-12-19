use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::collections::HashMap;


macro_rules! hashmap {
    ($( $key: expr => $val: expr ),*) => {{
         let mut map = ::std::collections::HashMap::new();
         $( map.insert(String::from($key), $val); )*
         map
    }}
}


fn one_step(x: &mut f32, y: &mut f32, steps: &HashMap<String,(f32, f32)>, step_name: &str) {
    match steps.get(&String::from(step_name)) {
        Some(&(dx, dy)) => {*x += dx; *y += dy},
        _ => println!("Something's wrong: {}\n", step_name),
    };
}

fn main() {
    let steps = hashmap![
        "s" => (0.0, 1.0), "sw" => (-1.0, 0.5), "se" => (1.0, 0.5),
        "n" => (0.0, -1.0), "nw" => (-1.0, -0.5), "ne" => (1.0, -0.5)
    ];
    // Create a path to the desired file
    let path = Path::new("data.txt");
    let display = path.display();

    // Open the path in read-only mode, returns `io::Result<File>`
    let mut file = match File::open(&path) {
        // The `description` method of `io::Error` returns a string that
        // describes the error
        Err(why) => panic!("couldn't open {}: {}", display,
                                                   why.description()),
        Ok(file) => file,
    };

    // Read the file contents into a string, returns `io::Result<usize>`
    let mut input_string = String::new();
    match file.read_to_string(&mut input_string) {
        Err(why) => panic!("couldn't read {}: {}", display,
                                                   why.description()),
        Ok(_) => (),
    }
    
    let mut x: f32 = 0.0;
    let mut y: f32 = 0.0;
    
    for step_name in input_string.split(",") {
        one_step(&mut x, &mut y, &steps, &step_name.trim());
    }
    print!("Resulting coordinates. X:{}, Y:{}\n", x, y);
    
    // If abs(y) < abs(x)*0.5, means we can reach (0, 0) by a combination of diagonal 
    // moves only, in exactly abs(x) moves. 
    // Otherwise we'll be moving in one diagonal direction to reach x=0, 
    // and then do abs(y) hops. 
    let y_move = y.abs() - x.abs()*0.5;
    print!("Solution: {}\n", x.abs() + if y_move > 0.0 {y_move} else {0.0})
    
    // `file` goes out of scope, and the "hello.txt" file gets closed
}
