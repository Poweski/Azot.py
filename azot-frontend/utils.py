def adjust_window(window_width, window_height, app):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    return f'{window_width}x{window_height}+{x}+{y}'
