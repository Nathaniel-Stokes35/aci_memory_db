from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os
import subprocess

Window.clearcolor = (0, 0, 0, 1)  # Set background color to Black
Window.size = (1000, 1300)  # Set window size

class TagSearch(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        self.label = Label(text="Search for ACI Tags by defining the ACI impression of the event.", font_size=24, size_hint_y=None, height=50)
        self.add_widget(self.label)
        self.label2 = Label(text="Use the sliders and switches to specify the ACI impression of the event.", font_size=18, size_hint_y=None, height=30)
        self.add_widget(self.label2)
        self.label3 = Label(text="MBTI Type:", font_size=18, size_hint_y=None, height=30)
        self.add_widget(self.label3)
        self.mbtiOpenLabel = Label(text="How does the AI...")
        self.add_widget(self.mbtiOpenLabel)
        self.e_iLabel = Label(text="Recharge Socially?")
        self.add_widget(self.e_iLabel)
        self.mbtiswitch = MBTISwitch(trait_name="E versus I", options=["With Friends", "Alone"])
        self.add_widget(self.mbtiswitch)
        self.n_fLabel = Label(text="Make Decisions?")
        self.add_widget(self.n_fLabel)
        self.mbtiswitch2 = MBTISwitch(trait_name="S versus N", options=["Logic", "Feelings"])
        self.add_widget(self.mbtiswitch2)
        self.s_tLabel = Label(text="Focus on Details?")
        self.add_widget(self.s_tLabel)
        self.mbtiswitch3 = MBTISwitch(trait_name="F versus T", options=["Big Picture", "Details"])
        self.add_widget(self.mbtiswitch3)
        self.j_pLabel = Label(text="Prefer Structure?")
        self.add_widget(self.j_pLabel)
        self.mbtiswitch4 = MBTISwitch(trait_name="P versus J", options=["Spontaneous", "Structured"])
        self.add_widget(self.mbtiswitch4)

        self.oceanLabel = Label(text="OCEAN Traits:", font_size=18, size_hint_y=None, height=30)
        self.add_widget(self.oceanLabel)
        self.oceanOpenLabel = Label(text="Where does the AI land on the scale of...", font_size=20, size_hint_y=None, height=30)
        self.add_widget(self.oceanOpenLabel)
        self.oceanOLabel = Label(text="Methodical versus Curious?")
        self.add_widget(self.oceanOLabel)
        self.oceanSliderO = OCEANslider(trait_name="Openness")
        self.add_widget(self.oceanSliderO)
        self.oceanCLabel = Label(text="Free Spirited versus Self-Control?")
        self.add_widget(self.oceanCLabel)
        self.oceanSliderC = OCEANslider(trait_name="Conscientiousness")
        self.add_widget(self.oceanSliderC)
        self.oceanELabel = Label(text="Passive versus Outgoing?")
        self.add_widget(self.oceanELabel)
        self.oceanSliderE = OCEANslider(trait_name="Extraversion")
        self.add_widget(self.oceanSliderE)
        self.oceanALabel = Label(text="Uncompromising versus Accommodating?")
        self.add_widget(self.oceanALabel)
        self.oceanSliderA = OCEANslider(trait_name="Agreeableness")
        self.add_widget(self.oceanSliderA)
        self.oceanNLabel = Label(text="Easy Going versus Easily Stressed?")
        self.add_widget(self.oceanNLabel)
        self.oceanSliderN = OCEANslider(trait_name="Neuroticism")
        self.add_widget(self.oceanSliderN)

        self.perceptionLabel = Label(text="Perception of the Event:", font_size=18, size_hint_y=None, height=30)
        self.add_widget(self.perceptionLabel)
        self.perceptionOpenLabel = Label(text="How does the AI perceive the desired tag?", font_size=20, size_hint_y=None, height=30)
        self.add_widget(self.perceptionOpenLabel)
        self.perceptionSliderCaution = PerceptionSlider(trait_name="Caution/Danger")
        self.add_widget(self.perceptionSliderCaution)
        self.perceptionSliderCuriosity = PerceptionSlider(trait_name="Curiosity/Interest")
        self.add_widget(self.perceptionSliderCuriosity)
        self.perceptionSliderEmpathy = PerceptionSlider(trait_name="Empathy/Indifference")
        self.add_widget(self.perceptionSliderEmpathy)

        # --- Search Tag Button ---
        self.searchButton = Button(
            text="Search Tag",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        self.searchButton.bind(on_press=self.search_tag)

        self.add_widget(self.searchButton)

        self.clearButton = Button(
            text="Clear Old Tags",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        self.clearButton.bind(on_press=lambda instance: self.clear_old_tags(self.get_mbti(), self.get_trait()[0]))
        self.add_widget(self.clearButton)

        # --- SQL Toggle Section ---
        self.sqlToggleLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        self.sqlLabel = Label(text="Show SQL Queries", size_hint_x=0.7)
        self.sqlSwitch = Switch(active=False)
        self.sqlSwitch.bind(active=self.toggle_sql_display)

        self.sqlToggleLayout.add_widget(self.sqlLabel)
        self.sqlToggleLayout.add_widget(self.sqlSwitch)

        self.add_widget(self.sqlToggleLayout)

        # --- SQL Display (hidden by default) ---
        self.sqlScroll = ScrollView(size_hint=(1, None), height=200)
        self.sqlOutput = Label(
            text="",
            size_hint_y=None,
            halign='left',
            valign='top'
        )

        self.sqlOutput.bind(texture_size=self.update_sql_height)

        self.sqlScroll.add_widget(self.sqlOutput)
        self.add_widget(self.sqlScroll)

        self.sqlScroll.opacity = 0  # hidden initially

        # --- Result Display ---
        self.resultLabel = Label(
            text="Returned Tag: None",
            font_size=18,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.resultLabel)

    def toggle_sql_display(self, instance, value):
        if value:
            self.sqlScroll.opacity = 1
            self.update_sql_query()
        else:
            self.sqlScroll.opacity = 0

    def clear_old_tags(self, mbti, trait_letter):
        """
            Clears existing tags in personality_tags based on MBTI and trait.
            If MBTI exists, drop only the specified trait.
            If MBTI does not exist, clear the entire table.
        """
        profile_prefix = f"{mbti}_"
        
        # Check existing MBTIs in table
        existing_mbti = self.db.execute_query(
            "SELECT DISTINCT profile_id FROM personality_tags WHERE profile_id LIKE ?",
            (f"{profile_prefix}%",)
        )

        if existing_mbti:
            # MBTI exists → remove only the specific trait
            trait_map = {"O": "Openness", "C": "Conscientiousness",
                        "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"}
            trait_name = trait_map.get(trait_letter, trait_letter)
            print(f"Clearing existing {mbti} {trait_name} tags...")
            self.db.execute_query(
                "DELETE FROM personality_tags WHERE profile_id = ?",
                (f"{mbti}_{trait_name}",)
            )
            self.db.connection.commit()
        else:
            # MBTI does not exist → clear entire table
            print(f"MBTI {mbti} not found, clearing entire personality_tags table...")
            self.db.execute_query("DELETE FROM personality_tags")
            self.db.connection.commit()

    def search_tag(self, instance):
        db_path = "aci_memory.db"
        db_exists = os.path.exists(db_path)

        self.db = SQLiteDatabase(db_path)
        self.db.connect()

        print("MBTI: {}".format(self.get_mbti()))
        print("Trait: {}".format(self.get_trait()))

        subprocess.run([
            "python",
            "create_aci.py",
            self.get_mbti(),
            self.get_trait()[0]  # Pass first letter of trait for create_aci
        ], check=True)

        try: # Check if the personality_tags table is empty
            result = self.db.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='personality_tags';"
            )

            if not result:
                raise Exception("Table missing")

        except:
            print("Initializing database schema + data...")

            subprocess.run([
                "python",
                "create_aci.py",
                self.get_mbti(),
                self.get_trait()[0]  # Pass first letter of trait for create_aci
            ], check=True)
        
        caution = int(self.perceptionSliderCaution.slider.value)
        curiosity = int(self.perceptionSliderCuriosity.slider.value)
        empathy = int(self.perceptionSliderEmpathy.slider.value)

        profile_id = f"{self.get_mbti()}_{self.get_trait()}"

        # --- SQL Display ---
        query_display = f"""
                -- Active Profile:
                -- {profile_id}

                SELECT value
                FROM personality_tags
                WHERE profile_id = '{profile_id}'
                AND caution = {caution}
                AND curiosity = {curiosity}
                AND empathy = {empathy}
                LIMIT 1;
                """
        self.sqlOutput.text = query_display

        # --- Execute Query ---
        try:
            query = """
                SELECT value
                FROM personality_tags
                WHERE profile_id = ?
                AND caution = ?
                AND curiosity = ?
                AND empathy = ?
                LIMIT 1;
                """

            result = self.db.execute_query(
                query,
                (profile_id, caution, curiosity, empathy)
            )

            if result:
                tag = result[0][0]
                self.resultLabel.text = f"Returned Tag: {tag}"
                self.resultLabel.color = (0, 1, 0, 1)
            else:
                self.resultLabel.text = "Returned Tag: No match found"
                self.resultLabel.color = (1, 0, 0, 1)

        except Exception as e:
            self.resultLabel.text = f"Error: {str(e)}"
            self.resultLabel.color = (1, 0, 0, 1)

    def update_sql_height(self, instance, size):
        instance.height = size[1]
        instance.text_size = (self.sqlScroll.width, None)

    def get_mbti(self):
        e_i = "E" if self.mbtiswitch.switch.active else "I"
        s_n = "S" if self.mbtiswitch2.switch.active else "N"
        f_t = "F" if self.mbtiswitch3.switch.active else "T"
        j_p = "J" if self.mbtiswitch4.switch.active else "P"
        return f"{e_i}{s_n}{f_t}{j_p}"
    
    def get_trait(self):
        traits = {
            "Openness": int(self.oceanSliderO.slider.value),
            "Conscientiousness": int(self.oceanSliderC.slider.value),
            "Extraversion": int(self.oceanSliderE.slider.value),
            "Agreeableness": int(self.oceanSliderA.slider.value),
            "Neuroticism": int(self.oceanSliderN.slider.value)
        }
        return max(traits, key=traits.get)

    def update_sql_query(self):
        caution = int(self.perceptionSliderCaution.slider.value)
        curiosity = int(self.perceptionSliderCuriosity.slider.value)
        empathy = int(self.perceptionSliderEmpathy.slider.value)

        profile_id = f"{self.get_mbti()}_{self.get_trait()}"  # Use first letter of trait for display

        # Convert trait letter to full name (like in create_aci_db)
        trait_letter_map = {
            "O": "Openness",
            "C": "Conscientiousness",
            "E": "Extraversion",
            "A": "Agreeableness",
            "N": "Neuroticism"
        }

        full_trait = trait_letter_map[self.get_trait()[0]]
        profile_id = f"{self.get_mbti()}_{full_trait}"

        # --- REAL QUERY EXECUTION ---
        try:
            query = """
                SELECT value
                FROM personality_tags
                WHERE profile_id = ?
                AND caution = ?
                AND curiosity = ?
                AND empathy = ?
                LIMIT 1;
                """

            result = self.db.execute_query(
                query,
                (profile_id, caution, curiosity, empathy)
            )

            if result:
                tag = result[0][0]
            else:
                tag = "No match found"

            self.resultLabel.text = f"Returned Tag: {tag}"

            if hasattr(self, 'db') and self.db:
                self.db.clear_log()  # Clear previous logs before executing new query
                self.sqlOutput.text = self.db.get_query_log()

        except Exception as e:
            self.resultLabel.text = f"Error: {str(e)}"


class MBTISwitch(BoxLayout):
    def __init__(self, trait_name, options, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.trait_name = trait_name
        self.options = options

        self.trait_label = Label(
            text=trait_name,
            size_hint_x=None,
            width=120,
            halign='left',
            valign='middle'
        )
        self.trait_label.bind(size=self.trait_label.setter('text_size'))

        self.value_label = Label(
            text=options[0],
            size_hint_x=0.4
        )

        self.switch = Switch(size_hint=(None, None), size=(100, 50))
        self.switch.bind(active=self.on_switch_toggle)
        
        self.add_widget(self.trait_label)
        self.add_widget(self.value_label)
        self.add_widget(self.switch)
    
    def on_switch_toggle(self, instance, value):
        option_index = 1 if value else 0
        self.value_label.text = self.options[option_index]

class OCEANslider(BoxLayout):
    def __init__(self, trait_name, **kwargs):
        super().__init__(spacing=10,**kwargs)
        self.trait_name = trait_name

        # Outer container (full width, centers inner layout)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60

        # Inner layout (this is what gets centered)
        self.layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(400, 50),  # fixed width so centering works
            pos_hint={'center_x': 0.5}
        )

        self.label = Label(
            text=f"{trait_name}: 50",
            size_hint_x=None,
            width=150,
            halign='right',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint_x=1,
            step=1,
            width=250
        )

        self.slider.bind(value=self.on_value_change)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.slider)

        self.add_widget(self.layout)

    def on_value_change(self, instance, value):
        self.label.text = f"{self.trait_name}: {value:.0f}"

class PerceptionSlider(BoxLayout):
    def __init__(self, trait_name, **kwargs):
        super().__init__(**kwargs)
        self.trait_name = trait_name

        # Outer container (full width, centers inner layout)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60

        # Inner layout (this is what gets centered)
        self.layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(400, 50),  # fixed width so centering works
            pos_hint={'center_x': 0.5}
        )

        self.label = Label(
            text=f"{trait_name}: 50",
            size_hint_x=None,
            width=150,
            halign='right',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint_x=1,
            step=1,
            width=250
        )

        self.slider.bind(value=self.on_value_change)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.slider)

        self.add_widget(self.layout)

    def on_value_change(self, instance, value):
        self.label.text = f"{self.trait_name}: {value:.0f}"

class TagSearchApp(App):
    def build(self):
        root = ScrollView()
        layout = TagSearch(size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        root.add_widget(layout)
        return root
    
class SQLiteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.query_log = []

    def connect(self):
        import sqlite3
        self.connection = sqlite3.connect(self.db_name)

    def execute_query(self, query, params=None):
        if self.connection is None:
            raise Exception("Database not connected")
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
            logged_query = query
            for p in params:
                logged_query = logged_query.replace("?", repr(p), 1)
            self.query_log.append(logged_query)
        else:
            cursor.execute(query)
            self.query_log.append(query)
        return cursor.fetchall()

    def get_query_log(self):
        """Return all logged queries as a single string."""
        return "\n\n".join(self.query_log)

    def clear_log(self):
        self.query_log = []

    def close(self):
        if self.connection:
            self.connection.close()

if __name__ == '__main__':
    TagSearchApp().run()