from rich.console import Console
from rich.table import Table

table = Table(title="Bottle Capping/ De-Capping System Demo")
rows = [
    ["John", "Doe", "45"],
    ["Jane", "Doe", "32"],
    ["Mary", "Smith", "25"],
]
columns = ["Action", "Key", "Range"]

for column in columns:
    table.add_column(column)

for row in rows:
    table.add_row(*row, style='bright_green')

console = Console()
console.print(table)

#################
table = Table(title="Star Wars Movies")

table.add_column("Released", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()
#console.print(table, justify="center")
console.print(table)

####################
table = Table(title="Key Map for Bottle Capping/ De-Capping System Operation")

table.add_column("Tool/Function", style="cyan", no_wrap=True)
table.add_column("Key", style="magenta")
table.add_column("Action",justify="center", style="green")

table.add_row("Cylinder", "+", "Move down")
table.add_row("        ", "-", "Move up")
table.add_row()
table.add_row("Gripper", "z", "Full Close")
table.add_row("        ", "x", "Full Open")
table.add_row("        ", "c", "Open steps")
table.add_row("        ", "v", "Close steps")
table.add_row()
table.add_row("Rotary Gripper", "a", "Full Close")
table.add_row("        ", "s", "Full Open")
table.add_row("        ", "d", "Open steps")
table.add_row("        ", "f", "Close steps")
table.add_row("        ", "g", "Rotate CW")
table.add_row("        ", "h", "Rotate CCW")
table.add_row()
table.add_row("Set home position", "i", "Set to home position and calibrate")
table.add_row()
table.add_row("Run Capping/ De-Capping example", "e", "Automated capping and decapping ")
table.add_row("        ", " ", "based on user input parameters")

table1 = Table(title="Capping/ De-Capping example")

console = Console()
#console.print(table, justify="center")
console.print(table)