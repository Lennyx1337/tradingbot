import os
import urllib
from tkinterhtml import HtmlFrame
import tkinter as tk
import customtkinter
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

        # create dashboard frame
        self.dashboard_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)

        # create HtmlFrame for TradingView chart
        self.tradingview_frame = HtmlFrame(self.dashboard_frame, horizontal_scrollbar="auto")
        self.tradingview_frame.grid(row=0, column=0, sticky="nsew")

        # load TradingView chart widget HTML code
        tradingview_html = """
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container" style="height:100%;width:100%">
          <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
          <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
          {
          "autosize": true,
          "symbol": "NASDAQ:AAPL",
          "interval": "D",
          "timezone": "Etc/UTC",
          "theme": "dark",
          "style": "1",
          "locale": "en",
          "enable_publishing": false,
          "allow_symbol_change": true,
          "calendar": false,
          "support_host": "https://www.tradingview.com"
        }
          </script>
        </div>
        <!-- TradingView Widget END -->
        """
        self.tradingview_frame.set_content(tradingview_html)

        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")

        # show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid_forget()

    def dashboard_button_event(self):
        self.select_frame_by_name("dashboard")

if __name__ == "__main__":
    app = App()
    app.mainloop()
