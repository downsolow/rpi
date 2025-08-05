mod hello_world_diode;

use hello_world_diode::hello_world_diode::Blinker;
use std::io;

fn main() {
    println!("Hello, world! Compiled on W11. Run on RPi");

    let mut blinker = Blinker::new();
    blinker.start();

    println!("Press q to quit");
    let mut input = String::new();
    _ = io::stdin().read_line(&mut input);

    while !(input.to_ascii_lowercase().starts_with("q")) {
        blinker.set_message(&input);
        input.clear();
        _ = io::stdin().read_line(&mut input);
    }

    blinker.stop();
    
    println!("Bye! Bye!");
}
