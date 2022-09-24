from os import remove
from requests import get
from os.path import isfile
from xmltodict import parse

def main():
    lversion = parse(get("https://maven.fabricmc.net/net/fabricmc/fabric-installer/maven-metadata.xml").content)["metadata"]["versioning"]["latest"]
    if input("server.jar? (y/n)") == "n":
        server = ""
    else:
        server = "-server"
    with get(f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{lversion}/fabric-installer-{lversion}{server}.jar") as a: # type: ignore
        if isfile("fabric.jar"):
            remove("fabric.jar")
        with open("fabric.jar", "wb") as f:
            f.write(a.content)
    print("done")

if __name__ == "__main__":
    main()
