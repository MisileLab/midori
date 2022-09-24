from os import remove
from requests import get
from os.path import isfile

def main():
    with get("https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/latest/quilt-installer-latest.jar") as a: # type: ignore
        if isfile("quilt.jar"):
            remove("quilt.jar")
        with open("quilt.jar", "wb") as f:
            f.write(a.content)
    print("done")

if __name__ == "__main__":
    main()
