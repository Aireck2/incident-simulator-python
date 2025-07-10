def highlight(text: str, color: str = "yellow", bold: bool = False) -> str:
    colors = {
        "black": '30', "red": '31', "green": '32',
        "yellow": '33', "blue": '34', "magenta": '35',
        "cyan": '36', "white": '37'
    }
    color_code = colors.get(color.lower(), '33')
    bold_code = '1' if bold else '0'
    return f"\033[{bold_code};{color_code}m{text}\033[0m"
