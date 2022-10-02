import click
from requests import get
from os.path import isfile
from os import remove, getcwd, chdir
from subprocess import run
from xmltodict import parse

client_id = "1a92c271-496c-496d-b2ac-3bced4d11853"
redirect_url = "http://localhost"

@click.command("lol")
@click.option('--modloader', type=str, default=None, help="forge/fabric/quilt support, default is Vanila")
@click.option('--version', type=str, help="minecraft version")
@click.option('--ram', type=int, help="set java --Xms and --Xmx, default is 4GB", default="4")
@click.option('--client', type=bool, help="minecraft client or server, default is True (client)", default=True)
@click.option('--maindir', type=str, help="maindir of minecraft")
@click.option('--subdir', type=str, help="subdir of minecraft", default=None)
@click.option('--mversion', type=str, help="modloader version, defualt is latest", default=None)
def main(modloader: str | None, version: str, ram: int, client: bool, maindir: str, subdir: str | None, mversion: str | None):
    Downloader(modloader, version, ram, client, maindir, subdir, mversion).install()

def shell_run(command: str):
    run(command, shell=True)

class Downloader:
    def __init__(self, modloader: str | None, version: str, ram: int, client: bool, maindir: str, subdir: str | None, mversion: str | None):
        if modloader is None:
            self.modloader = None
        else:
            self.modloader = modloader.lower() # type: ignore
        self.version = { "mc": version, "modloader": mversion }
        self.ram = ram
        self.client = client
        self.dir = { "main": maindir, "data": subdir }

    def install(self):
        if self.client:
            if self.modloader is None:
                if self.dir["data"] is None:
                    shell_run(f"portablemc --main-dir={self.dir['main']} start self.version['mc'] --jvm-args='-Xmx{self.ram}G -Xms{self.ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M'")
                else:
                    shell_run(f"portablemc --main-dir={self.dir['main']} --work-dir={self.dir['data']} start self.version['mc'] --jvm-args='-Xmx{self.ram}G -Xms{self.ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M'")
            else:
                if self.version["modloader"] is None:
                    if self.dir["data"] is None:
                        shell_run(f"portablemc --main-dir={self.dir['main']} start {self.modloader}:{self.version['mc']} --jvm-args='-Xmx{self.ram}G -Xms{self.ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M'")
                    else:
                        shell_run(f"portablemc --main-dir={self.dir['main']} --work-dir={self.dir['data']} start {self.modloader}:{self.version['mc']} --jvm-args='-Xmx{self.ram}G -Xms{self.ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M'")
                else:
                    if self.dir["data"] is None:
                        shell_run(f"portablemc --main-dir={self.dir['main']} start {self.modloader}:{self.version['mc']}:{self.version['modloader']} --jvm-args='-Xmx{self.ram}G -Xms{self.ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M'")
                    else:
                        shell_run(f"portablemc --main-dir={self.dir['main']} --work-dir={self.dir['data']} start {self.modloader}:{self.version['mc']}:{self.version['modloader']} --jvm-args='-Xmx{self.ram}G -Xms{self.ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M'")

    def install_fabric(self):
        lversion = parse(get("https://maven.fabricmc.net/net/fabricmc/fabric-installer/maven-metadata.xml").content)["metadata"]["versioning"]["latest"]
        with get(f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{lversion}/fabric-installer-{lversion}.jar") as a: # type: ignore
            if isfile("fabric-installer.jar"):
                remove("fabric-installer.jar")
            with open("fabric-installer.jar", "wb") as f:
                f.write(a.content)
        if self.version['mc'] is None:
            shell_run(f"java -jar fabric-installer.jar -mcversion {self.version['mc']} -path {self.dir['main']} -noprofile -snapshot")
        else:
            shell_run(f"java -jar fabric-installer.jar -mcversion {self.version['mc']} -path {self.dir['main']} -noprofile -snapshot -loader {self.version['modloader']}")

    def install_forge(self):
        options = {}
        for i, i2 in get("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json").json()["promos"].items():
            if i.endswith("latest"):
                options[i.removesuffix("-latest")] = i2
        if self.version["modloader"] is not None:
            options[self.version["mc"]] = self.version["modloader"]
        with get(f"https://maven.minecraftforge.net/net/minecraftforge/forge/{self.version['mc']}-{options[self.version['modloader']]}/forge-{self.version['mc']}-{options[self.version['mc']]}-installer.jar") as a: # type: ignore
            if a.status_code == 404:
                print("can't find version")
                return
            if isfile("forge-installer.jar"):
                remove("forge-installer.jar")
            with open("forge-installer.jar", "wb") as f:
                f.write(a.content)
        orgd = getcwd()
        chdir(self.dir["main"])
        shell_run(f"java -jar forge-installer.jar --installServer")
        chdir(orgd)

    def install_quilt(self):
        with get("https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/latest/quilt-installer-latest.jar") as a: # type: ignore
            if a.status_code == 404:
                print("can't find version")
                return
            if isfile("quilt.jar"):
                remove("quilt.jar")
            with open("quilt.jar", "wb") as f:
                f.write(a.content)
        orgd = getcwd()
        chdir(self.dir["main"])
        shell_run("java -jar quilt.jar install server {self.version['mc']} --download-server")
        chdir(orgd)

if __name__ == "__main__":
    main()
