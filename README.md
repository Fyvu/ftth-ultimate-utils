# FTTH Utils
ini adalah sebuah paket utilitas yang dapat membantu proses perencanaan FTTH

yang sudah tercantum disini adalah Macro untuk google earth yang dimana macro ini akan membantu dalam pengubahan icons serta warnanya dengan otomatisasi macro Autohotkey, jadi tidak perlu melakukan manual satu per satu dalam mengubah icons dan warnanya

## Cara Penggunaan: 
- install Autohotkey
- download macro (Google-earth-macros\myrep-ge-macro.ahk)
- jalankan macro

## Daftar Shortcut

### Shortcut Utilitas Umum
| Shortcut | Output |
| :--- | :--- |
| `Alt + Enter` (Ketik: `Alt + e`) | Eksekusi `Alt + Enter` (Membuka jendela Properties) |
| `Shift + Tab` | Pindah fokus ke sidebar folder |

### Pola Shortcut Ikon dan Warna

| Shortcut | Aksi |
|---|---|
| `Ctrl + Alt + [Key]` | **Placement** — mengganti ikon pada placemark spesifik |
| `Shift + Alt + [Key]` | **Folder** — mengganti ikon pada satu folder full |

Jika ikon memiliki lebih dari satu warna, setelah shortcut ditekan akan muncul prompt:
```
chose color mode (1-N)
```
Ketik nomor warna yang diinginkan (timeout 2 detik). Jika timeout atau input tidak valid, aksi dibatalkan.

---

## Daftar Ikon

### Slack — `S`
Satu warna, dipilih otomatis.
```
Ctrl/Shift + Alt + S
```
`1` : `#FF0000`

---

### FDT — `D`
```
Ctrl/Shift + Alt + D + [1-5]
```
`1` : `#AA00FF` | `2` : `#0000FF` | `3` : `#00FFFF` | `4` : `#FFFF00` | `5` : `#AA0000`

---

### FAT — `A`
```
Ctrl/Shift + Alt + A + [1-5]
```
`1` : `#00FF00` | `2` : `#FFFF00` | `3` : `#FF0000` | `4` : `#FF00FF` | `5` : `#000FF`

---

### Cable — `C`
```
Ctrl/Shift + Alt + C + [1-7]
```
`1` : `#00FF00` | `2` : `#FF00FF` | `3` : `#AA00FF` | `4` : `#550000` | `5` : `#FF0000` | `6` : `#FFFF00` | `7` : `#FFAA00`

---

### Home Pass — `H`
Satu warna, dipilih otomatis.
```
Ctrl/Shift + Alt + H
```
`1` : `#00FF00`

---

### Pole — `P`
```
Ctrl/Shift + Alt + P + [1-5]
```
`1` : `#FF0000` | `2` : `#00FF00` | `3` : `#00FFFF` | `4` : `#AA00FF` | `5` : `#550000`

---

### Joint Closure — `J`
```
Ctrl/Shift + Alt + J + [1-7]
```
`1` : `#00FF00` | `2` : `#FF00FF` | `3` : `#AA00FF` | `4` : `#550000` | `5` : `#FF0000` | `6` : `#FFFF00` | `7` : `#FFAA00`

---

### Sling Wire — `W`
Satu warna, dipilih otomatis.
```
Ctrl/Shift + Alt + W
```
`1` : `#00FFFF`

---

## Shortcut Utilitas

| Shortcut | Fungsi |
|---|---|
| `Alt + E` | Simulasi `Alt + Enter` (buka properties) |
| `Shift + Tab` | Simulasi `Tab` sebanyak 5 kali |

---

## Catatan

- Koordinat klik bersifat fixed — pastikan resolusi dan layout UI Google Earth tidak berubah.
- `globalDelay` (55ms): jeda antar klik, ubah jika diperlukan.
- `colorClick` (4x klik): digunakan untuk mengosongkan field warna sebelum input.
