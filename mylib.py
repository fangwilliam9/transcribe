from pathlib import Path
import tempfile
import shutil

def en_to_zh(md_path: Path):
    """
    将英文标点符号替换为中文标点符号
    - 英文逗号 , → 中文逗号 ，
    - 英文句号 . → 中文句号 。
    - 英文问号 ? → 中文问号 ？
    - 英文感叹号 ! → 中文感叹号 ！
    """
    # 定义替换规则
    replacements = {
        ',': '，',
        '.': '。',
        '?': '？',
        # '!': '！'
    }
    
    # 读取文件内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 执行替换
    for en_punc, zh_punc in replacements.items():
        content = content.replace(en_punc, zh_punc)
    
    return content

def traverse_process(dir_in: Path) -> bool:
    """
    递归处理目录下所有.md文件
    """
    # 递归查找所有.md文件
    md_files = list(dir_in.rglob("*.md"))

    if not md_files:
        print("No md files found.")
        return False

    print("  en_to_zh processing")
    for md_path in md_files:
        try:
            # 处理文件内容
            new_content = en_to_zh(md_path)
            
            # 使用tempfile安全保存
            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                delete=False,
                suffix='.md'
            ) as tmp_file:
                tmp_file.write(new_content)
                tmp_path = Path(tmp_file.name)
            
            # 替换原文件
            shutil.move(str(tmp_path), str(md_path))
        except Exception as e:
            print(f"Failed to process {md_path.name}: {e}")
            return False

    return True

if __name__ == "__main__":
    root_dir = Path(r'C:\Users\fangw\Downloads\chrome')
    which_to_process = input('Input directory to process (relative to root): ')
    dir_in = root_dir / which_to_process

    if not dir_in.exists():
        print(f'No such directory: {dir_in}')
        exit(0)

    traverse_process(dir_in)