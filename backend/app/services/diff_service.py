"""
Diff servisi — iki metin arasindaki farklari hesaplar.
difflib.ndiff kullanilarak satir bazli karsilastirma yapilir.
"""

import difflib


def compute_diff(content_a: str, content_b: str) -> list[dict]:
    """
    Iki icerik arasindaki farki satir bazli hesaplar.

    Args:
        content_a: Ilk versiyonun icerigi
        content_b: Ikinci versiyonun icerigi

    Returns:
        Diff satirlarinin listesi. Her eleman {"type": "...", "text": "..."} formatindadir.
        type degerleri: "unchanged", "added", "removed"
    """
    lines_a = content_a.splitlines(keepends=True)
    lines_b = content_b.splitlines(keepends=True)

    result = []
    diff = difflib.ndiff(lines_a, lines_b)

    for line in diff:
        # ndiff ciktisi: '  ' (degismemis), '+ ' (eklenmis), '- ' (kaldirilmis), '? ' (ipucu)
        if line.startswith('  '):
            result.append({"type": "unchanged", "text": line[2:].rstrip('\n')})
        elif line.startswith('+ '):
            result.append({"type": "added", "text": line[2:].rstrip('\n')})
        elif line.startswith('- '):
            result.append({"type": "removed", "text": line[2:].rstrip('\n')})
        # '? ' satirlari (ipucu satirlari) atlanir — frontend icin gereksiz

    return result
