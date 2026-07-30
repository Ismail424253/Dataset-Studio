# AI Prompt & Dataset Studio

## Proje Özeti

AI Prompt & Dataset Studio, büyük dil modelleri (LLM) için fine-tuning süreçlerinde kullanılacak verileri hazırlamaya yönelik bir iç araçtır. Bu araç ile prompt'lar oluşturulup versiyonlanabilir, versiyonlar arasındaki farklar karşılaştırılabilir (diff), prompt'lara etiketler atanabilir, bu prompt versiyonlarından ve karşılık gelen model çıktılarından oluşan veri setleri (dataset) bir araya getirilebilir. Oluşturulan veri setleri doğrulama (validation) ve tekrar tespiti (duplicate detection) adımlarından geçirildikten sonra JSONL, Alpaca ve ShareGPT formatlarında dışa aktarılabilir (export). Bu araç kesinlikle bir LLM çalıştırma veya eğitme aracı **değildir** — yalnızca fine-tuning için gerekli veriyi hazırlar, düzenler ve yönetir.

## Teknoloji Yığını (Tech Stack)

| Katman | Araç | Tercih Sebebi |
|---|---|---|
| **Backend** | Python + FastAPI | Hafif, hızlı geliştirmeye uygun; Swagger/OpenAPI dokümantasyonu otomatik olarak üretiliyor. Python'un veri işleme ekosistemi (json, csv, hashlib, difflib) bu proje için çok uygun. |
| **Veritabanı** | SQLite | Ayrı bir veritabanı sunucusu kurmaya gerek yok; tek dosya üzerinden çalışır. Düşük kaynaklı bilgisayarlarda bile sorunsuz çalışır. |
| **Frontend** | React + Vite + Tailwind CSS | Vite çok hızlı bir geliştirme sunucusu sağlıyor, düşük RAM kullanımıyla çalışır. React bileşen tabanlı yapısı ile karmaşık UI'ları yönetmeyi kolaylaştırır. Tailwind CSS ise hazır sınıflarla hızlı ve tutarlı tasarım yapmayı mümkün kılıyor. |
| **Diff (Fark Karşılaştırma)** | Python `difflib` (standart kütüphane) | Python ile birlikte geliyor, ek kurulum gerektirmiyor. İki metin versiyonu arasındaki farkları satır satır göstermek için yeterli. |
| **Token Tahmini** | `tiktoken` veya karakter/4 sezgisel yöntemi | Yerel olarak çalışır, internet bağlantısı veya GPU gerektirmez. Prompt uzunluğunu token cinsinden yaklaşık olarak hesaplamak için yeterli. |
| **Tekrar Tespiti** | `hashlib` (tam eşleşme) + opsiyonel `rapidfuzz` (yaklaşık benzerlik) | `hashlib` tamamen CPU tabanlı ve standart kütüphanede mevcut. Tam eşleşme tespiti için hash karşılaştırması yeterli. İlerleyen aşamada yaklaşık benzerlik gerekirse `rapidfuzz` eklenebilir. |
| **Versiyon Kontrolü** | Git + GitHub (ücretsiz plan) | Endüstri standardı; commit geçmişi proje değerlendirmesinin bir parçası. |

## Geliştirme Ortamı

| Araç | Versiyon |
|---|---|
| Python | 3.12.0 |
| Node.js | 24.18.0 |
| Git | 2.55.0 |

## Kurulum Talimatları

> **Not:** Backend (Gün 3) ve frontend (Gün 5) iskelet yapıları oluşturuldukça bu bölüm güncellenecektir.

### Backend

```bash
# Proje klasorune git
cd backend

# Sanal ortam olustur ve etkinlestir
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Bagimliliklari kur
pip install -r requirements.txt

# Veritabanini olustur (ilk calistirmada)
python database/init_db.py

# Sunucuyu baslat
uvicorn app.main:app --reload
```

Sunucu basladiktan sonra:
- API: http://127.0.0.1:8000
- Swagger UI (otomatik API dokumantasyonu): http://127.0.0.1:8000/docs

**Not:** Veritabani erisimi icin Python standart kutuphanesindeki `sqlite3` modulu kullanilmaktadir. Bu proje olceginde ORM (SQLAlchemy vb.) gereksiz karmasiklik ekleyecegi icin tercih edilmemistir.

### Frontend

```bash
# Gün 5'te eklenecek
```

## Proje Durumu ve Yol Haritası

Bu proje 20 iş günlük bir plan dahilinde geliştirilmektedir. Her 5 günde bir (Gün 5, 10, 15, 20) canlı demo içeren bir kontrol noktası (checkpoint) bulunmaktadır.

| Gün | Hedef | Durum |
|---|---|---|
| Gün 1 | Proje yapısı kurulumu, `.gitignore`, README hazırlanması | ✅ Tamamlandı |
| Gün 2 | Veritabanı şema tasarımı ve oluşturulması | ✅ Tamamlandı |
| Gün 3 | Backend iskelet yapısı (FastAPI) ve temel Prompt CRUD API | ✅ Tamamlandı |
| Gün 4 | Prompt CRUD API tamamlanması, hata yönetimi, test | 🔲 Planlandı |
| Gün 5 | Frontend iskelet yapısı (React+Vite+Tailwind), Prompt yönetimi UI — **Checkpoint #1** | 🔲 Planlandı |
| Gün 6-10 | Versiyonlama, Diff, Etiketleme — **Checkpoint #2** | 🔲 Planlandı |
| Gün 11-15 | Dataset oluşturma, JSONL/Alpaca/ShareGPT export — **Checkpoint #3** | 🔲 Planlandı |
| Gün 16-20 | Validation, Duplicate Detection, Token Tahmini, İstatistikler, Arama/Filtreleme, Son Demo — **Checkpoint #4** | 🔲 Planlandı |

## Veritabanı Şeması

Detaylı şema dökümantasyonu ve ER diyagramı için: [`docs/database-schema.md`](docs/database-schema.md)

### Tablolar

| Tablo | Açıklama | İlişki |
|---|---|---|
| `prompts` | Prompt kayıtları (id, title, created_at, updated_at) | — |
| `prompt_versions` | Versiyon geçmişi (id, prompt_id, version_no, content, created_at) | → prompts (1:N) |
| `tags` | Etiketler (id, name) | — |
| `prompt_tags` | Prompt-etiket ilişkisi (prompt_id, tag_id) | prompts ↔ tags (N:M) |
| `datasets` | Veri setleri (id, name, description, created_at) | — |
| `dataset_items` | Veri seti öğeleri (id, dataset_id, prompt_version_id, output_text) | → datasets (1:N), → prompt_versions (1:N) |

### ON DELETE Kararları

| İlişki | Davranış | Gerekçe |
|---|---|---|
| prompt_versions → prompts | **CASCADE** | Prompt silinince versiyonları da silinir |
| prompt_tags → prompts / tags | **CASCADE** | İlişkili kayıt silinince bağlantı da temizlenir |
| dataset_items → datasets | **CASCADE** | Veri seti silinince öğeleri de silinir |
| dataset_items → prompt_versions | **RESTRICT** | Bir veri setinde kullanılan prompt versiyonu silinemez — veri bütünlüğünü korur |

## Lisans

Bu proje bir staj projesi olarak geliştirilmektedir.
