import html

def render_confirmation(name):
    return f"<h1>Thanks {html.escape(name)}</h1>"
