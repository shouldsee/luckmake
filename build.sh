# export PYTHONOPTIMIZE=10
# python3.7 `which pyinstaller` cli.spec --distpath ./bin
python3.7 -m PyInstaller cli.spec --distpath ./bin $@ 
#pyinstaller cli.spec --distpath ./bin --clean $@
