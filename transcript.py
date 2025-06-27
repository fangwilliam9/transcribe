from pathlib import Path
import whisper
import json
import re
import time
import sys
import torch
import cv2
import mylib

INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1f]'
THIS_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_TYPES = ["medium"]


def save_md_json(jdata: dict, md_path: Path):
    try:
        text = jdata.get("text", 'no text here')
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text)
        # print("Saved")
    except Exception as e:
        print(f"Error saving files for {md_path.name}: {e}")
        exit(1)

def get_sleep_time(video_path:Path) -> int:
    try:
        # 打开视频文件
        video = cv2.VideoCapture(video_path)
        ## 获取视频帧率
        fps = video.get(cv2.CAP_PROP_FPS)
        # 检查 fps 是否为 0，避免/0错误
        if fps == 0:
            video.release()
            raise ValueError("视频的帧率 (fps) 为 0，无法计算时长！")
        ## 获取视频总帧数
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        ## 计算视频时长（秒）
        duration = frame_count / fps
        # 释放视频对象
        video.release()
        
        print(f'  {round(duration/60, 1)}min')
        # 根据时长决定sleep时间
        if duration > 60 * 60:
            return 60*3
        elif duration > 20 * 60: # 超过10分钟
            return 60 *2
        elif duration > 10 * 60: # 超过10分钟
            return 60 *1
        elif duration > 1 * 60: # 超过5分钟
            return 60 *0.5
        elif duration > 0.5 * 60: # 超过0.5分钟
            return 5
        else:
            return 0            # 不超过1分钟
    except Exception as e:
        print(f'get_sleep_time(): {e}')

def transcribe_and_save(dir: Path) -> bool:
    def check_env_device():
        print(f"Current Python path: {sys.executable}")
        print(f"Current device: {THIS_DEVICE}")
    
    check_env_device()
    for type in MODEL_TYPES:
        print(f"Loading model: {type}")
        model = whisper.load_model(type).to(THIS_DEVICE)
        print(f"Current device: {next(model.parameters()).device}")

        # 递归查找所有 .mp4 和 .m4a 文件
        video_paths = list(dir.rglob("*.mp4")) + list(dir.rglob("*.m4a"))
        if not video_paths:
            print("No video files found.")
            return
        for video_path in video_paths:
            # if transcribed
            base = video_path.stem
            md_path = video_path.parent / f'{base}.md'
            if md_path.exists():
                print(f'Has md already: {video_path}')
                continue
            # if not
            print(f"Transcribing: {video_path}")
            try:
                result_jdata = model.transcribe(
                    str(video_path),
                    language="zh",
                    fp16=torch.cuda.is_available(),
                    verbose=False,
                    initial_prompt="以下是简体中文的句子",
                    task="transcribe",
                )
                save_md_json(result_jdata, md_path)
                time2sleep = get_sleep_time(video_path)
                time.sleep(time2sleep)
            except Exception as e:
                print(f"Failed to process {video_path.name}: {e}")
                return False
    # 
    if mylib.traverse_process(dir):
        print('All done, en_to_zh replacement')
    return True
    # print('All done.')


if __name__ == "__main__":
    dir = Path( input('path: ') )

    if not dir.exists():
        print(f'No such dir: {dir}')
        exit(0)

    transcribe_and_save(dir)