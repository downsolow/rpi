use rppal::gpio::{Gpio, OutputPin};
use std::thread::{self, sleep, JoinHandle};
use std::sync::{Arc, RwLock, atomic::{AtomicBool, Ordering}};
use std::time::Duration;
use std::collections::HashMap;
use std::vec;
use once_cell::sync::Lazy;

pub struct Blinker {
    state: Arc<AtomicBool>,
    handle: Option<JoinHandle<()>>,
    message: Arc<RwLock<String>>,
}

impl Blinker {
    pub fn new() -> Blinker {

        Blinker{
            state: Arc::new(AtomicBool::new(false)), 
            handle: None,
            message: Arc::new(RwLock::new("Hello World!".to_string())),
        }
    }

    pub fn set_message(&mut self, message: &str) {
        let mut msg =  self.message.write().unwrap();
        msg.clear();
        msg.push_str(message);
    }

    pub fn start(&mut self) {
        let state = self.state.clone();
        state.store(true, Ordering::SeqCst);
        let morse_state = self.state.clone();
        let message = Arc::clone(&self.message);
        
        self.handle = Some(thread::spawn( move || {
            let mut morse = Morse::new(morse_state);
             while state.load(Ordering::SeqCst) {
                let msg = message.read().unwrap().clone();
                morse.broadcast(msg);
            }
        }));
    }

    pub fn stop(&mut self) {
        self.state.store(false, Ordering::SeqCst);

        if let Some(handle) = self.handle.take() {
            let _ = handle.join();
        }
    }
}

pub struct Morse {
    pin: OutputPin,
    active: Arc<AtomicBool>,
}

impl Morse {
    pub fn new(active: Arc<AtomicBool>) -> Morse {
        let gpio = Gpio::new().unwrap();
        let output_pin = gpio.get(18).unwrap().into_output();
        Morse{
            pin: output_pin,
            active: active,
        }
    }

    pub fn set_active(&mut self, active: Arc<AtomicBool>) {
        self.active = active;
    }

    pub fn broadcast(&mut self, message: String) {
        for ch in message.chars() {
            if !self.active.load(Ordering::SeqCst)  {
                break;
            }
            match ch {
                ' ' => { sleep(4 * Self::DIT_DURATION); }, // 7 dits
                _ if ch.is_ascii_alphabetic() => { self.broadcast_char(ch); },
                _ => {}
            }
        }

        if self.active.load(Ordering::SeqCst) {
            sleep(4 * Self::DIT_DURATION)
        }
    }

    pub fn broadcast_char(&mut self, ch: char) {
        let char_code = ALPHABET.get(&ch.to_ascii_uppercase());
        match char_code {
            Some(code) => { self.broadcast_symbols(code)},
            _ => {}
        };
    }

    pub fn broadcast_symbols(&mut self, symbols: &Vec<MorseSymbol>) {
        for symbol in symbols.iter() {
            match symbol {
                MorseSymbol::Dit => { self.broadcast_dit(); },
                MorseSymbol::Dah => { self.broadcast_dah(); },
            }
        }
        sleep(2* Self::DIT_DURATION); // 3 dits
    }

    pub fn broadcast_dit(&mut self) {
        self.pin.set_high();
        sleep(Self::DIT_DURATION);
        self.pin.set_low();
        sleep(Self::DIT_DURATION);
    }

    pub fn broadcast_dah(&mut self) {
        self.pin.set_high();
        sleep(3 * Self::DIT_DURATION);
        self.pin.set_low();
        sleep(Self::DIT_DURATION);
    }

    const DIT_DURATION: Duration = Duration::from_millis(90);
}

static ALPHABET: Lazy<HashMap<char, Vec<MorseSymbol>>> = Lazy::new(|| {
    use MorseSymbol::*;
    let m = [
    ('A', vec![Dit, Dah,]),
    ('B', vec![Dah, Dit, Dit, Dit,]),
    ('C', vec![Dah, Dit, Dah, Dit,]),
    ('D', vec![Dah, Dit, Dit,]),
    ('E', vec![Dit,]),
    ('F', vec![Dit, Dit, Dah, Dit,]),
    ('G', vec![Dah, Dah, Dit,]),
    ('H', vec![Dit, Dit, Dit, Dit,]),
    ('I', vec![Dit, Dit,]),
    ('J', vec![Dit, Dah, Dah, Dah,]),
    ('K', vec![Dah, Dit, Dah,]),
    ('L', vec![Dit, Dah, Dit, Dit,]),
    ('M', vec![Dah, Dah,]),
    ('N', vec![Dah, Dit,]),
    ('O', vec![Dah, Dah, Dah,]),
    ('P', vec![Dit, Dah, Dah, Dit,]),
    ('Q', vec![Dah, Dah, Dit, Dah,]),
    ('R', vec![Dit, Dah, Dit,]),
    ('S', vec![Dit, Dit, Dit,]),
    ('T', vec![Dah,]),
    ('U', vec![Dit, Dit, Dah,]),
    ('V', vec![Dit, Dit, Dit, Dah,]),
    ('W', vec![Dit, Dah, Dah,]),
    ('X', vec![Dah, Dit, Dit, Dah,]),
    ('Y', vec![Dah, Dit, Dah, Dah,]),
    ('Z', vec![Dah, Dah, Dit, Dit,]),
    ];
    m.into_iter().collect()
});

pub enum MorseSymbol {
    Dit,
    Dah,
}



// A	Dit, Dah,		
// B	Dah, Dit, Dit, Dit,		
// C	Dah, Dit, Dah, Dit,		
// D	Dah, Dit, Dit,		
// E	Dit,		
// F	Dit, Dit, Dah, Dit,		
// G	Dah, Dah, Dit,		
// H	Dit, Dit, Dit, Dit,		
// I	Dit, Dit,		
// J	Dit, Dah, Dah, Dah,		
// K	Dah, Dit, Dah,		
// L	Dit, Dah, Dit, Dit,		
// M	Dah, Dah,		
// N	Dah, Dit,
// O	Dah, Dah, Dah,
// P	Dit, Dah, Dah, Dit,
// Q	Dah, Dah, Dit, Dah,
// R	Dit, Dah, Dit,
// S	Dit, Dit, Dit,
// T	Dah,
// U	Dit, Dit, Dah,
// V	Dit, Dit, Dit, Dah,
// W	Dit, Dah, Dah,
// X	Dah, Dit, Dit, Dah,
// Y	Dah, Dit, Dah, Dah,
// Z	Dah, Dah, Dit, Dit,

