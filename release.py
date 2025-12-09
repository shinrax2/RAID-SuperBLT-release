# imports
import shutil
import os
import sys

# dirs
dll = "RAID-SuperBLT"
base = "RAID-SuperBLT-Lua"
tmp = "tmp/"
root = os.getcwd()

# urls
dll_repo = "https://github.com/RAIDModding/RAID-SuperBLT"
base_repo = "https://github.com/RAIDModding/RAID-SuperBLT-Lua"

# check requirements
git = shutil.which("git") is not None
vc_vars_x64 = True if os.environ["VSCMD_ARG_TGT_ARCH"] == "x64" and os.environ["VSCMD_ARG_HOST_ARCH"] == "x64" else False

if git == False:
    print("this script requires 'git' to be on PATH")
    sys.exit(1)

if vc_vars_x64 == False:
    print("this script requires to be run under 'x64 Native Tools Command Prompt'")
    sys.exit(1)

# clean up/prep

if os.path.exists(dll):
    shutil.rmtree(dll)

if os.path.exists(base):
    shutil.rmtree(base)

if os.path.exists(tmp):
    shutil.rmtree(tmp)
else:
    os.mkdir(tmp)

# clone

os.system(f"git clone --recursive {dll_repo} {dll}")
os.system(f"git clone {base_repo} {base}")

# build dll & updater
os.chdir(dll)
os.mkdir("build")
os.chdir("build")
os.system("cmake -S .. -A x64 -G \"Visual Studio 17 2022\" -DCMAKE_BUILD_TYPE=Release") # configure
os.system("msbuild SuperBLT.sln /t:Build /p:Configuration=Release") # build
os.chdir(root)
shutil.copy2(os.path.join(dll, "build/Release/IPHLPAPI.dll"), tmp)
shutil.copy2(os.path.join(dll, "build/Release/WSOCK32.dll"), tmp)
shutil.copy2(os.path.join(dll, "build/Release/SBLT_DLL_UPDATER.exe"), tmp)

# prepare base
os.mkdir("tmp/base")
shutil.copytree(os.path.join(base, "assets"), "tmp/base/assets")
shutil.copytree(os.path.join(base, "loc"), "tmp/base/loc")
shutil.copytree(os.path.join(base, "lua"), "tmp/base/lua")
shutil.copytree(os.path.join(base, "req"), "tmp/base/req")
shutil.copytree(os.path.join(base, "wren"), "tmp/base/wren")
shutil.copy2(os.path.join(base, "base.lua"), "tmp/base/")
shutil.copy2(os.path.join(base, "blt.png"), "tmp/base/")
shutil.copy2(os.path.join(base, "CHANGELOG.md"), "tmp/base/")
shutil.copy2(os.path.join(base, "LICENSE.md"), "tmp/base/")
shutil.copy2(os.path.join(base, "supermod.xml"), "tmp/base/")

# build zips

# release wsock32
os.mkdir("tmp/wsock32_rel")
os.mkdir("tmp/wsock32_rel/mods")
os.mkdir("tmp/wsock32_rel/updater")
shutil.copytree("tmp/base", "tmp/wsock32_rel/mods/base")
shutil.copy2("tmp/WSOCK32.dll", "tmp/wsock32_rel/")
shutil.copy2("tmp/SBLT_DLL_UPDATER.exe", "tmp/wsock32_rel/updater")
shutil.make_archive("RAID-SuperBLT_WSOCK32", "zip", root_dir="tmp/wsock32_rel")

# release iphlpapi

os.mkdir("tmp/iphlpapi_rel")
os.mkdir("tmp/iphlpapi_rel/mods")
os.mkdir("tmp/iphlpapi_rel/updater")
shutil.copytree("tmp/base", "tmp/iphlpapi_rel/mods/base")
shutil.copy2("tmp/IPHLPAPI.dll", "tmp/iphlpapi_rel/")
shutil.copy2("tmp/SBLT_DLL_UPDATER.exe", "tmp/iphlpapi_rel/updater")
shutil.make_archive("RAID-SuperBLT_IPHLPAPI", "zip", root_dir="tmp/iphlpapi_rel")

# autoupdate base
os.mkdir("tmp/auto_base")
shutil.copytree("tmp/base", "tmp/auto_base")
shutil.make_archive("AutoUpdate_base", "zip", root_dir="tmp/auto_base")

# autoupdate wsock32
os.mkdir("tmp/auto_wsock32")
shutil.copy2("tmp/WSOCK32.dll", "tmp/auto_wsock32/")
shutil.make_archive("AutoUpdate_wsock32", "zip", root_dir="tmp/auto_wsock32")

# autoupdate iphlpapi
os.mkdir("tmp/auto_iphlpapi")
shutil.copy2("tmp/IPHLPAPI.dll", "tmp/auto_iphlpapi/")
shutil.make_archive("AutoUpdate_iphlpapi", "zip", root_dir="tmp/auto_iphlpapi")

# autoupdate updater
os.mkdir("tmp/auto_updater")
shutil.copy2("tmp/SBLT_DLL_UPDATER.dll", "tmp/auto_updater/")
shutil.make_archive("AutoUpdate_updater", "zip", root_dir="tmp/auto_updater")
