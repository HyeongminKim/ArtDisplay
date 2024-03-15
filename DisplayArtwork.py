wallpaper_window = None
viewer = None
status = None

try:
    import platform
    if platform.system() == 'Windows':
        raise OSError(f'{platform.system()} system does not support.')

    from os import environ
    from tkinter import Tk, Label, TclError
    from PIL import Image, ImageTk
    from urllib.error import HTTPError, URLError
    import urllib.request
    import io
except (ImportError, ModuleNotFoundError, OSError) as error:
    print(error)
    exit(1)

# usage: `export artwork_res=0` or write .bash_profile to configure artwork size
updateInterval = environ.get('artwork_inv') # unit: minutes
fullscreen = environ.get('artwork_fs')
resolutionX = environ.get('artwork_resX')
resolutionY = environ.get('artwork_resY')

if (resolutionX is None or resolutionY is None or updateInterval is None):
    print("resolution vector does not configured yet. Please set resolution vector first!")
    print("Splash image reload interval was not configured!")
    print("supported environ values:")
    print("\tartwork_inv\tupdate splash image every n minutes")
    print("\tartwork_fs\tmake fullscreen display artwork")
    print("\tartwork_resX\tsplash image X")
    print("\tartwork_resY\tsplash image Y")
    exit(1)
else:
    try:
        resolutionX = int(resolutionX)
        resolutionY = int(resolutionY)
        updateInterval = (int(updateInterval) * 1000)
    except (ValueError) as error:
        print(error)
        exit(1)

def downloadSplashSource():
    backgroundSource = f"https://unsplash.it/{resolutionX}/{resolutionY}/?random"
    print(f"Display artwork resolution vector: {resolutionX}x{resolutionY}")
    print(f"Display artwork target: {backgroundSource}")
    try:
        with urllib.request.urlopen(backgroundSource) as url_parse:
            status.place_forget()
            return url_parse.read()
    except (HTTPError) as error:
        print("error: Background source could not download at this time.")
        print(f"respond status code: {error.code}")
        status.place(relx=0.5, rely=0.5, anchor='center')
        status['text'] = f"{error}"
        return None
    except (URLError) as error:
        print(error)
        status.place(relx=0.5, rely=0.5, anchor='center')
        status['text'] = f"{error}"
        return None

def refreshSplashImage():
    cache = downloadSplashSource()
    if cache is None:
        print("error: unable to cast type None to Object")
        if updateInterval < 5000:
            print(f"refresh rate: 5 seconds.")
            wallpaper_window.after(5000, refreshSplashImage)
        else:
            print(f"refresh rate: {updateInterval / 1000} seconds.")
            wallpaper_window.after(updateInterval, refreshSplashImage)
        return

    newImage = ImageTk.PhotoImage(Image.open(io.BytesIO(cache)))
    viewer['image'] = newImage
    viewer.image = newImage
    print(f"refresh rate: {updateInterval * 60 / 1000} seconds.")
    wallpaper_window.after((updateInterval * 60), refreshSplashImage)

try:
    wallpaper_window = Tk()
    wallpaper_window.geometry("1024x768")
    wallpaper_window.title("")
    wallpaper_window.config(cursor="none")
except (TclError) as error:
    print(f'{error}. Please update $DISPLAY variable like ":0.0" and make sure get-default is graphical.target')
    exit(1)

viewer = Label(wallpaper_window, text="")
viewer.place(relx=0.5, rely=0.5, anchor='center')

status = Label(wallpaper_window, text="", foreground='#FF0000', background='#000000', font=('Helvetica', 18))

if (fullscreen is not None and fullscreen == "true"):
    wallpaper_window.attributes('-fullscreen', True)

refreshSplashImage()
wallpaper_window.mainloop()

