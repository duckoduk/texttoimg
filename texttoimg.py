import os
import csv
from PIL import Image, ImageDraw, ImageFont

# ✅ 자동 줄바꿈 함수
def wrap_text(text, font, draw, max_width):
    """텍스트가 max_width를 넘지 않도록 줄바꿈 처리"""
    lines = []
    words = text.split(' ')
    line = ''

    for word in words:
        test_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            line = test_line
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


# ✅ 출력 폴더 생성
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

# ✅ 폰트 경로 및 로드
font_path = "C:/Windows/Fonts/times.ttf"  # 사용자 지정 경로
try:
    font_title = ImageFont.truetype(font_path, 40)   # 장소 이름 폰트 크기
    font_address = ImageFont.truetype(font_path, 28) # 주소 폰트 크기
    print("✅ 폰트 로드 성공")
except Exception as e:
    raise FileNotFoundError(f"❌ 폰트 로드 실패: {e}")

# ✅ 텍스트 파일 읽기
input_file = "locations.txt"

with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if len(row) != 2:
            print(f"⚠️ 잘못된 형식 (줄 {i+1}): {row}")
            continue

        place, address = row
        place = place.strip('" ')
        address = address.strip('" ')

        # ✅ 이미지 생성 (크기: 300x300)
        img = Image.new('RGB', (300, 300), color='white')
        draw = ImageDraw.Draw(img)
        max_width = 260  # 여백 고려 (300 - 2*20)

        # ✅ 자동 줄바꿈 적용
        place_lines = wrap_text(place, font_title, draw, max_width)
        address_lines = wrap_text(address, font_address, draw, max_width)

        # ✅ 텍스트 추가
        y_position = 20  # 시작 Y 좌표

        # 장소 이름 추가
        for line in place_lines:
            draw.text((20, y_position), line, font=font_title, fill="black")
            bbox = font_title.getbbox(line)
            text_height = bbox[3] - bbox[1]
            y_position += text_height + 5  # 줄 간격 5px

        # ✅ 장소명과 주소 사이에 줄바꿈 추가 (빈 줄 높이만큼 추가)
        y_position += font_address.getbbox("A")[3] + 10  # 주소 폰트 높이 + 추가 간격

        # 주소 추가
        for line in address_lines:
            draw.text((20, y_position), line, font=font_address, fill="black")
            bbox = font_address.getbbox(line)
            text_height = bbox[3] - bbox[1]
            y_position += text_height + 3  # 줄 간격 3px

        # ✅ 파일 이름 처리
        safe_filename = "".join(c for c in place if c.isalnum() or c in (' ', '_')).strip().replace(" ", "_")
        image_path = os.path.join(output_dir, f"{safe_filename}.png")

        # ✅ 이미지 저장
        img.save(image_path)
        print(f"✅ 저장 완료: {image_path}")
