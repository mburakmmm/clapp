#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    printf("🚀 Hello from C!\n");
    printf("==============================\n");
    
    // Sistem bilgileri
    time_t now = time(NULL);
    printf("📅 Unix timestamp: %ld\n", now);
    
    // Basit hesaplama
    int a = 10, b = 5;
    int result = a + b;
    printf("🧮 %d + %d = %d\n", a, b, result);
    
    printf("\n✅ C uygulaması başarıyla çalıştı!\n");
    return 0;
} 