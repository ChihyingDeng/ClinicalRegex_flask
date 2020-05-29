# -*- mode: python ; coding: utf-8 -*-
# work-around a bug in hook-botocore
from PyInstaller.utils.hooks import is_module_satisfies
import PyInstaller.compat
PyInstaller.compat.is_module_satisfies = is_module_satisfies
block_cipher = None
datas=[('ClinicalRegex\\ClinicalRegex\\', 'ClinicalRegex\\'), ('input', 'input'), ('output', 'output'), ('C:\Python37\Lib\site-packages\spacy\data','.'),('C:\Python37\Lib\site-packages\spacy\data\en_core_web_sm','spacy\data\en_core_web_sm'),('C:\Python37\Lib\site-packages\en_core_web_sm','en_core_web_sm'),('C:\Python37\Lib\site-packages\spacy\data\en_core_web_sm\en_core_web_sm-2.2.5','spacy\data\en_core_web_sm\en_core_web_sm-2.2.5')]

a = Analysis(['app.py'],
             pathex=['C:\\Users\\User\\Desktop\\Dana Farber Projects\\Phase 1\\Chih-Ying Request - DONT FORGET TO PULL NEW BRANCH\\W64 Spacy\\ClinicalRegex_flask'],
             binaries=[],
             datas=datas,
             hiddenimports=[
                 'spacy.kb',
    'spacy.lexeme',
    'spacy.matcher._schemas',
    'spacy.morphology',
    'spacy.parts_of_speech',
    'spacy.syntax._beam_utils',
    'spacy.syntax._parser_model',
    'spacy.syntax.arc_eager',
    'spacy.syntax.ner',
    'spacy.syntax.nn_parser',
    'spacy.syntax.stateclass',
    'spacy.syntax.transition_system',
    'spacy.tokens._retokenize',
    'spacy.tokens.morphanalysis',
    'spacy.tokens.underscore',

    'blis',
    'blis.py',

    'cymem',
    'cymem.cymem',

    'murmurhash',

    'preshed.maps',

    'srsly.msgpack.util',

    'thinc.extra.search',
    'thinc.linalg',
    'thinc.neural._aligned_alloc',
    'thinc.neural._custom_kernels',
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
