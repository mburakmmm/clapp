#!/bin/bash

# LWM - Lua Window Manager Akıllı Kurulum Script'i
# Sistem tespiti yaparak gereksinimleri otomatik yükler

set -e

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logo
echo -e "${CYAN}"
cat << "EOF"
██╗     ██╗    ██╗    ███╗   ███╗
██║     ██║    ██║    ████╗ ████║
██║     ██║ █╗ ██║    ██╔████╔██║
██║     ██║███╗██║    ██║╚██╔╝██║
███████╗╚███╔███╔╝    ██║ ╚═╝ ██║
╚══════╝ ╚══╝╚══╝     ╚═╝     ╚═╝
                                   
Lua Window Manager - Akıllı Kurulum
EOF
echo -e "${NC}"

# Global değişkenler
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/awesome"
BACKUP_DIR="$HOME/.config/awesome.backup.$(date +%Y%m%d_%H%M%S)"
OS_TYPE=""
OS_VERSION=""
PACKAGE_MANAGER=""
INSTALL_COMMAND=""
UPDATE_COMMAND=""
AUTO_INSTALL=false
SKIP_CONFIRM=false
VERBOSE=false

# Fonksiyonlar
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${PURPLE}[VERBOSE]${NC} $1"
    fi
}

# Sistem tespiti
detect_system() {
    print_status "Sistem tespit ediliyor..."
    
    # OS tespiti
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS_TYPE="$NAME"
            OS_VERSION="$VERSION_ID"
        elif [ -f /etc/lsb-release ]; then
            . /etc/lsb-release
            OS_TYPE="$DISTRIB_ID"
            OS_VERSION="$DISTRIB_RELEASE"
        elif [ -f /etc/debian_version ]; then
            OS_TYPE="Debian"
            OS_VERSION=$(cat /etc/debian_version)
        elif [ -f /etc/redhat-release ]; then
            OS_TYPE="RedHat"
            OS_VERSION=$(cat /etc/redhat-release | sed 's/.*release \([0-9.]*\).*/\1/')
        else
            OS_TYPE="Linux"
            OS_VERSION="Unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS_TYPE="macOS"
        OS_VERSION=$(sw_vers -productVersion)
    else
        OS_TYPE="Unknown"
        OS_VERSION="Unknown"
    fi
    
    print_verbose "OS: $OS_TYPE $OS_VERSION"
    
    # Paket yöneticisi tespiti
    if command -v apt &> /dev/null; then
        PACKAGE_MANAGER="apt"
        INSTALL_COMMAND="apt install -y"
        UPDATE_COMMAND="apt update"
    elif command -v pacman &> /dev/null; then
        PACKAGE_MANAGER="pacman"
        INSTALL_COMMAND="pacman -S --noconfirm"
        UPDATE_COMMAND="pacman -Sy"
    elif command -v dnf &> /dev/null; then
        PACKAGE_MANAGER="dnf"
        INSTALL_COMMAND="dnf install -y"
        UPDATE_COMMAND="dnf update"
    elif command -v yum &> /dev/null; then
        PACKAGE_MANAGER="yum"
        INSTALL_COMMAND="yum install -y"
        UPDATE_COMMAND="yum update"
    elif command -v zypper &> /dev/null; then
        PACKAGE_MANAGER="zypper"
        INSTALL_COMMAND="zypper install -y"
        UPDATE_COMMAND="zypper refresh"
    elif command -v brew &> /dev/null; then
        PACKAGE_MANAGER="brew"
        INSTALL_COMMAND="brew install"
        UPDATE_COMMAND="brew update"
    else
        print_error "Desteklenmeyen paket yöneticisi"
        exit 1
    fi
    
    print_verbose "Paket Yöneticisi: $PACKAGE_MANAGER"
    print_success "Sistem tespit edildi: $OS_TYPE $OS_VERSION ($PACKAGE_MANAGER)"
}

# Gereksinimleri kontrol et
check_requirements() {
    print_status "Gereksinimler kontrol ediliyor..."
    
    local missing_packages=()
    local optional_packages=()
    
    # Temel gereksinimler
    if ! command -v awesome &> /dev/null; then
        missing_packages+=("awesome")
    fi
    
    if ! command -v lua &> /dev/null; then
        missing_packages+=("lua")
    fi
    
    # X11 kontrolü (Linux için)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if ! command -v xrandr &> /dev/null; then
            missing_packages+=("xorg")
        fi
    fi
    
    # Opsiyonel paketler
    if ! command -v vicious &> /dev/null; then
        optional_packages+=("vicious")
    fi
    
    if ! command -v playerctl &> /dev/null; then
        optional_packages+=("playerctl")
    fi
    
    if ! command -v alacritty &> /dev/null; then
        optional_packages+=("alacritty")
    fi
    
    # Font kontrolü
    if ! fc-list | grep -i "jetbrains" &> /dev/null; then
        optional_packages+=("fonts-jetbrains-mono")
    fi
    
    # Sonuçları göster
    if [ ${#missing_packages[@]} -eq 0 ]; then
        print_success "Temel gereksinimler karşılanıyor"
    else
        print_warning "Eksik temel paketler: ${missing_packages[*]}"
    fi
    
    if [ ${#optional_packages[@]} -gt 0 ]; then
        print_warning "Önerilen paketler: ${optional_packages[*]}"
    fi
    
    # Eksik paketleri döndür
    echo "${missing_packages[@]}"
}

# Paket yükleme fonksiyonu
install_packages() {
    local packages=("$@")
    
    if [ ${#packages[@]} -eq 0 ]; then
        print_success "Yüklenecek paket yok"
        return 0
    fi
    
    print_status "Paketler yükleniyor: ${packages[*]}"
    
    # Paket listesini güncelle
    if [ "$PACKAGE_MANAGER" != "brew" ]; then
        print_verbose "Paket listesi güncelleniyor..."
        sudo $UPDATE_COMMAND
    fi
    
    # Paketleri yükle
    for package in "${packages[@]}"; do
        print_verbose "Yükleniyor: $package"
        
        case $PACKAGE_MANAGER in
            "apt")
                case $package in
                    "awesome") sudo apt install -y awesome awesome-extra ;;
                    "lua") sudo apt install -y lua5.4 lua5.4-dev ;;
                    "xorg") sudo apt install -y xorg ;;
                    "vicious") sudo apt install -y vicious ;;
                    "playerctl") sudo apt install -y playerctl ;;
                    "alacritty") sudo apt install -y alacritty ;;
                    "fonts-jetbrains-mono") sudo apt install -y fonts-jetbrains-mono ;;
                    *) sudo apt install -y "$package" ;;
                esac
                ;;
            "pacman")
                case $package in
                    "awesome") sudo pacman -S --noconfirm awesome ;;
                    "lua") sudo pacman -S --noconfirm lua ;;
                    "xorg") sudo pacman -S --noconfirm xorg ;;
                    "vicious") sudo pacman -S --noconfirm vicious ;;
                    "playerctl") sudo pacman -S --noconfirm playerctl ;;
                    "alacritty") sudo pacman -S --noconfirm alacritty ;;
                    "fonts-jetbrains-mono") sudo pacman -S --noconfirm ttf-jetbrains-mono ;;
                    *) sudo pacman -S --noconfirm "$package" ;;
                esac
                ;;
            "dnf")
                case $package in
                    "awesome") sudo dnf install -y awesome ;;
                    "lua") sudo dnf install -y lua ;;
                    "xorg") sudo dnf install -y xorg ;;
                    "vicious") sudo dnf install -y vicious ;;
                    "playerctl") sudo dnf install -y playerctl ;;
                    "alacritty") sudo dnf install -y alacritty ;;
                    "fonts-jetbrains-mono") sudo dnf install -y jetbrains-mono-fonts ;;
                    *) sudo dnf install -y "$package" ;;
                esac
                ;;
            "brew")
                case $package in
                    "awesome") brew install awesome ;;
                    "lua") brew install lua ;;
                    "vicious") brew install vicious ;;
                    "playerctl") brew install playerctl ;;
                    "alacritty") brew install alacritty ;;
                    "fonts-jetbrains-mono") brew install font-jetbrains-mono ;;
                    *) brew install "$package" ;;
                esac
                ;;
            *)
                sudo $INSTALL_COMMAND "$package"
                ;;
        esac
        
        if [ $? -eq 0 ]; then
            print_success "$package başarıyla yüklendi"
        else
            print_error "$package yüklenemedi"
            return 1
        fi
    done
    
    return 0
}

# LWM dosyalarını kopyala
install_lwm() {
    print_status "LWM dosyaları kuruluyor..."
    
    # Konfigürasyon dizini oluştur
    mkdir -p "$CONFIG_DIR"
    
    # Mevcut konfigürasyonu yedekle
    if [ -d "$CONFIG_DIR" ] && [ "$(ls -A "$CONFIG_DIR" 2>/dev/null)" ]; then
        print_warning "Mevcut AwesomeWM konfigürasyonu bulundu"
        if [ "$SKIP_CONFIRM" = false ]; then
            read -p "Yedeklemek istiyor musunuz? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cp -r "$CONFIG_DIR" "$BACKUP_DIR"
                print_success "Yedek oluşturuldu: $BACKUP_DIR"
            fi
        else
            cp -r "$CONFIG_DIR" "$BACKUP_DIR"
            print_success "Yedek oluşturuldu: $BACKUP_DIR"
        fi
    fi
    
    # LWM dosyalarını kopyala
    local files=("main.lua" "theme.lua" "widgets.lua" "rc.lua")
    for file in "${files[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            cp "$SCRIPT_DIR/$file" "$CONFIG_DIR/"
            print_verbose "$file kopyalandı"
        else
            print_warning "$file bulunamadı"
        fi
    done
    
    # Çalıştırma izni ver
    chmod +x "$CONFIG_DIR/main.lua" 2>/dev/null || true
    
    print_success "LWM dosyaları kuruldu: $CONFIG_DIR"
}

# Font cache'ini yenile
refresh_fonts() {
    print_status "Font cache yenileniyor..."
    
    if command -v fc-cache &> /dev/null; then
        fc-cache -fv
        print_success "Font cache yenilendi"
    else
        print_warning "fc-cache bulunamadı"
    fi
}

# Otomatik başlatma ayarla
setup_autostart() {
    print_status "Otomatik başlatma ayarlanıyor..."
    
    local xinitrc="$HOME/.xinitrc"
    local xsession="$HOME/.xsession"
    
    # .xinitrc dosyası
    if [ ! -f "$xinitrc" ]; then
        echo "exec awesome" > "$xinitrc"
        print_success ".xinitrc dosyası oluşturuldu"
    else
        if ! grep -q "exec awesome" "$xinitrc"; then
            echo "exec awesome" >> "$xinitrc"
            print_success ".xinitrc dosyasına awesome eklendi"
        else
            print_verbose ".xinitrc dosyası zaten awesome içeriyor"
        fi
    fi
    
    # .xsession dosyası
    if [ ! -f "$xsession" ]; then
        echo "exec awesome" > "$xsession"
        print_success ".xsession dosyası oluşturuldu"
    else
        if ! grep -q "exec awesome" "$xsession"; then
            echo "exec awesome" >> "$xsession"
            print_success ".xsession dosyasına awesome eklendi"
        else
            print_verbose ".xsession dosyası zaten awesome içeriyor"
        fi
    fi
}

# Sistem özel ayarlar
setup_system_specific() {
    print_status "Sistem özel ayarlar yapılandırılıyor..."
    
    case $OS_TYPE in
        *"Ubuntu"*|*"Debian"*|*"Linux Mint"*)
            # Ubuntu/Debian özel ayarlar
            if command -v gsettings &> /dev/null; then
                gsettings set org.gnome.desktop.interface enable-hot-corners false 2>/dev/null || true
            fi
            ;;
        *"Arch"*|*"Manjaro"*)
            # Arch özel ayarlar
            if command -v systemctl &> /dev/null; then
                sudo systemctl enable --user awesome 2>/dev/null || true
            fi
            ;;
        *"Fedora"*|*"Red Hat"*|*"CentOS"*)
            # Fedora özel ayarlar
            if command -v gsettings &> /dev/null; then
                gsettings set org.gnome.desktop.interface enable-hot-corners false 2>/dev/null || true
            fi
            ;;
        *"macOS"*)
            # macOS özel ayarlar
            print_warning "macOS'ta AwesomeWM sınırlı destek sunar"
            print_warning "X11 kurulumu gerekebilir"
            ;;
    esac
}

# Test kurulumu
test_installation() {
    print_status "Kurulum test ediliyor..."
    
    local tests_passed=0
    local total_tests=0
    
    # AwesomeWM kontrolü
    ((total_tests++))
    if command -v awesome &> /dev/null; then
        print_success "✅ AwesomeWM kuruldu"
        ((tests_passed++))
    else
        print_error "❌ AwesomeWM bulunamadı"
    fi
    
    # Lua kontrolü
    ((total_tests++))
    if command -v lua &> /dev/null; then
        print_success "✅ Lua kuruldu"
        ((tests_passed++))
    else
        print_error "❌ Lua bulunamadı"
    fi
    
    # Konfigürasyon dosyaları kontrolü
    ((total_tests++))
    if [ -f "$CONFIG_DIR/main.lua" ]; then
        print_success "✅ LWM konfigürasyonu kuruldu"
        ((tests_passed++))
    else
        print_error "❌ LWM konfigürasyonu bulunamadı"
    fi
    
    # Font kontrolü
    ((total_tests++))
    if fc-list | grep -i "jetbrains" &> /dev/null; then
        print_success "✅ JetBrains Mono font kuruldu"
        ((tests_passed++))
    else
        print_warning "⚠️ JetBrains Mono font bulunamadı"
    fi
    
    # Test sonucu
    if [ $tests_passed -eq $total_tests ]; then
        print_success "🎉 Tüm testler başarılı! ($tests_passed/$total_tests)"
        return 0
    else
        print_warning "⚠️ Bazı testler başarısız ($tests_passed/$total_tests)"
        return 1
    fi
}

# Yardım mesajı
show_help() {
    cat << EOF
LWM Akıllı Kurulum Script'i

Kullanım: $0 [SEÇENEK]

Seçenekler:
  -h, --help         Bu yardım mesajını göster
  -y, --yes          Tüm sorulara otomatik "evet" cevabı ver
  -v, --verbose      Detaylı çıktı göster
  -s, --skip-packages Sadece LWM kur, paketleri yükleme
  -t, --test         Sadece test yap, kurulum yapma
  -c, --check        Sadece gereksinimleri kontrol et
  -f, --force        Mevcut konfigürasyonu zorla üzerine yaz

Örnekler:
  $0                 Normal kurulum (etkileşimli)
  $0 -y              Otomatik kurulum
  $0 -s              Sadece LWM kur
  $0 -t              Sadece test
  $0 -c              Sadece gereksinim kontrolü
  $0 -v              Detaylı kurulum

Desteklenen Sistemler:
  • Ubuntu/Debian/Linux Mint (apt)
  • Arch Linux/Manjaro (pacman)
  • Fedora/CentOS/RHEL (dnf/yum)
  • openSUSE (zypper)
  • macOS (Homebrew)

EOF
}

# Ana fonksiyon
main() {
    # Argümanları işle
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -y|--yes)
                AUTO_INSTALL=true
                SKIP_CONFIRM=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -s|--skip-packages)
                SKIP_PACKAGES=true
                shift
                ;;
            -t|--test)
                TEST_ONLY=true
                shift
                ;;
            -c|--check)
                CHECK_ONLY=true
                shift
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            *)
                print_error "Bilinmeyen seçenek: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Sadece test modu
    if [ "$TEST_ONLY" = true ]; then
        detect_system
        test_installation
        exit $?
    fi
    
    # Sadece kontrol modu
    if [ "$CHECK_ONLY" = true ]; then
        detect_system
        check_requirements
        exit 0
    fi
    
    print_status "LWM akıllı kurulumu başlıyor..."
    
    # Sistem tespiti
    detect_system
    
    # Gereksinimleri kontrol et
    local missing_packages=($(check_requirements))
    
    # Paket kurulumu
    if [ "$SKIP_PACKAGES" = false ] && [ ${#missing_packages[@]} -gt 0 ]; then
        if [ "$AUTO_INSTALL" = false ]; then
            echo
            read -p "Eksik paketleri yüklemek istiyor musunuz? (Y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Nn]$ ]]; then
                print_warning "Paket kurulumu atlandı"
            else
                install_packages "${missing_packages[@]}"
            fi
        else
            install_packages "${missing_packages[@]}"
        fi
    fi
    
    # LWM kurulumu
    install_lwm
    
    # Font cache yenileme
    refresh_fonts
    
    # Otomatik başlatma
    setup_autostart
    
    # Sistem özel ayarlar
    setup_system_specific
    
    # Test
    test_installation
    
    # Başarı mesajı
    echo
    echo -e "${GREEN}🎉 LWM başarıyla kuruldu! 🎉${NC}"
    echo
    echo -e "${CYAN}Sonraki adımlar:${NC}"
    echo "1. Oturumu kapatın ve yeniden giriş yapın"
    echo "2. AwesomeWM'yi seçin"
    echo "3. Super + S tuşlarına basarak yardım menüsünü açın"
    echo
    echo -e "${YELLOW}Önemli kısayollar:${NC}"
    echo "• Super + Enter: Terminal aç"
    echo "• Super + R: Komut çalıştır"
    echo "• Super + S: Yardım menüsü"
    echo "• Super + Shift + Q: Çıkış"
    echo
    echo -e "${PURPLE}Daha fazla bilgi için README.md dosyasını okuyun.${NC}"
    echo
    echo -e "${BLUE}Konfigürasyon dizini:${NC} $CONFIG_DIR"
    if [ -d "$BACKUP_DIR" ]; then
        echo -e "${BLUE}Yedek dizini:${NC} $BACKUP_DIR"
    fi
}

# Script'i çalıştır
main "$@" 