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
# Gün 3'te eklenecek
```

### Frontend

```bash
# Gün 5'te eklenecek
```

## Proje Durumu ve Yol Haritası

Bu proje 20 iş günlük bir plan dahilinde geliştirilmektedir. Her 5 günde bir (Gün 5, 10, 15, 20) canlı demo içeren bir kontrol noktası (checkpoint) bulunmaktadır.

| Gün | Hedef | Durum |
|---|---|---|
| Gün 1 | Proje yapısı kurulumu, `.gitignore`, README hazırlanması | ✅ Tamamlandı |
| Gün 2 | Veritabanı şema tasarımı ve oluşturulması | 🔲 Planlandı |
| Gün 3 | Backend iskelet yapısı (FastAPI) ve temel Prompt CRUD API | 🔲 Planlandı |
| Gün 4 | Prompt CRUD API tamamlanması, hata yönetimi, test | 🔲 Planlandı |
| Gün 5 | Frontend iskelet yapısı (React+Vite+Tailwind), Prompt yönetimi UI — **Checkpoint #1** | 🔲 Planlandı |
| Gün 6-10 | Versiyonlama, Diff, Etiketleme — **Checkpoint #2** | 🔲 Planlandı |
| Gün 11-15 | Dataset oluşturma, JSONL/Alpaca/ShareGPT export — **Checkpoint #3** | 🔲 Planlandı |
| Gün 16-20 | Validation, Duplicate Detection, Token Tahmini, İstatistikler, Arama/Filtreleme, Son Demo — **Checkpoint #4** | 🔲 Planlandı |

## Veritabanı Şeması

Veritabanı şeması Gün 2'de tasarlanacak ve bu bölüm güncellenecektir. Planlanan tablolar:

- `prompts` — Prompt kayıtları
- `prompt_versions` — Her prompt'un versiyon geçmişi
- `tags` — Etiketler
- `prompt_tags` — Prompt-etiket ilişkisi (çoka-çok)
- `datasets` — Veri setleri
- `dataset_items` — Veri seti öğeleri (prompt versiyonu + model çıktısı)

## Lisans

Bu proje bir staj projesi olarak geliştirilmektedir.
