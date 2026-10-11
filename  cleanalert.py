
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.clearcolor = (0.92, 0.97, 0.92, 1)


class CleanAlertApp(App):
    def build(self):
        self.laporan = []
        self.selesai = 0

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        judul = Label(
            text="CLEANALERT",
            font_size=28,
            bold=True,
            color=(0.05, 0.4, 0.15, 1),
            size_hint_y=None,
            height=55
        )
        root.add_widget(judul)

        root.add_widget(Label(
            text="Lapor dan Jaga Kebersihan Bersama!",
            size_hint_y=None,
            height=35,
            color=(0, 0, 0, 1)
        ))

        self.lokasi = TextInput(
            hint_text="Lokasi sampah (contoh: halaman sekolah)",
            multiline=False,
            size_hint_y=None,
            height=48
        )
        root.add_widget(self.lokasi)

        self.jenis = Spinner(
            text="Pilih jenis sampah",
            values=("Organik", "Anorganik", "Sampah campuran"),
            size_hint_y=None,
            height=48
        )
        root.add_widget(self.jenis)

        self.keterangan = TextInput(
            hint_text="Keterangan laporan",
            multiline=True,
            size_hint_y=None,
            height=75
        )
        root.add_widget(self.keterangan)

        tombol = Button(
            text="KIRIM LAPORAN",
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.6, 0.25, 1)
        )
        tombol.bind(on_press=self.kirim_laporan)
        root.add_widget(tombol)

        self.statistik = Label(
            text="Total laporan: 0 | Selesai: 0 | 0%",
            size_hint_y=None,
            height=40,
            color=(0, 0, 0, 1)
        )
        root.add_widget(self.statistik)

        root.add_widget(Label(
            text="DAFTAR LAPORAN",
            size_hint_y=None,
            height=35,
            color=(0.05, 0.4, 0.15, 1),
            bold=True
        ))

        scroll = ScrollView()
        self.daftar = BoxLayout(
            orientation="vertical",
            spacing=6,
            size_hint_y=None
        )
        self.daftar.bind(
            minimum_height=self.daftar.setter("height")
        )
        scroll.add_widget(self.daftar)
        root.add_widget(scroll)

        return root

    def kirim_laporan(self, tombol):
        lokasi = self.lokasi.text.strip()
        keterangan = self.keterangan.text.strip()
        jenis = self.jenis.text

        if not lokasi or not keterangan:
            self.statistik.text = "Isi lokasi dan keterangan dahulu!"
            return

        if jenis == "Pilih jenis sampah":
            self.statistik.text = "Pilih jenis sampah dahulu!"
            return

        laporan = {
            "lokasi": lokasi,
            "jenis": jenis,
            "keterangan": keterangan,
            "selesai": False
        }

        self.laporan.append(laporan)
        self.tampilkan_laporan(laporan)

        self.lokasi.text = ""
        self.keterangan.text = ""
        self.jenis.text = "Pilih jenis sampah"

        self.perbarui_statistik()

    def tampilkan_laporan(self, laporan):
        baris = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=100,
            padding=6
        )

        teks = Label(
            text=(
                f"Lokasi: {laporan['lokasi']}\n"
                f"Jenis: {laporan['jenis']}\n"
                f"Keterangan: {laporan['keterangan']}\n"
                "Status: Belum selesai"
            ),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle"
        )
        teks.bind(size=lambda obj, val:
                  setattr(obj, "text_size", val))
        baris.add_widget(teks)

        tombol = Button(
            text="Tandai Selesai",
            size_hint_y=None,
            height=38
        )

        def tandai_selesai(instance):
            if not laporan["selesai"]:
                laporan["selesai"] = True
                self.selesai += 1
                teks.text = (
                    f"Lokasi: {laporan['lokasi']}\n"
                    f"Jenis: {laporan['jenis']}\n"
                    f"Keterangan: {laporan['keterangan']}\n"
                    "Status: Selesai"
                )
                tombol.disabled = True
                self.perbarui_statistik()

        tombol.bind(on_press=tandai_selesai)
        baris.add_widget(tombol)
        self.daftar.add_widget(baris)

    def perbarui_statistik(self):
        total = len(self.laporan)
        persen = (self.selesai / total * 100) if total else 0

        self.statistik.text = (
            f"Total: {total} | Selesai: {self.selesai} "
            f"| Penyelesaian: {persen:.0f}%"
        )


if __name__ == "__main__":
    CleanAlertApp().run()
