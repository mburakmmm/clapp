const fs = require('fs');
const path = require('path');

console.log('🚀 Hello from Node.js!');
console.log('='.repeat(30));

// Sistem bilgileri
const now = new Date();
console.log(`📅 Tarih: ${now.toLocaleString()}`);

// Çalışma dizini
const currentDir = process.cwd();
console.log(`🏠 Çalışma dizini: ${currentDir}`);

// Basit hesaplama
function calculate(a, b) {
    return a + b;
}

const result = calculate(10, 5);
console.log(`🧮 10 + 5 = ${result}`);

// Dosya sistemi örneği
try {
    const files = fs.readdirSync(currentDir);
    console.log(`📁 Dizindeki dosya sayısı: ${files.length}`);
} catch (error) {
    console.log('📁 Dosya listesi alınamadı');
}

console.log('\n✅ Node.js uygulaması başarıyla çalıştı!'); 