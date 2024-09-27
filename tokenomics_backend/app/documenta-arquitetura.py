import os
import yaml

# 🎨 Usando emojis para representar tipos de arquivos
file_icons = {
    ".py": "🐍",
    ".yaml": "⚙️",
    ".yml": "⚙️",
    ".json": "🗃️",
    ".txt": "📄",
    ".md": "📝",
    ".html": "🌐",
    ".css": "🎨",
    ".js": "⚛️",
    ".jpg": "🖼️",
    ".jpeg": "🖼️",
    ".png": "🖼️",
    ".gif": "🖼️",
    ".svg": "🖼️",
    ".mp3": "🎵",
    ".mp4": "🎬",
    ".zip": "📦",
    ".rar": "📦",
    ".pdf": "📄",
    ".docx": "📄",
    ".xlsx": "📊",
    ".pptx": "📽️",
    ".db": "💾",
    ".sql": "💾",
    ".env": "🔐",
    ".gitignore": "🙈",
    ".dockerignore": "🐳",
    ".git": "🐙",
    ".idea": "🐘",
    ".vscode": "🆚",
    ".DS_Store": "🍎",
    ".gradle": "🐘",
    ".iml": "🐘",
    ".lock": "🔒",
    ".log": "📝",
    ".tmp": "⏳",
    ".cache": "📦",
    ".ini": "⚙️",
    ".cfg": "⚙️",
    ".conf": "⚙️",
    ".properties": "⚙️",
    ".sh": "🐚",
    ".bat": "🪟",
    ".exe": "🪟",
    ".dll": "🪟",
    ".so": "🐧",
    ".dylib": "🍎",
}

def get_file_icon(filename):
    """Retorna o emoji correspondente à extensão do arquivo."""
    _, ext = os.path.splitext(filename)
    return file_icons.get(ext.lower(), "📄")  # Padrão para arquivo

def generate_tree(path):
    """Gera a estrutura de diretórios recursivamente."""
    tree = {}
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree[f"📁 {item}"] = generate_tree(item_path)
        else:
            tree[f"{get_file_icon(item)} {item}"] = None
    return tree

if __name__ == "__main__":
    tree = generate_tree(".")
    output_filename = "directory_structure.yaml"

    # Garante que o arquivo seja salvo com codificação UTF-8
    with open(output_filename, "w", encoding="utf-8") as f:
        yaml.dump(tree, f, indent=2, allow_unicode=True)

    print(f"🌳 Estrutura do diretório exportada para '{output_filename}'! ✨")
