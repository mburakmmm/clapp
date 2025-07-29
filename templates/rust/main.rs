use std::env;
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    println!("🚀 Hello from Rust!");
    println!("{}", "=".repeat(30));
    
    // Sistem bilgileri
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    
    println!("📅 Unix timestamp: {}", now);
    
    // Çalışma dizini
    match env::current_dir() {
        Ok(path) => println!("🏠 Çalışma dizini: {}", path.display()),
        Err(_) => println!("🏠 Çalışma dizini: Bilinmiyor"),
    }
    
    // Basit hesaplama
    let result = calculate(10, 5);
    println!("🧮 10 + 5 = {}", result);
    
    println!("\n✅ Rust uygulaması başarıyla çalıştı!");
}

fn calculate(a: i32, b: i32) -> i32 {
    a + b
} 