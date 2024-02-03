try:
    from os import environ
    from tkinter import Tk, Label
    from PIL import Image, ImageTk
    import urllib.request
    import io
except (ImportError, ModuleNotFoundError) as error:
    print(error)
    exit(1)

# usage: `export artwork_res=0` or write .bash_profile to configure artwork size
fullscreen = environ.get('artwork_fs')
resolutionX = environ.get('artwork_resX')
resolutionY = environ.get('artwork_resY')
if (resolutionX is None or resolutionY is None):
    print("resolution vector does not configured yet. Please set resolution vector first!")
    exit(1)

backgroundSource = f"https://unsplash.it/{resolutionX}/{resolutionY}/?random"
print(f"Display artwork resolution vector: {resolutionX}x{resolutionY}")
print(f"Display artwork target: {backgroundSource}")

try:
    with urllib.request.urlopen(backgroundSource) as url_parse:
        raw_data = url_parse.read()
except (HTTPError) as error:
    print("error: Background source could not download at this time.")
    print(f"respond status code: {error.code}")
    exit(1)

wallpaper_window = Tk()
wallpaper_window.geometry("1024x768")
wallpaper_window.title("")

imageViewer = ImageTk.PhotoImage(Image.open(io.BytesIO(raw_data)))
label = Label(wallpaper_window, image=imageViewer)
label.image = imageViewer
label.place(relx=0.5, rely=0.5, anchor='center')

if (fullscreen is not None and fullscreen == "true"):
    wallpaper_window.attributes('-fullscreen', True)

wallpaper_window.mainloop()

