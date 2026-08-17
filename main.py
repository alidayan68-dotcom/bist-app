# -*- coding: utf-8 -*-
import threading
import requests
import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

DEFAULT_HISSELER = [
    "ACSEL", "ADEL", "ADESE", "AEFES", "AFYON", "AKBNK", "AKSA", 
    "ALARK", "ARCLK", "ASELS", "ASTOR", "BIMAS", "EREGL", "FROTO", 
    "GARAN", "HEKTS", "KCHOL", "KOZAL", "SASA", "SISE", "THYAO", "TUPRS"
]

class BISTApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        self.add_widget(Label(text="[b]BIST Mobil Tarayıcı[/b]", markup=True, size_hint_y=None, height=40, font_size='20sp'))

        self.btn_scan = Button(text="Taramayı Başlat", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        self.btn_scan.bind(on_release=self.start_scan)
        self.add_widget(self.btn_scan)

        self.lbl_status = Label(text="Hazır", size_hint_y=None, height=30)
        self.add_widget(self.lbl_status)

        self.progress = ProgressBar(max=100, size_hint_y=None, height=15)
        self.add_widget(self.progress)

        self.scroll_view = ScrollView()
        self.results_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.results_grid.bind(minimum_height=self.results_grid.setter('height'))
        self.scroll_view.add_widget(self.results_grid)
        self.add_widget(self.scroll_view)

    def start_scan(self, instance):
        self.btn_scan.disabled = True
        self.results_grid.clear_widgets()
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        total = len(DEFAULT_HISSELER)
        for idx, symbol in enumerate(DEFAULT_HISSELER, 1):
            pct = (idx / total) * 100
            Clock.schedule_once(lambda dt, p=pct, i=idx, t=total: self._update_ui(p, f"Taranıyor: {i}/{t}"))
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.IS?range=1mo&interval=1d"
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url, headers=headers, timeout=4)
                if res.status_code == 200:
                    data = res.json()
                    closes = [c for c in data['chart']['result'][0]['indicators']['quote'][0]['close'] if c is not None]
                    if len(closes) >= 2:
                        last = closes[-1]
                        prev = closes[-2]
                        diff = ((last - prev) / prev) * 100
                        res_text = f"{symbol}: {last:.2f} TL (%{diff:+.2f})"
                        Clock.schedule_once(lambda dt, r=res_text: self._add_item(r))
            except Exception:
                pass

        Clock.schedule_once(lambda dt: self._finish())

    def _update_ui(self, pct, text):
        self.progress.value = pct
        self.lbl_status.text = text

    def _add_item(self, text):
        self.results_grid.add_widget(Label(text=text, size_hint_y=None, height=30))

    def _finish(self):
        self.btn_scan.disabled = False
        self.lbl_status.text = "Tarama Tamamlandı!"

class MainApp(App):
    def build(self):
        return BISTApp()

if __name__ == '__main__':
    MainApp().run()
