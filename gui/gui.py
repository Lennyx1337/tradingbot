import customtkinter
import os
from tkinterhtml import HtmlFrame
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("lemrokTradingBot.py")
        self.geometry("960x610")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.dashboard_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "dashboard_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "custom.png")), size=(20, 20))
        self.profile_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "profile_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" TradingBot", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dashboard",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.dashboard_image, anchor="w", command=self.dashboard_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.predefined_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Predefined",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.predefined_button_event)
        self.predefined_button.grid(row=2, column=0, sticky="ew")

        self.custom_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Custom",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.custom_button_event)
        self.custom_button.grid(row=3, column=0, sticky="ew")

        self.profile_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Profile",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.profile_image, anchor="w", command=self.profile_button_event)
        self.profile_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create dashboard frame
        self.dashboard_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)

        # self.tradingview_frame = HtmlFrame(self.dashboard_frame, horizontal_scrollbar="auto")
        # self.tradingview_frame.grid(row=0, column=0, sticky="nsew")

        # # load TradingView chart widget HTML code
        # self.tradingview_html = """
        # <div class="tradingview-widget-container" style="height:100%;width:100%">
        #   <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
        #   <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
        #   <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        #   {
        #   "autosize": true,
        #   "symbol": "NASDAQ:AAPL",
        #   "interval": "D",
        #   "timezone": "Etc/UTC",
        #   "theme": "dark",
        #   "style": "1",
        #   "locale": "en",
        #   "enable_publishing": false,
        #   "allow_symbol_change": true,
        #   "calendar": false,
        #   "support_host": "https://www.tradingview.com"
        # }
        #   </script>
        # </div>
        # """
        # self.tradingview_frame.set_content(self.tradingview_html)

        # self.dashboard_frame_large_image_label = customtkinter.CTkLabel(self.dashboard_frame, text="", image=self.large_test_image)
        # self.dashboard_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # self.dashboard_frame_button_1 = customtkinter.CTkButton(self.dashboard_frame, text="", image=self.image_icon_image)
        # self.dashboard_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.dashboard_frame_button_2 = customtkinter.CTkButton(self.dashboard_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        # self.dashboard_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.dashboard_frame_button_3 = customtkinter.CTkButton(self.dashboard_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        # self.dashboard_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.dashboard_frame_button_4 = customtkinter.CTkButton(self.dashboard_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        # self.dashboard_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.profile_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.predefined_button.configure(fg_color=("gray75", "gray25") if name == "predefined" else "transparent")
        self.custom_button.configure(fg_color=("gray75", "gray25") if name == "custom" else "transparent")
        self.profile_button.configure(fg_color=("gray75", "gray25") if name == "profile" else "transparent")


        # show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid_forget()
        if name == "predefined":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "custom":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "profile":
            self.profile_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.profile_frame.grid_forget()

    def dashboard_button_event(self):
        self.select_frame_by_name("dashboard")

    def predefined_button_event(self):
        self.select_frame_by_name("predefined")

    def custom_button_event(self):
        self.select_frame_by_name("custom")
    
    def profile_button_event(self):
        self.select_frame_by_name("profile")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()