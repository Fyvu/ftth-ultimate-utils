#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║         KML Boundary Auto-Labeler            ║
║  Melabeli ulang Placemark<Polygon> di KML    ║
╚══════════════════════════════════════════════╝

Cara penggunaan:
  python kml_labeler.py
  python kml_labeler.py path/ke/file.kml

Dependensi opsional (output lebih rapi):
  pip install lxml
"""

import os
import re
import sys


# ═══════════════════════════════════════════════
#  HELPER: Namespace
# ═══════════════════════════════════════════════

def extract_ns(tag: str) -> str:
    """Ekstrak prefix namespace dari tag XML, misal '{http://...}'."""
    m = re.match(r'(\{[^}]+\})', tag)
    return m.group(1) if m else ''


def ns_tag(ns: str, local: str) -> str:
    """Gabungkan namespace prefix dengan nama lokal tag."""
    return f'{ns}{local}' if ns else local


# ═══════════════════════════════════════════════
#  LOAD & SAVE KML
# ═══════════════════════════════════════════════

def load_kml(path: str):
    """
    Muat file KML. Mencoba lxml terlebih dahulu,
    jika tidak tersedia jatuh ke xml.etree.ElementTree.

    Return: (tree, root, use_lxml: bool)
    """
    try:
        from lxml import etree as ET
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(path, parser)
        return tree, tree.getroot(), True

    except ImportError:
        import xml.etree.ElementTree as ET

        # Daftarkan namespace umum KML agar tidak di-rename saat disimpan
        known_ns = {
            '':      'http://www.opengis.net/kml/2.2',
            'gx':    'http://www.google.com/kml/ext/2.2',
            'kml':   'http://www.opengis.net/kml/2.2',
            'atom':  'http://www.w3.org/2005/Atom',
            'xsi':   'http://www.w3.org/2001/XMLSchema-instance',
        }
        for prefix, uri in known_ns.items():
            ET.register_namespace(prefix, uri)

        tree = ET.parse(path)
        return tree, tree.getroot(), False


def save_kml(tree, path: str, use_lxml: bool) -> None:
    """Simpan tree yang telah dimodifikasi ke file output."""
    if use_lxml:
        from lxml import etree as ET
        tree.write(
            path,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )
    else:
        import xml.etree.ElementTree as ET
        # ET.indent tersedia mulai Python 3.9
        if hasattr(ET, 'indent'):
            ET.indent(tree.getroot(), space='  ')
        tree.write(path, xml_declaration=True, encoding='unicode')


# ═══════════════════════════════════════════════
#  CORE: Cari & Labeli Placemark<Polygon>
# ═══════════════════════════════════════════════

def find_boundary_placemarks(root):
    """
    Temukan semua elemen <Placemark> yang mengandung <Polygon>,
    diurutkan berdasarkan urutan hierarki dalam dokumen (atas → bawah).

    Return: (list_of_placemark_elements, namespace_prefix: str)
    """
    ns            = extract_ns(root.tag)
    placemark_tag = ns_tag(ns, 'Placemark')
    polygon_tag   = ns_tag(ns, 'Polygon')

    result = []
    for pm in root.iter(placemark_tag):
        # Periksa Polygon dengan atau tanpa namespace
        has_polygon = (
            pm.find(f'.//{polygon_tag}') is not None or
            pm.find('.//Polygon')        is not None
        )
        if has_polygon:
            result.append(pm)

    return result, ns


def create_name_element(tag: str, text: str, use_lxml: bool):
    """Buat elemen <name> baru."""
    if use_lxml:
        from lxml import etree as ET
    else:
        import xml.etree.ElementTree as ET

    elem      = ET.Element(tag)
    elem.text = text
    return elem


def label_placemarks(placemarks, ns: str, prefix: str, use_lxml: bool):
    """
    Terapkan label baru ke setiap Placemark boundary.
    Format  : {prefix}{nomor:02d}  — misal A01, A02, …

    Return  : list of (nama_lama, nama_baru) untuk ditampilkan
    """
    name_tag = ns_tag(ns, 'name')
    changes  = []

    for i, pm in enumerate(placemarks, start=1):
        new_label = f"{prefix}{i:02d}"

        # Cari elemen <name> (dengan atau tanpa namespace)
        name_elem = pm.find(name_tag)
        if name_elem is None:
            name_elem = pm.find('name')

        if name_elem is not None:
            old_label     = name_elem.text or "(kosong)"
            name_elem.text = new_label
        else:
            # Tidak ada <name> — buat baru, sisipkan di posisi pertama
            old_label = "(tidak ada)"
            new_elem  = create_name_element(name_tag, new_label, use_lxml)
            pm.insert(0, new_elem)

        changes.append((old_label, new_label))

    return changes


# ═══════════════════════════════════════════════
#  INPUT HELPER
# ═══════════════════════════════════════════════

def ask_file_path() -> str:
    """Minta path file KML dari pengguna."""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip().strip("'\"")
    return input("\n  Path file KML  : ").strip().strip("'\"")


def ask_prefix() -> str:
    """Minta prefix label dari pengguna (harus huruf alphabet)."""
    while True:
        prefix = input("  Prefix label   : ").strip().upper()
        if prefix and prefix.isalpha():
            return prefix
        print("  [!] Prefix harus berupa huruf A-Z dan tidak boleh kosong.\n")


# ═══════════════════════════════════════════════
#  DISPLAY HELPER
# ═══════════════════════════════════════════════

def print_banner():
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         KML Boundary Auto-Labeler            ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()


def print_preview(changes):
    """Tampilkan tabel perubahan nama (Nama Lama → Nama Baru)."""
    col_w = max((len(old) for old, _ in changes), default=10)
    col_w = max(col_w, 15) + 2
    sep   = "  " + "─" * (6 + col_w + 12)

    print(f"\n  {'No.':<6} {'Nama Lama':<{col_w}} Nama Baru")
    print(sep)
    for i, (old, new) in enumerate(changes, 1):
        print(f"  {i:<6} {old:<{col_w}} {new}")
    print(sep)


# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════

def main():
    print_banner()

    # ── 1. Input file ─────────────────────────
    input_file = ask_file_path()

    if not os.path.isfile(input_file):
        print(f"\n  [ERROR] File tidak ditemukan: '{input_file}'")
        sys.exit(1)

    if not input_file.lower().endswith('.kml'):
        ans = input("  [WARN]  Ekstensi bukan .kml, lanjutkan? (y/n): ").strip().lower()
        if ans != 'y':
            print("  Dibatalkan.")
            sys.exit(0)

    # ── 2. Input prefix ───────────────────────
    prefix = ask_prefix()

    # ── 3. Muat KML ───────────────────────────
    print(f"\n  [INFO] Memuat file  : {os.path.basename(input_file)}")

    try:
        tree, root, use_lxml = load_kml(input_file)
    except Exception as e:
        print(f"\n  [ERROR] Gagal membaca file KML: {e}")
        sys.exit(1)

    lib_name = "lxml" if use_lxml else "xml.etree.ElementTree"
    print(f"  [INFO] Library XML  : {lib_name}")

    # ── 4. Temukan boundary Placemarks ────────
    placemarks, ns = find_boundary_placemarks(root)

    if not placemarks:
        print("\n  [ERROR] Tidak ditemukan elemen Placemark yang mengandung "
              "<Polygon> dalam file.")
        sys.exit(1)

    total = len(placemarks)
    print(f"  [INFO] Boundary     : {total} elemen ditemukan")

    # ── 5. Terapkan label ─────────────────────
    changes = label_placemarks(placemarks, ns, prefix, use_lxml)

    # ── 6. Tampilkan preview ──────────────────
    print_preview(changes)

    # ── 7. Simpan output ──────────────────────
    base     = os.path.splitext(os.path.basename(input_file))[0]
    out_dir  = os.path.dirname(os.path.abspath(input_file))
    out_path = os.path.join(out_dir, f"{base}-LABELED.kml")

    try:
        save_kml(tree, out_path, use_lxml)
    except Exception as e:
        print(f"\n  [ERROR] Gagal menyimpan file: {e}")
        sys.exit(1)

    # ── 8. Ringkasan ──────────────────────────
    print(f"\n  [SUKSES] {total} label berhasil diterapkan.")
    print(f"  [OUTPUT] {out_path}")
    print()


if __name__ == "__main__":
    main()
