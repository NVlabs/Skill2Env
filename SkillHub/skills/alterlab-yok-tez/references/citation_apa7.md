# Citing a YÖK thesis — Türkçe APA-7

Source: tr:yok-tez research findings (pre-verified). The key move is mapping the
YÖK **Tez No** to APA-7's **Yayın No.** (publication number) for published
theses, and switching template by access state.

## The Tez No → Yayın No. mapping

Ulusal Tez Merkezi assigns each thesis a **Tez No** (thesis number). In a
Türkçe APA-7 reference, an *İzinli* (permitted, "published") thesis takes that
number as the parenthetical **Yayın No.** A restricted/unpublished thesis has no
Yayın No. and uses the "unpublished" form.

## Published / permitted (has a Yayın No.)

```
Soyad, A. (Yıl). Tez başlığı (Yayın No. NNNNNN) [Tez türü, Üniversite Adı].
YÖK Ulusal Tez Merkezi.
```

- *Tez başlığı* is italicized.
- *Tez türü* = the thesis type, e.g. **Doktora tezi**, **Yüksek lisans tezi**.
- Archive name is literally **YÖK Ulusal Tez Merkezi**.

Worked example:

```
Yılmaz, A. (2021). Sanal prodüksiyonun sinematografiye etkileri
(Yayın No. 654321) [Doktora tezi, İzmir Ekonomi Üniversitesi].
YÖK Ulusal Tez Merkezi.
```

## Unpublished / restricted (no Yayın No.)

```
Soyad, A. (Yıl). Tez başlığı [Yayımlanmamış tez türü tezi]. Üniversite Adı.
```

Worked example:

```
Demir, B. (2019). Etkileşimli medyada izleyici deneyimi
[Yayımlanmamış yüksek lisans tezi]. Ege Üniversitesi.
```

## Optional BibTeX

```bibtex
@phdthesis{yilmaz2021,
  author = {Yılmaz, Ayşe},
  title  = {Sanal prodüksiyonun sinematografiye etkileri},
  school = {İzmir Ekonomi Üniversitesi},
  year   = {2021},
  note   = {YÖK Ulusal Tez Merkezi, Tez No. 654321}
}
```

Use `@mastersthesis` for a *yüksek lisans* thesis. Preserve Turkish diacritics in
all author/title/institution strings.

## Reminders

- Take the **Tez No, year, author, university, and type directly from the YÖK
  record** — do not infer or invent any of them.
- Keep diacritics intact (İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü).
- Match *Tez türü* exactly to the record's type label.
