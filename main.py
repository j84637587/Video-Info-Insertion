from PIL import Image, ImageDraw, ImageFont
import cv2
import pandas as pd
import numpy as np
from moviepy.editor import VideoFileClip

FONT_PATH = "C:/Windows/Fonts/msjh.ttc" # 字型檔

def readCSV(path = 'example.csv'):
    """讀取CSV
    """
    df = pd.read_csv(path, encoding='big5')
    return df


def makeCaption(col_names, info):
    """將要嵌入的資訊格式化
    """
    seq = []
    for col in col_names:
        seq.append(f"{col}: {info[col]}")
        # cv2.putText(frame, text, (10, 10 * y_off), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA, True)
    return seq


def generateSquence(video, cap_data):
    """產生每個Frame的所要顯示的資訊
    """
    FPM = int(video.fps * 60)  # FPM
    TOTAL_FRAMES = int(video.fps * video.duration)  # 影片總畫面數
    cap_len = len(cap_data)  # 資訊數

    print(f"FPM: {FPM}   Total Frames: {TOTAL_FRAMES}\nFrames Min Required: {cap_len}")

    # 確保Frame數量足夠
    if TOTAL_FRAMES < cap_len:
        raise Exception(f'Frames of video is not enough to fit info. Frames of video is {TOTAL_FRAMES}, at least {cap_len} is needed.')

    # 取得時間Key
    times = sorted(cap_data.time.unique().astype('str'))
    sequence = []

    # loop time by time
    for time in times:
        crr_minu_info = cap_data.loc[cap_data.time == time]
        info_cnt = len(crr_minu_info)
        print(time, info_cnt)
        dur = int(FPM / info_cnt)
        rest = FPM % info_cnt
        # print(f'-' * 40)
        # print(f'Time: {time}, Info Count: {info_cnt}') # info_cnt 不可大於 FPM
        # print(f'Duribility: {dur}, Rest Of Frames: {rest}')
        dur_cfg = [dur] * info_cnt
        dur_cfg[:rest] = map((1).__add__, dur_cfg[:rest])
        idx = 0
        for _, row in crr_minu_info.iterrows():
            sequence += dur_cfg[idx] * [makeCaption(crr_minu_info, row)]
            idx += 1
    return sequence


def cv2ImgAddText(img, text, pos, textColor=(0, 255, 0), textSize=36):
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(FONT_PATH, textSize, encoding="utf-8")
    draw.text(pos, text, textColor, font=fontText)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def pipeline(frame, seq):
    try:
        # cv2 不支援 non-ascii
        # cv2.putText(frame, "這是測試", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)
        texts = seq.pop(0)
        for i, text in enumerate(texts):
            frame = cv2ImgAddText(frame, text, (30, 50 * (i+1)))
    except Exception as e:
        pass
    return frame


def main():
    cap_data = readCSV()
    video = VideoFileClip("example.mp4")
    sequence = generateSquence(video, cap_data)
    video = video.fl_image(lambda frame: pipeline(frame, sequence))
    video.write_videofile("result.mp4", audio=True)

if __name__ == '__main__':
    main()
