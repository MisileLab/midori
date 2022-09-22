import click

@click.command("lol")
@click.option('--modloader', type=str, default=None, help="forge/fabric/quilt support")
@click.option('--version', type=str, help="minecraft version")
@click.option('--path', type=str, help="minecraft path")
def main(modloader: str | None, version: str, path: str):
    if modloader == "forge":
        install_forge()
    elif modloader == "fabric":
        install_fabric()

def install_fabric():
    pass

def install_forge():
    pass

if __name__ == "__main__":
    main()
