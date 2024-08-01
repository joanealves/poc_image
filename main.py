from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import os
import shutil

KV = '''
BoxLayout:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(56)
        padding: dp(10)
        spacing: dp(10)
        
        Button:
            text: "Selecionar Imagens"
            on_release: app.select_images()

        Button:
            text: "Salvar Selecionadas"
            on_release: app.save_selected_images()

    ScrollView:
        GridLayout:
            id: image_grid
            cols: 2
            padding: dp(10)
            spacing: [dp(10), dp(16)]
            size_hint_y: None
            row_default_height: '300dp'
            row_force_default: True
            height: self.minimum_height
'''

class ImageManagerApp(App):

    def build(self):
        self.root = Builder.load_string(KV)
        self.load_default_images()
        return self.root


    def load_default_images(self):
        ref_dir = 'assets/ref'
        comp_dir = 'assets/comp'

         #definido o diretório das imagens
        ref_images = sorted(os.listdir(ref_dir))
        comp_images = sorted(os.listdir(comp_dir))

        #acessa o widget onde a imagem vai ser exibida
        grid = self.root.ids.image_grid

        #Itera sobre as listas de imagem simultaneamente, e constroi os caminhos completos de cada imagem

        for ref_img, comp_img in zip(ref_images, comp_images):
            ref_path = os.path.join(ref_dir, ref_img)
            comp_path = os.path.join(comp_dir, comp_img)
            
            img_ref_box = BoxLayout(orientation='vertical', size_hint_y=None, height='300dp')
            img_comp_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='300dp')

            img_ref = Image(source=ref_path, size_hint_y=None, height='300dp')
            img_ref.bind(on_touch_down=self.on_image_click)
            img_ref_box.add_widget(img_ref)
            
            img_comp = Image(source=comp_path, size_hint_y=None, height='300dp')
            img_comp.bind(on_touch_down=self.on_image_click)
            comp_controls_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(48), dp(300)), spacing=dp(10))
            checkbox = CheckBox(size_hint=(None, None), size=(dp(48), dp(48)))
            checkbox.color = [0, 0, 0, 1]  # Preto
            comp_controls_box.add_widget(checkbox)
            delete_button = Button(text='Excluir', size_hint=(None, None), size=(dp(48), dp(48)))
            delete_button.bind(on_release=lambda x, img=img_comp: self.delete_image(img))
            comp_controls_box.add_widget(delete_button)
            img_comp_box.add_widget(img_comp)
            img_comp_box.add_widget(comp_controls_box)
            
            grid.add_widget(img_ref_box)
            grid.add_widget(img_comp_box)

    def on_image_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.show_image_carousel(instance.source)

    def show_image_carousel(self, current_image):
        grid = self.root.ids.image_grid
        images = [child.children[0].source for child in grid.children if isinstance(child, BoxLayout) and isinstance(child.children[0], Image)]

        self.carousel = Carousel(direction='right', loop=True)
        for img_source in images:
            img = Image(source=img_source)
            self.carousel.add_widget(img)

        if current_image in images:
            self.carousel.index = images.index(current_image)

        layout = FloatLayout()
        layout.add_widget(self.carousel)

        left_arrow = Button(text='<', size_hint=(None, None), size=(dp(48), dp(48)), pos_hint={'center_y': 0.5, 'x': 0})
        right_arrow = Button(text='>', size_hint=(None, None), size=(dp(48), dp(48)), pos_hint={'center_y': 0.5, 'right': 1})
        
        left_arrow.bind(on_release=lambda x: self.carousel.load_previous())
        right_arrow.bind(on_release=lambda x: self.carousel.load_next())

        layout.add_widget(left_arrow)
        layout.add_widget(right_arrow)

        self.carousel_popup = Popup(title='Visualizar Imagens', content=layout, size_hint=(1, 1))
        self.carousel_popup.open()

    def select_images(self):
        content = FileChooserIconView(multiselect=True, on_selection=self.load_images)
        self.file_chooser = Popup(title="Selecionar Imagens", content=content, size_hint=(0.9, 0.9))
        self.file_chooser.open()

    def load_images(self, filechooser, selection):
        self.file_chooser.dismiss()
        if not selection:
            return

        grid = self.root.ids.image_grid
        for img_path in selection:
            img_ref_box = BoxLayout(orientation='vertical', size_hint_y=None, height='300dp')
            img_comp_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='300dp')

            img_ref = Image(source=img_path, size_hint_y=None, height='300dp')
            img_ref.bind(on_touch_down=self.on_image_click)
            img_ref_box.add_widget(img_ref)
            
            img_comp = Image(source=img_path, size_hint_y=None, height='300dp')
            img_comp.bind(on_touch_down(self.on_image_click))
            comp_controls_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(48), dp(300)), spacing=dp(10))
            checkbox = CheckBox(size_hint=(None, None), size=(dp(48), dp(48)))
            checkbox.color = [0, 0, 0, 1]  # Preto
            comp_controls_box.add_widget(checkbox)
            delete_button = Button(text='Excluir', size_hint=(None, None), size=(dp(48), dp(48)))
            delete_button.bind(on_release=lambda x, img=img_comp: self.delete_image(img))
            comp_controls_box.add_widget(delete_button)
            img_comp_box.add_widget(img_comp)
            img_comp_box.add_widget(comp_controls_box)
            
            grid.add_widget(img_ref_box)
            grid.add_widget(img_comp_box)

    def delete_image(self, img):
        parent = img.parent
        grid = self.root.ids.image_grid
        grid.remove_widget(parent)

    def save_selected_images(self):
        grid = self.root.ids.image_grid
        selected_images = []

        for child in grid.children:
            if isinstance(child, BoxLayout) and len(child.children) > 1:
                controls_box = child.children[1]
                if isinstance(controls_box, BoxLayout) and len(controls_box.children) > 0:
                    checkbox = controls_box.children[0]
                    if isinstance(checkbox, CheckBox) and checkbox.active:
                        img_widget = child.children[0].children[0] if len(child.children[0].children) > 0 else None
                        if isinstance(img_widget, Image):
                            selected_images.append(img_widget.source)

        if selected_images:
            content = FileChooserIconView(on_submit=self.save_images)
            self.save_dialog = Popup(title="Escolher Pasta para Salvar", content=content, size_hint=(0.9, 0.9))
            self.save_dialog.selected_images = selected_images
            self.save_dialog.open()

    def save_images(self, filechooser, selection, touch):
        self.save_dialog.dismiss()
        if not selection:
            return

        save_dir = selection[0]
        selected_images = self.save_dialog.selected_images

        for img_path in selected_images:
            try:
                shutil.copy(img_path, save_dir)
            except Exception as e:
                self.show_dialog(f"Erro ao salvar {os.path.basename(img_path)}: {str(e)}")

        self.show_dialog("Imagens salvas com sucesso!")

    def show_dialog(self, text):
        dialog = Popup(title='Informação', content=Label(text=text), size_hint=(0.5, 0.5))
        dialog.open()

if __name__ == '__main__':
    ImageManagerApp().run()
