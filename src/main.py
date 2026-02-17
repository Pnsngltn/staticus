import os
import shutil

from getcontent import generate_page


def recursive_copy(source, destination):
    # Delete all files in destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)

    print(f"Creating directory: {destination}")
    os.mkdir(destination)

    # List contents of source directory
    contents = os.listdir(source)

    for item in contents:
        orgn = os.path.join(source, item)
        dest = os.path.join(destination, item)
        if os.path.isfile(orgn):
            print(f"Copying file: {orgn} to {dest}")
            shutil.copy(orgn, dest)
        else:
            recursive_copy(orgn, dest)


def main():
    recursive_copy("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
