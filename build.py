from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
DIST.mkdir(exist_ok=True)
for name in ['index.html','styles.css','app.js','data.js','trip.json','offline-guide.html','iceland-guide.pdf','costs.csv']:
 shutil.copy2(ROOT/name,DIST/name)
shutil.copytree(ROOT/'assets',DIST/'assets',dirs_exist_ok=True)
print('Built static guide into',DIST)
