import shutil
import os


def main ():
    ftocopy = [
        "portal.py",
        "requirements.txt",
        "requirements.311.txt"
    ]

    rootpath = os.path.abspath('./')
    distdir = os.path.abspath('./dist')
    distpath = os.path.abspath('./dist/portal')
    osmpython = os.path.abspath('./reactapp/OpenStreetTouch')

    
    shutil.rmtree (os.path.join(distdir, ""), ignore_errors=True)
    os.makedirs (distpath, exist_ok=True)
    for fname in ftocopy:
        shutil.copyfile (os.path.join(rootpath, fname), os.path.join(distpath, fname))
    
    shutil.copytree (os.path.join(rootpath, "app"), os.path.join(distpath, "app"), 
                     ignore=shutil.ignore_patterns("*.pyc", "__pycache__" ))
    shutil.copytree (os.path.join(osmpython, "osm"), os.path.join(distpath, "reactapp/OpenStreetTouch/osm"), 
                         ignore=shutil.ignore_patterns("*.pyc", "__pycache__", "*.db" ))

if __name__ == "__main__":
    main()