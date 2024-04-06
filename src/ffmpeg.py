import os
import asyncio
import argparse
from pathlib import Path

def convert_size(size_bytes):
    for unit in ['バイト', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

async def run_ffmpeg(input_path, output_path, show_result=False):
    if Path(input_path).is_dir():
        for file in Path(input_path).iterdir():
            if file.is_file() and file.suffix in ['.mp4', '.avi', '.mov', '.mkv']:
                output_file = Path(output_path) / file.name
                await process_file(str(file), str(output_file), show_result)
    else:
        output_path = Path(output_path) / Path(input_path).name
        await process_file(input_path, str(output_path), show_result)

async def process_file(input_file, output_file, show_result):
    # コマンドを構築
    cmd = f'ffmpeg -i "{input_file}" "{output_file}"'
    
    # 非同期サブプロセスを作成し、実行
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    
    # コマンドの実行が完了するまで待機
    stdout, stderr = await process.communicate()
    
    # 結果を出力
    if process.returncode == 0:
        print("コマンドが成功しました")
        if show_result:
            input_size = os.path.getsize(input_file)
            output_size = os.path.getsize(output_file)
            print(f"input file size: {convert_size(input_size)} bites")
            print(f"output file size: {convert_size(output_size)} bites")
    else:
        print("エラーが発生しました")
        print(stderr.decode())    

def main():
    parser = argparse.ArgumentParser(description='ffmpeg test')
    parser.add_argument('-i', '--input', required=True, help='input file path')
    parser.add_argument('-o', '--output', required=True, help='output file path')
    parser.add_argument('-s', '--show', action='store_true', help='show ffmpeg output')
    
    args = parser.parse_args()
    
    asyncio.run(run_ffmpeg(args.input, args.output, args.show))
    
if __name__ == '__main__':
    main()