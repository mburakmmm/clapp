#!/bin/bash

echo "🚀 Hello from Bash!"
echo "=============================="

# Sistem bilgileri
echo "📅 Tarih: $(date)"
echo "🏠 Çalışma dizini: $(pwd)"
echo "👤 Kullanıcı: $(whoami)"
echo "💻 Sistem: $(uname -s)"

# Basit hesaplama
a=10
b=5
result=$((a + b))
echo "🧮 $a + $b = $result"

# Dosya sayısı
file_count=$(ls -1 | wc -l)
echo "📁 Dizindeki dosya sayısı: $file_count"

echo ""
echo "✅ Bash uygulaması başarıyla çalıştı!" 