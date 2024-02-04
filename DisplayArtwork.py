wallpaper_window = None
label = None

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
updateInterval = environ.get('artwork_inv')
fullscreen = environ.get('artwork_fs')
resolutionX = environ.get('artwork_resX')
resolutionY = environ.get('artwork_resY')

if (resolutionX is None or resolutionY is None or updateInterval is None):
    print("resolution vector does not configured yet. Please set resolution vector first!")
    print("Splash image reload interval was not configured!")
    print("supported environ values:")
    print("\tartwork_inv\tupdate splash image interval")
    print("\tartwork_fs\tmake fullscreen display artwork")
    print("\tartwork_resX\tsplash image X")
    print("\tartwork_resY\tsplash image Y")
    exit(1)

def downloadSplashSource():
    backgroundSource = f"https://unsplash.it/{resolutionX}/{resolutionY}/?random"
    print(f"Display artwork resolution vector: {resolutionX}x{resolutionY}")
    print(f"Display artwork target: {backgroundSource}")
    try:
        with urllib.request.urlopen(backgroundSource) as url_parse:
            return url_parse.read()
    except (HTTPError) as error:
        print("error: Background source could not download at this time.")
        print(f"respond status code: {error.code}")
        return None

def refreshSplashImage():
    newImage = ImageTk.PhotoImage(Image.open(io.BytesIO(downloadSplashSource())))
    label['image'] = newImage
    label.image = newImage
    wallpaper_window.after(updateInterval, refreshSplashImage)

wallpaper_window = Tk()
wallpaper_window.geometry("1024x768")
wallpaper_window.title("")

label = Label(wallpaper_window, text="")
label.place(relx=0.5, rely=0.5, anchor='center')

if (fullscreen is not None and fullscreen == "true"):
    wallpaper_window.attributes('-fullscreen', True)

refreshSplashImage()
wallpaper_window.mainloop()

