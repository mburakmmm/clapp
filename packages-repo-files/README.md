# clapp-packages - Resmi Paket Deposu

Bu repo, [clapp](https://github.com/mburakmmm/clapp) paket yöneticisi için resmi paket deposudur.

## Paket Listesi

### Demo Paketler
- **hello-world** (v1.0.0) - Basit merhaba dünya uygulaması
- **text-editor** (v2.1.0) - Basit metin editörü
- **calculator** (v1.5.0) - Gelişmiş hesap makinesi
- **file-manager** (v3.0.0) - Basit dosya yöneticisi

### Productivity
- **todo-app** - Görev yöneticisi
- **note-taker** - Not alma uygulaması
- **password-manager** - Şifre yöneticisi

### Utilities
- **system-monitor** - Sistem izleme
- **disk-cleaner** - Disk temizleyici
- **network-scanner** - Ağ tarayıcı

### Games
- **snake-game** - Yılan oyunu
- **tic-tac-toe** - XOX oyunu
- **memory-game** - Hafıza oyunu

## Paket Yükleme

```bash
# clapp ile paket yükle
clapp install https://github.com/mburakmmm/clapp-packages/releases/download/v1.0.0/hello-world.clapp.zip

# veya GUI üzerinden App Store'dan yükle
clapp gui
```

## Paket Geliştirme

### Yeni Paket Oluşturma

```bash
# Yeni paket scaffold et
clapp scaffold my-package --language python

# Paket geliştir
cd my-package
# ... kod yaz ...

# Paket doğrula
clapp validate .

# Paket yayınla
clapp publish .
```

### Paket Yapısı

```
my-package/
├── manifest.json    # Paket bilgileri
├── main.py         # Ana dosya
├── README.md       # Paket açıklaması
└── assets/         # Varlıklar (opsiyonel)
    └── icon.png
```

### Manifest Örneği

```json
{
    "name": "my-package",
    "version": "1.0.0",
    "language": "python",
    "entry": "main.py",
    "description": "Paket açıklaması",
    "author": "Geliştirici Adı",
    "dependencies": [],
    "category": "utility"
}
```

## Paket Gönderme

1. Paketinizi geliştirin ve test edin
2. `.clapp.zip` dosyası oluşturun
3. GitHub Release olarak yayınlayın
4. `packages.json` dosyasını güncelleyin
5. Pull Request gönderin

## Paket Standartları

- ✅ Geçerli `manifest.json` dosyası
- ✅ Çalışan entry point
- ✅ README.md dosyası
- ✅ Uygun kategori seçimi
- ✅ Semantic versioning (x.y.z)
- ✅ Güvenli kod (zararlı kod yok)

## Katkıda Bulunma

1. Fork edin
2. Yeni paket ekleyin veya mevcut paketi güncelleyin
3. Pull Request gönderin
4. Review sürecini bekleyin

## Lisans

Bu repodaki paketler kendi lisanslarına sahiptir. Genel repo MIT lisansı altındadır.

## Destek

- 🐛 Bug Report: [Issues](https://github.com/mburakmmm/clapp-packages/issues)
- 💡 Paket Önerisi: [Issues](https://github.com/mburakmmm/clapp-packages/issues)
- 📖 Ana Proje: [clapp](https://github.com/mburakmmm/clapp) 