import on_screen_overlay
import tkinter as tk


if __name__ == "__main__":
    window = tk.Tk()
    window.wait_visibility(window)
    window.wm_attributes("-alpha", 0.4)
    # app = FullScreen(window)
    app = on_screen_overlay.FullScreen(window)
    window.bind("<Escape>", lambda x: window.destroy())
    window.mainloop()

    while(true)