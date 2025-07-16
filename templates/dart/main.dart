#!/usr/bin/env dart
// Hello Dart - clapp Örnek Uygulaması
//
// Bu uygulama clapp için Dart uygulaması geliştirme örneğidir.

import 'dart:io';
import 'dart:math';

void main() {
  printHeader();
  
  // Temel bilgiler
  print('📅 Tarih: ${DateTime.now()}');
  print('📁 Çalışma Dizini: ${Directory.current.path}');
  
  // Kullanıcı etkileşimi
  stdout.write('\n👋 Adınızı girin: ');
  String? name = stdin.readLineSync();
  
  if (name != null && name.trim().isNotEmpty) {
    print('Merhaba $name! clapp\'e hoş geldiniz!');
  } else {
    print('Merhaba! clapp\'e hoş geldiniz!');
  }
  
  // Örnek işlemler
  print('\n🔢 Basit Hesaplama Örneği:');
  try {
    stdout.write('Birinci sayıyı girin: ');
    double a = double.parse(stdin.readLineSync() ?? '0');
    
    stdout.write('İkinci sayıyı girin: ');
    double b = double.parse(stdin.readLineSync() ?? '0');
    
    print('Toplam: ${a + b}');
    print('Çarpım: ${a * b}');
    
    if (b != 0) {
      print('Bölüm: ${a / b}');
    } else {
      print('Bölüm: Tanımsız (sıfıra bölme)');
    }
  } catch (e) {
    print('❌ Geçersiz sayı girişi!');
  }
  
  // Dart özellikleri gösterimi
  print('\n🔧 Dart Özellikleri:');
  
  // Liste örneği
  List<String> colors = ['kırmızı', 'yeşil', 'mavi'];
  print('Renkler: ${colors.join(', ')}');
  
  // Map örneği
  Map<String, int> scores = {
    'Ali': 85,
    'Ayşe': 92,
    'Mehmet': 78,
  };
  print('Skorlar: $scores');
  
  // Fonksiyon örneği
  int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
  }
  
  print('5! = ${factorial(5)}');
  
  // Rastgele sayı
  Random random = Random();
  print('Rastgele sayı: ${random.nextInt(100)}');
  
  print('\n✅ Uygulama başarıyla tamamlandı!');
  printSeparator();
}

void printHeader() {
  printSeparator();
  print('🚀 Hello Dart - clapp Örnek Uygulaması');
  printSeparator();
}

void printSeparator() {
  print('=' * 50);
} 