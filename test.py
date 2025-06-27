from pathlib import Path

if __name__ == "__main__":
    root_dir = Path(R'C:\Users\fangw\Downloads\chrome')
    dir_in = root_dir / '本本Benjamin'
    
    video_files = list(dir_in.rglob('*'))
    print(video_files)

    video_files = list(dir_in.rglob("*.mp4"))
    print(video_files)

    video_files = list(dir_in.rglob("*.mp4")) + list(dir_in.rglob("*.m4a"))
    print(video_files)
