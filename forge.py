from os import remove
from requests import get
from simple_term_menu import TerminalMenu
from os.path import isfile

def main():
    options = {}
    for i, i2 in get("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json").json()["promos"].items():
        if i.endswith("latest"):
            options[i.removesuffix("-latest")] = i2
    terminal_menu = TerminalMenu(options)
    terminal_menu.show()
    menu_entry = terminal_menu.chosen_menu_entry
    with get(f"https://maven.minecraftforge.net/net/minecraftforge/forge/{menu_entry}-{options[menu_entry]}/forge-{menu_entry}-{options[menu_entry]}-installer.jar") as a: # type: ignore
        print(a.url)
        print(a.status_code)
        if isfile("forge.jar"):
            remove("forge.jar")
        with open("forge.jar", "wb") as f:
            f.write(a.content)
    print("done")

if __name__ == "__main__":
    main()
