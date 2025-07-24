from tkinter import PhotoImage
import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk


def veritabani_olustur():
    conn = sqlite3.connect("not_defteri.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS notlar
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       baslik
                       TEXT,
                       kategori
                       TEXT,
                       icerik
                       TEXT,
                       tarih
                       TEXT,
                       onem
                       TEXT
                       DEFAULT
                       'Orta'
                   )
                   """)
    conn.commit()
    conn.close()


def notlari_yukle():
    for widget in liste_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("not_defteri.db")
    cursor = conn.cursor()

    arama = arama_entry.get().strip()
    secilen_kategori = kategori_combo.get()

    if secilen_kategori == "Tüm Kategoriler":
        if arama:
            cursor.execute("SELECT * FROM notlar WHERE baslik LIKE ? ORDER BY tarih DESC", ('%' + arama + '%',))
        else:
            cursor.execute("SELECT * FROM notlar ORDER BY tarih DESC")
    else:
        if arama:
            cursor.execute("SELECT * FROM notlar WHERE kategori = ? AND baslik LIKE ? ORDER BY tarih DESC",
                           (secilen_kategori, '%' + arama + '%'))
        else:
            cursor.execute("SELECT * FROM notlar WHERE kategori = ? ORDER BY tarih DESC", (secilen_kategori,))

    notlar = cursor.fetchall()
    conn.close()

    renkler = {
        "Yüksek": ("#ff4757", "#ffffff"),
        "Orta": ("#ffa502", "#2f3542"),
        "Düşük": ("#2ed573", "#2f3542")
    }

    if not notlar:
        bos_label = customtkinter.CTkLabel(liste_frame,
                                           text="📝 Henüz not bulunmuyor\nİlk notunuzu eklemek için yukarıdaki butona tıklayın",
                                           font=("Segoe UI", 16), text_color="#7f8c8d")
        bos_label.pack(pady=50)
        return

    for i, not_ in enumerate(notlar):
        id, baslik, kategori, icerik, tarih, onem = not_
        bg_color, text_color = renkler.get(onem, ("#ecf0f1", "#2c3e50"))

        kart = customtkinter.CTkFrame(liste_frame, corner_radius=15, fg_color=bg_color, height=80)
        kart.pack(fill="x", pady=8, padx=15)
        kart.pack_propagate(False)
        sol_frame = customtkinter.CTkFrame(kart, fg_color="transparent")
        sol_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        baslik_label = customtkinter.CTkLabel(sol_frame, text=f"📌 {baslik}",
                                              font=("Segoe UI", 16, "bold"),
                                              text_color=text_color, anchor="w")
        baslik_label.pack(fill="x")
        alt_bilgi = f"📁 {kategori} • 📅 {tarih.split()[0]} • ⭐ {onem} Öncelik"
        alt_label = customtkinter.CTkLabel(sol_frame, text=alt_bilgi,
                                           font=("Segoe UI", 11),
                                           text_color=text_color, anchor="w")
        alt_label.pack(fill="x", pady=(5, 0))
        sag_frame = customtkinter.CTkFrame(kart, fg_color="transparent")
        sag_frame.pack(side="right", padx=10, pady=10)

        def duzenle_fonksiyonu(not_id=id, baslik=baslik, kategori=kategori, icerik=icerik, onem=onem):
            yeni_not_penceresi(guncelle=True, not_id=not_id, baslik=baslik, kategori=kategori, icerik=icerik, onem=onem)

        def sil_fonksiyonu(not_id=id):
            conn = sqlite3.connect("not_defteri.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notlar WHERE id = ?", (not_id,))
            conn.commit()
            conn.close()
            notlari_yukle()

        duzenle_buton = customtkinter.CTkButton(sag_frame, text="✏️", width=35, height=35,
                                                corner_radius=10, fg_color="#3498db",
                                                hover_color="#2980b9", command=duzenle_fonksiyonu)
        duzenle_buton.pack(side="top", pady=2)

        sil_buton = customtkinter.CTkButton(sag_frame, text="🗑️", width=35, height=35,
                                            corner_radius=10, fg_color="#e74c3c",
                                            hover_color="#c0392b", command=sil_fonksiyonu)
        sil_buton.pack(side="top")


def yeni_not_penceresi(guncelle=False, not_id=None, baslik="", kategori="Genel", icerik="", onem="Orta"):
    pencere = customtkinter.CTkToplevel(app)
    pencere.geometry("550x650")
    pencere.title("✏️ Not Düzenle" if guncelle else "➕ Yeni Not")
    pencere.attributes("-topmost", True)
    pencere.configure(fg_color="#f8f9fa")


    main_frame = customtkinter.CTkScrollableFrame(pencere, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    baslik_frame = customtkinter.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=15)
    baslik_frame.pack(fill="x", pady=(0, 15))
    customtkinter.CTkLabel(baslik_frame, text="📝 Başlık", font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))
    baslik_entry = customtkinter.CTkEntry(baslik_frame, width=480, height=40, font=("Segoe UI", 12),
                                          corner_radius=10, border_width=2)
    baslik_entry.insert(0, baslik)
    baslik_entry.pack(pady=(0, 15))
    secenekler_frame = customtkinter.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=15)
    secenekler_frame.pack(fill="x", pady=(0, 15))
    ic_frame = customtkinter.CTkFrame(secenekler_frame, fg_color="transparent")
    ic_frame.pack(fill="x", padx=15, pady=15)
    kat_frame = customtkinter.CTkFrame(ic_frame, fg_color="transparent")
    kat_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
    customtkinter.CTkLabel(kat_frame, text="📁 Kategori", font=("Segoe UI", 12, "bold")).pack()
    kategori_combo_pencere = customtkinter.CTkComboBox(kat_frame,
                                                       values=["Genel", "İş", "Kişisel", "Okul"],
                                                       width=200, height=35, corner_radius=10)
    kategori_combo_pencere.set(kategori if kategori in ["Genel", "İş", "Kişisel", "Okul"] else "Genel")
    kategori_combo_pencere.pack(pady=(5, 0))


    onem_frame = customtkinter.CTkFrame(ic_frame, fg_color="transparent")
    onem_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
    customtkinter.CTkLabel(onem_frame, text="⭐ Önem", font=("Segoe UI", 12, "bold")).pack()
    onem_combo = customtkinter.CTkComboBox(onem_frame, values=["Yüksek", "Orta", "Düşük"],
                                           width=200, height=35, corner_radius=10)
    onem_combo.set(onem if onem in ["Yüksek", "Orta", "Düşük"] else "Orta")
    onem_combo.pack(pady=(5, 0))

    icerik_frame = customtkinter.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=15)
    icerik_frame.pack(fill="both", expand=True, pady=(0, 15))
    customtkinter.CTkLabel(icerik_frame, text="📄 İçerik", font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))

    text_container = customtkinter.CTkFrame(icerik_frame, fg_color="#f8f9fa", corner_radius=10)
    text_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    text_widget = tk.Text(text_container, wrap="word", font=("Segoe UI", 11),
                          bg="#ffffff", fg="#2c3e50", relief="flat", bd=10,
                          insertbackground="#3498db", selectbackground="#3498db")
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)
    text_widget.insert("1.0", icerik)

    def kaydet_guncelle():
        yeni_baslik = baslik_entry.get().strip()
        yeni_kategori = kategori_combo_pencere.get()
        yeni_icerik = text_widget.get("1.0", "end-1c")
        yeni_onem = onem_combo.get()
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not yeni_baslik or not yeni_icerik.strip():
            return

        conn = sqlite3.connect("not_defteri.db")
        cursor = conn.cursor()

        if guncelle:
            cursor.execute(
                "UPDATE notlar SET baslik = ?, kategori = ?, icerik = ?, tarih = ?, onem = ? WHERE id = ?",
                (yeni_baslik, yeni_kategori, yeni_icerik, tarih, yeni_onem, not_id)
            )
        else:
            cursor.execute(
                "INSERT INTO notlar (baslik, kategori, icerik, tarih, onem) VALUES (?, ?, ?, ?, ?)",
                (yeni_baslik, yeni_kategori, yeni_icerik, tarih, yeni_onem)
            )

        conn.commit()
        conn.close()
        pencere.destroy()
        notlari_yukle()

    kaydet_buton = customtkinter.CTkButton(main_frame,
                                           text=f"{'💾 Güncelle' if guncelle else '💾 Kaydet'}",
                                           font=("Segoe UI", 14, "bold"),
                                           height=45, corner_radius=15,
                                           fg_color="#27ae60", hover_color="#229954",
                                           command=kaydet_guncelle)
    kaydet_buton.pack(fill="x")

veritabani_olustur()

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("800x750")
app.title("🗒️ Modern Not Defteri")
app.configure(fg_color="#ecf0f1")

header_frame = customtkinter.CTkFrame(app, height=100, corner_radius=20, fg_color="#2c3e50")
header_frame.pack(pady=20, padx=20, fill="x")
header_frame.pack_propagate(False)

customtkinter.CTkLabel(header_frame, text="🗒️ Modern Not Defteri",
                       font=("Segoe UI", 24, "bold"), text_color="#ffffff").pack(pady=30)

filtre_frame = customtkinter.CTkFrame(app, fg_color="#ffffff", corner_radius=15, height=80)
filtre_frame.pack(pady=(0, 20), padx=20, fill="x")
filtre_frame.pack_propagate(False)
filtre_ic = customtkinter.CTkFrame(filtre_frame, fg_color="transparent")
filtre_ic.pack(fill="both", expand=True, padx=20, pady=15)
arama_frame = customtkinter.CTkFrame(filtre_ic, fg_color="transparent")
arama_frame.pack(side="left", fill="both", expand=True)

customtkinter.CTkLabel(arama_frame, text="🔍 Ara:", font=("Segoe UI", 12, "bold")).pack(side="left")
arama_entry = customtkinter.CTkEntry(arama_frame, width=300, height=35, corner_radius=10,
                                     placeholder_text="Not başlığında ara...")
arama_entry.pack(side="left", padx=(10, 0))

kategori_frame = customtkinter.CTkFrame(filtre_ic, fg_color="transparent")
kategori_frame.pack(side="right")
customtkinter.CTkLabel(kategori_frame, text="📁 Kategori:", font=("Segoe UI", 12, "bold")).pack(side="left")
kategori_combo = customtkinter.CTkComboBox(kategori_frame,
                                           values=["Tüm Kategoriler", "Genel", "İş", "Kişisel", "Okul"],
                                           width=160, height=35, corner_radius=10)
kategori_combo.set("Tüm Kategoriler")
kategori_combo.pack(side="left", padx=(10, 0))


def filtrele_event(event=None):
    notlari_yukle()

arama_entry.bind("<KeyRelease>", filtrele_event)
kategori_combo.bind("<<ComboboxSelected>>", filtrele_event)

yeni_not_buton = customtkinter.CTkButton(app, text="➕ Yeni Not Ekle",
                                         height=50, font=("Segoe UI", 16, "bold"),
                                         corner_radius=15, fg_color="#3498db", hover_color="#2980b9",
                                         command=lambda: yeni_not_penceresi())
yeni_not_buton.pack(pady=(0, 20), padx=20, fill="x")
liste_frame = customtkinter.CTkScrollableFrame(app, corner_radius=15, fg_color="#ffffff")
liste_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)

notlari_yukle()
app.mainloop()
