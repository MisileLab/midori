import click
from requests import get
from os.path import isfile
from os import remove
from subprocess import run
from xmltodict import parse

@click.command("lol")
@click.option('--modloader', type=str, default=None, help="forge/fabric/quilt support, default is Vanila")
@click.option('--version', type=str, help="minecraft version")
@click.option('--path', type=str, help="minecraft path")
@click.option('--run', type=bool, help="run minecraft or not?, default is False", default=False)
@click.option('--ram', type=int, help="set java --Xms and --Xmx, default is 4GB", default="4")
@click.option('--client', type=bool, help="minecraft client or server, default is True (client)", default=True)
def main(modloader: str | None, version: str, path: str, run: bool, ram: int, client: bool):
    Downloader(modloader, version, path, run, ram, client).install()

def shell_run(command: str):
    run(command, shell=True)

class Downloader:
    def __init__(self, modloader: str | None, version: str, path: str, run: bool, ram: int, client: bool):
        if modloader is None:
            self.modloader = None
        else:
            self.modloader = modloader.lower() # type: ignore
        self.version = version
        self.path = path
        self.run = run
        self.ram = ram
        self.client = client

    def install(self):
        self.install_minecraft_library()
        if self.modloader == "forge":
            self.install_forge()
        elif self.modloader == "fabric":
            self.install_fabric()
        elif self.modloader == "quilt":
            self.install_quilt()

    def install_minecraft_library(self):
        raise NotImplementedError

    def run_minecraft(self):
        raise NotImplementedError

    def install_fabric(self):
        lversion = parse(get("https://maven.fabricmc.net/net/fabricmc/fabric-installer/maven-metadata.xml").content)["metadata"]["versioning"]["latest"]
        with get(f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{lversion}/fabric-installer-{lversion}.jar") as a: # type: ignore
            if isfile("fabric-installer.jar"):
                remove("fabric-installer.jar")
            with open("fabric-installer.jar", "wb") as f:
                f.write(a.content)
        if self.client is True:
            cstring = "client -noprofile"
        else:
            cstring = "server"
        shell_run(f"java -jar fabric-installer.jar {cstring} -mcversion {self.version} -path {self.path} -noprofile")

    def install_forge(self):
        options = {}
        for i, i2 in get("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json").json()["promos"].items():
            if i.endswith("latest"):
                options[i.removesuffix("-latest")] = i2
        with get(f"https://maven.minecraftforge.net/net/minecraftforge/forge/{self.version}-{options[self.version]}/forge-{self.version}-{options[self.version]}-installer.jar") as a: # type: ignore
            print(f"{a.url}: {a.status_code}")
            if isfile("forge-installer.jar"):
                remove("forge-installer.jar")
            with open("forge-installer.jar", "wb") as f:
                f.write(a.content)
        if self.client:
            shell_run("java -jar forge-installer.jar")
        else:
            shell_run("java -jar forge-installer.jar --installServer")

    def install_quilt(self):
        raise NotImplementedError

if __name__ == "__main__":
    main()
