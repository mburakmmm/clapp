package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	fmt.Println("🚀 Hello from Go!")
	fmt.Println("=" * 30)
	
	// Sistem bilgileri
	fmt.Printf("📅 Tarih: %s\n", time.Now().Format("2006-01-02 15:04:05"))
	fmt.Printf("🏠 Çalışma dizini: %s\n", getCurrentDir())
	
	// Basit hesaplama
	result := calculate(10, 5)
	fmt.Printf("🧮 10 + 5 = %d\n", result)
	
	fmt.Println("\n✅ Go uygulaması başarıyla çalıştı!")
}

func getCurrentDir() string {
	dir, err := os.Getwd()
	if err != nil {
		return "Bilinmiyor"
	}
	return dir
}

func calculate(a, b int) int {
	return a + b
} 