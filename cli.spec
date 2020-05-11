# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

 
import platform
import sys
sys.path.insert(0,'')
from luck.header import __version__

def get_exe_name(target,src):
  san = lambda x:x.replace('_','-').replace('.','-')
  exe_name = '_'.join([
    san(target),
    san(__version__),
    san(platform.platform())
    ])
  return exe_name


for target, src in [
  ('luck',      'luck/cli.py',), 
  ('luckmake',    'luck/luck_build_main.py')]:
  exe_name = get_exe_name(target,src)
  a = Analysis([src],
               pathex=['/data/local/repos/luck'],
               binaries=[],
               datas=[],
               hiddenimports=[
                'luck.cli',
                'luck.types',
                'luck.shorts',
                'luck.header',
                'luck.defer',
                'luck.pattern',
                'luck.rule_stamp',
                'future_fstrings',
                ],
               hookspath=[],
               runtime_hooks=[],
               excludes=[],
               win_no_prefer_redirects=False,
               win_private_assemblies=False,
               cipher=block_cipher,
               noarchive=False,
               )
  pyz = PYZ(a.pure, a.zipped_data,
               cipher=block_cipher)

  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            [],
            name=exe_name,
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=True )

  from path import Path
  if platform.system().lower() in ['linux']:
    d = Path(exe.name).dirname()
    #Path(exe.name).basename().symlink(Path(d/target).unlink_p())
    Path(exe.name).link(Path(d/target).unlink_p())
    print('[exe]%s'%exe.name)


