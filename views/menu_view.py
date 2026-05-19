class MenuRenderer:
    def __init__(self):
        pass

    def renderMenu(self, menu):
        options: list[str] = menu.options
        hovering: int = menu.hovering
        header: bool = menu.header

        if header:
            for _ in range(2):
                print()
            for row in menu.getHeader():
                print(row.rjust( 10 + len(row)))

        for i, option in enumerate(options):
            option = '►' + option if i == hovering else ' ' + option 
            print(option.rjust(35 + len(option)))
