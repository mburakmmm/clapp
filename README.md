# clapp - Komut Satırı Uygulama Paket Yöneticisi

clapp, Python ve Lua uygulamalarını kolayca yönetmenizi sağlayan bir paket yöneticisidir.

## Özellikler

- 🚀 **Kolay Kurulum**: Paketleri tek komutla yükleyin
- 📦 **Çoklu Dil Desteği**: Python ve Lua uygulamaları
- 🖥️ **GUI & CLI**: Hem grafik hem komut satırı arayüzü
- 🔧 **Geliştirici Araçları**: Paket oluşturma ve yayınlama
- 📋 **Manifest Sistemi**: Kolay paket tanımlama

## Kurulum

```bash
pip install clapp
```

## Kullanım

### Komut Satırı

```bash
# Paket yükle
clapp install https://example.com/package.clapp.zip

# Yüklü paketleri listele
clapp list

# Paket çalıştır
clapp run my-app

# Paket kaldır
clapp remove my-app
```

### GUI Arayüzü

```bash
# GUI'yi başlat
clapp gui
```

## Geliştirici Araçları

```bash
# Yeni paket oluştur
clapp scaffold my-app --language python

# Paket doğrula
clapp validate my-app

# Paket yayınla
clapp publish my-app
```

## Manifest Formatı

```json
{
    "name": "my-app",
    "version": "1.0.0",
    "language": "python",
    "entry": "main.py",
    "description": "Uygulama açıklaması",
    "dependencies": []
}
```

## Paket Deposu

Hazır paketler için: [clapp-packages](https://github.com/mburakmmm/clapp-packages)

## Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add some amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Destek

- 🐛 Bug Report: [Issues](https://github.com/mburakmmm/clapp/issues)
- 💡 Feature Request: [Issues](https://github.com/mburakmmm/clapp/issues)
- 📖 Dokumentasyon: [Wiki](https://github.com/mburakmmm/clapp/wiki) 