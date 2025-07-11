#!/usr/bin/env python3
"""
Hello World - clapp Demo Uygulaması
Basit merhaba dünya uygulaması
"""

import sys
import os
from datetime import datetime

def main():
    """Ana fonksiyon"""
    print("=" * 50)
    print("🌍 clapp Hello World Uygulaması")
    print("=" * 50)
    print()
    
    # Kullanıcı bilgisi
    user = os.getenv('USER', 'Kullanıcı')
    print(f"👋 Merhaba {user}!")
    print()
    
    # Tarih ve saat
    now = datetime.now()
    print(f"📅 Tarih: {now.strftime('%d/%m/%Y')}")
    print(f"🕐 Saat: {now.strftime('%H:%M:%S')}")
    print()
    
    # Sistem bilgisi
    print(f"🐍 Python Sürümü: {sys.version.split()[0]}")
    print(f"💻 Platform: {sys.platform}")
    print()
    
    # clapp bilgisi
    print("📦 Bu uygulama clapp paket yöneticisi ile çalışıyor!")
    print("🚀 Daha fazla paket için: clapp gui")
    print()
    
    # Teşekkür mesajı
    print("✨ clapp kullandığınız için teşekkürler!")
    print("🔗 GitHub: https://github.com/mburakmmm/clapp")
    print("=" * 50)

if __name__ == "__main__":
    main() 