import markdown
import os

DEFAULT_CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 850px;
    margin: 0 auto;
    padding: 20px;
}
h1, h2, h3, h4, h5, h6 { border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
code { background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace; }
pre { background-color: #f6f8fa; padding: 16px; overflow: auto; border-radius: 3px; }
pre code { background-color: transparent; padding: 0; }
blockquote { border-left: 0.25em solid #dfe2e5; color: #6a737d; padding: 0 1em; margin: 0; }
table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
table th, table td { border: 1px solid #dfe2e5; padding: 6px 13px; }
table tr:nth-child(2n) { background-color: #f6f8fa; }
"""

def mdcode(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=['extra', 'codehilite', 'tables'])

def mdfile(md_path: str, 
           out_path: str, 
           use_css: bool = False, 
           css_path: str = None, 
           inline_css: bool = False):
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Файл не найден: {md_path}")
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_body = mdcode(md_content)

    css_section = ""
    if use_css:
        if inline_css:
            css_content = DEFAULT_CSS
            if css_path and os.path.exists(css_path):
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
            elif css_path:
                print(f"Предупреждение: CSS файл '{css_path}' не найден. Использован базовый стиль.")
                
            css_section = f"<style>\n{css_content}\n</style>"
        else:
            link_href = css_path if css_path else "style.css"
            css_section = f'<link rel="stylesheet" href="{link_href}">'
            
            if not css_path and not os.path.exists("style.css"):
                with open("style.css", 'w', encoding='utf-8') as f:
                    f.write(DEFAULT_CSS)
                print("Создан файл style.css с базовыми стилями по умолчанию.")

    full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(md_path).replace('.md', '')}</title>
    {css_section}
</head>
<body>
{html_body}
</body>
</html>"""

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Файл успешно сконвертирован: {out_path}")