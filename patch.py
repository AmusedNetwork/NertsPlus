import os
import shutil
import urllib.request
import zipfile
from pathlib import Path
import platform
import utils

system = platform.system()

BIN_PATH = Path("bin")

if not "SKIP_DOWNLOAD" in os.environ:
  try:
    if BIN_PATH.exists():
      shutil.rmtree(BIN_PATH)
  except:
    print("Unable to clear bin/ directory, aborting.")
    quit()

  BIN_PATH.mkdir()

  # Download de4dot
  urllib.request.urlretrieve("https://github.com/ViRb3/de4dot-cex/releases/download/v4.0.0/de4dot-cex.zip", BIN_PATH / "de4dot-cex.zip")

  # Extract de4dot
  with zipfile.ZipFile(BIN_PATH / "de4dot-cex.zip", "r") as zip:
    zip.extractall("bin/")

nertsPath = utils.get_nerts_path()
cleanedName = f"{nertsPath.stem}-cleaned.exe"
actualName = "NertsOnline-cleaned.exe"

# Run de4dot to deobfuscate executable
utils.run_exe(BIN_PATH / "de4dot-x64.exe", "\"" + str(nertsPath) + "\"")
shutil.copyfile(nertsPath.parent / cleanedName, Path("bin") / actualName)

# Build and run patcher
os.chdir("Patcher")
os.system("dotnet build")
utils.run_exe(BIN_PATH / "Debug/net452/NertsPlusPatcher.exe")
shutil.copyfile(BIN_PATH / "Debug/net452/NertsPlusPatcher.exe", os.path.dirname(nertsPath) + "/NertsPlusPatcher.exe")
os.chdir("..")

# Copy patcher output back to Steam directory
shutil.copyfile(BIN_PATH / "NertsOnline-patched.exe", os.path.dirname(nertsPath) + "/NertsOnline-patched.exe")

# Build and copy plugin
os.chdir("Plugin")
os.system("dotnet build")
shutil.copyfile(BIN_PATH / "Debug/net452/NertsPlus.dll", os.path.dirname(nertsPath) + "/NertsPlus.dll")
shutil.copyfile(BIN_PATH / "Debug/net452/0Harmony.dll", os.path.dirname(nertsPath) + "/0Harmony.dll")
shutil.copyfile(BIN_PATH / "Debug/net452/Newtonsoft.Json.dll", os.path.dirname(nertsPath) + "/Newtonsoft.Json.dll")
os.chdir("..")

# Write steam_appid.txt file
with open(os.path.dirname(nertsPath) + "/steam_appid.txt", "w") as file:
  file.write("1131190")

# Finally, copy textures...
shutil.copyfile("textures/logo_button.tex", os.path.dirname(nertsPath) + "/Content/Packed/logo_button.tex")
shutil.copyfile("textures/logo_button_hover.tex", os.path.dirname(nertsPath) + "/Content/Packed/logo_button_hover.tex")

print("🎉 All done! To finish, drop NertsPlus.dll in to " + os.path.dirname(nertsPath) + ", and then execute run.py")
