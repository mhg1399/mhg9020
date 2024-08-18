from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.colorpicker import ColorPicker
import requests
import json
import urllib.parse

class MusicAdvisorApp(App):
    def build(self):
        self.api_url = 'https://api.deezer.com'
        self.api_endpoint = '/search'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.music_name_label = Label(text="Music Name:")
        layout.add_widget(self.music_name_label)

        self.music_name_entry = TextInput(size_hint_y=None, height=30)
        layout.add_widget(self.music_name_entry)

        self.search_button = Button(text="Search for Similar Music", size_hint_y=None, height=50)
        self.search_button.bind(on_press=self.search_music)
        layout.add_widget(self.search_button)

        self.result_text = ScrollView(size_hint=(1, 1))
        self.result_label = TextInput(size_hint_y=None, text="Results will be displayed here.", height=600, readonly=True)
        self.result_text.add_widget(self.result_label)
        layout.add_widget(self.result_text)

        self.bg_color_button = Button(text="Choose Background Color", size_hint_y=None, height=50)
        self.bg_color_button.bind(on_press=self.choose_bg_color)
        layout.add_widget(self.bg_color_button)

        return layout

    def search_music(self, instance):
        music_name = self.music_name_entry.text.strip()
        if not music_name:
            self.result_label.text = "Please enter the name of the music."
            return

        try:
            url = f'{self.api_url}/search?q={urllib.parse.quote(music_name)}'
            response = requests.get(url)
            data = response.json()

            if 'data' in data:
                results = "Similar music for '{}':\n".format(music_name)
                for track in data['data']:
                    title = track.get('title', 'Title not available')
                    artist = track.get('artist', {}).get('name', 'Artist name not available')
                    preview_url = track.get('preview', 'Preview URL not available')
                    results += f"{title} - {artist}\nPreview: {preview_url}\n\n"
                self.result_label.text = results
                # Ensure text wraps correctly
                self.result_label.text_size = (self.result_label.width, None)
            else:
                self.result_label.text = "No similar music found."
        except Exception as e:
            self.result_label.text = f"An error occurred: {e}"

    def choose_bg_color(self, instance):
        color_picker = ColorPicker()
        color_picker.bind(color=self.update_bg_color)
        self.root.add_widget(color_picker)

    def update_bg_color(self, instance, value):
        color = value[0], value[1], value[2], 1
        self.root.background_color = color

if __name__ == '__main__':
    MusicAdvisorApp().run()
