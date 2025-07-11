#!/usr/bin/env python3
"""
Calculator Python - Basit komut satırı hesap makinesi
clapp paket yöneticisi için örnek uygulama (bağımlılık testi)
"""

import sys
import os
from datetime import datetime

def add(a, b):
    """Toplama işlemi"""
    return a + b

def subtract(a, b):
    """Çıkarma işlemi"""
    return a - b

def multiply(a, b):
    """Çarpma işlemi"""
    return a * b

def divide(a, b):
    """Bölme işlemi"""
    if b == 0:
        raise ValueError("Sıfıra bölme hatası!")
    return a / b

def power(a, b):
    """Üs alma işlemi"""
    return a ** b

def sqrt(a):
    """Karekök işlemi"""
    if a < 0:
        raise ValueError("Negatif sayının karekökü alınamaz!")
    return a ** 0.5

def show_menu():
    """Menüyü göster"""
    print("\n🧮 Hesap Makinesi")
    print("=" * 30)
    print("1. Toplama (+)")
    print("2. Çıkarma (-)")
    print("3. Çarpma (*)")
    print("4. Bölme (/)")
    print("5. Üs alma (^)")
    print("6. Karekök (√)")
    print("7. Çıkış")
    print("=" * 30)

def get_numbers():
    """Kullanıcıdan sayıları al"""
    try:
        a = float(input("Birinci sayı: "))
        b = float(input("İkinci sayı: "))
        return a, b
    except ValueError:
        print("❌ Geçersiz sayı formatı!")
        return None, None

def get_single_number():
    """Kullanıcıdan tek sayı al"""
    try:
        a = float(input("Sayı: "))
        return a
    except ValueError:
        print("❌ Geçersiz sayı formatı!")
        return None

def main():
    """Ana fonksiyon"""
    print("🧮 Calculator Python v1.2.0")
    print("Basit komut satırı hesap makinesi")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Bağımlılık kontrolü (hello-python'un varlığını kontrol et)
    hello_python_path = os.path.join("..", "hello-python")
    if os.path.exists(hello_python_path):
        print("✅ Bağımlılık kontrolü: hello-python bulundu")
    else:
        print("⚠️  Bağımlılık uyarısı: hello-python bulunamadı")
    
    while True:
        show_menu()
        
        try:
            choice = input("Seçiminiz (1-7): ").strip()
            
            if choice == '7':
                print("👋 Hesap makinesi kapatılıyor...")
                break
            
            elif choice == '1':
                # Toplama
                a, b = get_numbers()
                if a is not None and b is not None:
                    result = add(a, b)
                    print(f"📊 Sonuç: {a} + {b} = {result}")
            
            elif choice == '2':
                # Çıkarma
                a, b = get_numbers()
                if a is not None and b is not None:
                    result = subtract(a, b)
                    print(f"📊 Sonuç: {a} - {b} = {result}")
            
            elif choice == '3':
                # Çarpma
                a, b = get_numbers()
                if a is not None and b is not None:
                    result = multiply(a, b)
                    print(f"📊 Sonuç: {a} * {b} = {result}")
            
            elif choice == '4':
                # Bölme
                a, b = get_numbers()
                if a is not None and b is not None:
                    try:
                        result = divide(a, b)
                        print(f"📊 Sonuç: {a} / {b} = {result}")
                    except ValueError as e:
                        print(f"❌ Hata: {e}")
            
            elif choice == '5':
                # Üs alma
                a, b = get_numbers()
                if a is not None and b is not None:
                    result = power(a, b)
                    print(f"📊 Sonuç: {a} ^ {b} = {result}")
            
            elif choice == '6':
                # Karekök
                a = get_single_number()
                if a is not None:
                    try:
                        result = sqrt(a)
                        print(f"📊 Sonuç: √{a} = {result}")
                    except ValueError as e:
                        print(f"❌ Hata: {e}")
            
            else:
                print("❌ Geçersiz seçim! Lütfen 1-7 arasında bir sayı girin.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Hesap makinesi kapatılıyor...")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
    
    print("✅ Calculator Python başarıyla sonlandı!")

if __name__ == "__main__":
    main() 