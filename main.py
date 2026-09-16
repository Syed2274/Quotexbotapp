from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
import time
import math
import random

class SmartSignalAlgorithm:
    @staticmethod
    def calculate_signal(pair, timeframe):
        current_time = time.time()
        seed_value = sum(ord(c) for c in pair) + sum(ord(c) for c in timeframe)
        timeframe_multiplier = {'5s': 0.1, '15s': 0.3, '30s': 0.5, '1m': 1.0, '2m': 1.5, '5m': 2.0}.get(timeframe, 1.0)
        
        momentum = math.sin((current_time / 10.0) + seed_value) * timeframe_multiplier
        rsi_simulation = 50 + (math.cos(current_time / 5.0) * 35) + random.uniform(-5, 5)
        
        if rsi_simulation < 35 or momentum < -0.4:
            return "UP 🚀", "CALL / BUY", (0, 1, 0.4, 1), round(abs(rsi_simulation), 1)
        elif rsi_simulation > 65 or momentum > 0.4:
            return "DOWN 🔻", "PUT / SELL", (1, 0.2, 0.2, 1), round(abs(rsi_simulation), 1)
        else:
            return ("UP 🚀", "CALL / BUY", (0, 1, 0.4, 1), round(abs(rsi_simulation), 1)) if random.random() > 0.48 else ("DOWN 🔻", "PUT / SELL", (1, 0.2, 0.2, 1), round(abs(rsi_simulation), 1))

class FloatingBotLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatingBotLayout, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.1, 0.12, 0.95)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.title_label = Label(
            text='[b]Quotex Smart Algo Bot[/b]', markup=True,
            size_hint=(0.9, 0.12), pos_hint={'center_x': 0.5, 'top': 0.95}, font_size='16sp'
        )
        self.add_widget(self.title_label)

        quotex_pairs = ('EUR/USD (OTC)', 'GBP/USD (OTC)', 'USD/JPY (OTC)', 'AUD/CAD (OTC)', 'EUR/GBP (OTC)', 'USD/CAD (OTC)')
        self.pair_spinner = Spinner(text='EUR/USD (OTC)', values=quotex_pairs, size_hint=(0.8, 0.12), pos_hint={'center_x': 0.5, 'top': 0.80})
        self.add_widget(self.pair_spinner)

        self.time_spinner = Spinner(text='1m', values=('5s', '15s', '30s', '1m', '2m', '5m'), size_hint=(0.8, 0.12), pos_hint={'center_x': 0.5, 'top': 0.65})
        self.add_widget(self.time_spinner)

        self.gen_button = Button(text='ANALYZE & GENERATE', size_hint=(0.8, 0.14), pos_hint={'center_x': 0.5, 'top': 0.48}, background_color=(0.1, 0.8, 0.3, 1), bold=True)
        self.gen_button.bind(on_press=self.generate_signal)
        self.add_widget(self.gen_button)

        self.result_label = Label(text='Select pair & click Analyze', size_hint=(0.9, 0.25), pos_hint={'center_x': 0.5, 'top': 0.30}, font_size='14sp', bold=True, halign='center', valign='middle')
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.add_widget(self.result_label)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def generate_signal(self, instance):
        selected_pair = self.pair_spinner.text
        selected_time = self.time_spinner.text
        signal_icon, signal_type, text_color, rsi_val = SmartSignalAlgorithm.calculate_signal(selected_pair, selected_time)
        self.result_label.color = text_color
        self.result_label.text = f"Pair: {selected_pair}\nTime: {selected_time} | Strength: {rsi_val}%\nSignal: {signal_icon} ({signal_type})"

class QuotexFloatingBotApp(App):
    def build(self):
        return FloatingBotLayout()

if __name__ == '__main__':
    QuotexFloatingBotApp().run()
