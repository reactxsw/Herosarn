from requests import post
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
font200 = ImageFont.truetype("rsc/Roboto.ttf", 200)
font145 = ImageFont.truetype("rsc/Roboto.ttf", 145)
font90 = ImageFont.truetype("rsc/Roboto.ttf", 90)

doc, lottery, ask, check, black = [], [], False, True, (0, 0, 0)
tday = datetime.today().strftime('%Y-%m-%d')
while check:
    response = post(headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                    url="https://www.glo.or.th/api/lottery/getLatestLottery")
    if response.status_code == 200:
        response = response.json()
        lastest = response["response"]["date"]
        print(
            f": กําลังหารางวัลของวันนี้ {tday} งวดล่าสุด : {lastest}")
        sleep(1)
        data = response["response"]["data"]
        for place in ["first", "second", "third", "fourth", "fifth", "last2", "last3f", "last3b", "near1"]:
            lottery.append(sorted([(data[place]["number"][i]["value"]) for i in range(
                len(data[place]["number"]))]))
        if response["response"]["date"] == tday:
            check = False
            print(
                f": พบรางวัลของวันนี้ {tday} งวดล่าสุด : {lastest}")
            print(
                f": เริ่มทําใบตรวจรางวัลของงวด : {lastest}")
        if not ask:
            ask = True
            if input(
                    f"[>] ต้องการปริ๊นใบตรวจงวด : {lastest} [Y/N] ").lower() == "y":
                check = False
                print(
                    f": เริ่มทําใบตรวจรางวัลของงวด : {lastest}")

# วันที่
previewimg = Image.open('rsc/preview.png')  # 3508x4960
blankimg = Image.new("RGB", (3508, 4960), "WHITE")
for img, canva in [(previewimg, ImageDraw.Draw(previewimg)),
                   (blankimg, ImageDraw.Draw(blankimg))]:
    if img == previewimg:
        date = lastest.split("-")
        canva.text((1025, 110), date[2] + "/" + date[1] +
                   "/" + date[0][2:], font=font145, fill=(255, 0, 0))
    # รางวัลที่ 1
    canva.text((250, 380), lottery[0][0], font=font200, fill=black)
    # เลขหน้า 3 ตัว
    canva.text((490, 790), lottery[6][0], font=font200, fill=black)
    canva.text((490, 980), lottery[6][1], font=font200, fill=black)
    # ใกล้ 1
    canva.text((160, 1330), lottery[8][0], font=font200, fill=black)
    canva.text((1000, 1330), lottery[8][1], font=font200, fill=black)
    # เลขท้าย 2 ตัว
    canva.text((1330, 380),
               lottery[5][0], font=font200, fill=black)
    # เลขท้าย 3 ตัว
    canva.text((1330, 790),
               lottery[7][0], font=font200, fill=black)
    canva.text((1330, 980),
               lottery[7][1], font=font200, fill=black)
    # รางวัลที่ 2
    canva.text((1000, 1680), lottery[1][0], font=font90, fill=black)
    canva.text((1000, 1780), lottery[1][1], font=font90, fill=black)
    canva.text((1000, 1880), lottery[1][2], font=font90, fill=black)
    canva.text((1420, 1680), lottery[1][3], font=font90, fill=black)
    canva.text((1420, 1780), lottery[1][4], font=font90, fill=black)
    canva.text((1420, 1880), "********", font=font90, fill=black)
    # รางวัลที่ 3
    for i, m in enumerate([(160, 2130), (160, 2230), (160, 2330),
                           (580, 2130), (580, 2230), (580, 2330),
                           (1000, 2130), (1000, 2230), (1420, 2130), (1420, 2230)]):
        canva.text(m, lottery[2][i], font=font90, fill=black)

    # รางวัลที่ 4
    # matrix = [n0 , nm , posx]
    posx = 1840
    for m in [[0, 16], [16, 32], [32, 41], [41, 50]]:
        posy = 830
        for num in lottery[3][m[0]:m[1]]:
            canva.text((posx, posy), num, font=font90, fill=black)
            posy += 100
        posx += 420

    # รางวัลที่ 5
    # matrix = [n0 , nm , posx , posy]
    posx = 160
    for i, m in enumerate([[0, 14], [14, 28], [
            28, 42], [42, 56], [56, 70], [70, 84], [84, 92], [92, 100]]):
        posy = 2565 if i < 6 else 3165
        for num in lottery[4][m[0]:m[1]]:
            canva.text((posx, posy), num, font=font90, fill=black)
            posy += 100
        posx += 420

    doc.append(img)
doc.extend([img.crop((0, 0, 3508, 2480)), img.crop((0, 2480, 3508, 4960))])

doc = doc[2], doc[3], doc[1], doc[0]
for count, page in enumerate(doc):
    page.save(f"page/HPage-{count}.png")
doc[0].save(f'H-{lastest}.pdf', save_all=True, append_images=doc[1:],
            title="Herosarn", author="Herosarn", subject="Lottery")

input(f": File saved as H-{lastest}.pdf")
