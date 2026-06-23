#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

BRAND=(224,101,79); CREAM=(251,247,244); INK=(36,31,28); WHITE=(255,255,255)

def font(sz, bold=True):
    paths=["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
           "/System/Library/Fonts/Helvetica.ttc","/Library/Fonts/Arial.ttf"]
    for p in paths:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def logo_dot(size, pad_ratio=0.0, bg=None):
    """A peach circle with a white inner dot (the brand mark). Optional rounded bg."""
    S=size*4  # supersample
    img=Image.new("RGBA",(S,S),(0,0,0,0))
    d=ImageDraw.Draw(img)
    if bg:
        r=int(S*0.22)
        d.rounded_rectangle([0,0,S,S], radius=r, fill=bg)
    m=int(S*0.10)
    d.ellipse([m,m,S-m,S-m], fill=BRAND)
    # white crescent highlight (top-left)
    hi=int(S*0.30)
    d.ellipse([int(S*0.26),int(S*0.22),int(S*0.26)+hi,int(S*0.22)+hi], fill=WHITE)
    return img.resize((size,size), Image.LANCZOS)

# favicon.ico (multi-size)
ico=logo_dot(256)
ico.save("favicon.ico", sizes=[(16,16),(32,32),(48,48),(64,64)])

# apple-touch-icon 180x180 with cream rounded bg
apple=logo_dot(180, bg=CREAM)
apple.save("apple-touch-icon.png")

# 512 maskable / pwa icon
logo_dot(512, bg=CREAM).save("icon-512.png")

# favicon.svg
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="42" fill="#e0654f"/>
<circle cx="40" cy="38" r="15" fill="#ffffff"/>
</svg>'''
open("favicon.svg","w").write(svg)

# og.png 1200x630
W,H=1200,630
og=Image.new("RGB",(W,H),CREAM)
d=ImageDraw.Draw(og)
# subtle top bar
d.rectangle([0,0,W,10], fill=BRAND)
# logo
dot=logo_dot(150)
og.paste(dot,(90,90),dot)
d.text((260,120), "AcneSafeCheck", font=font(58), fill=INK)
d.text((92,300), "Acne Safe Ingredient Checker", font=font(72), fill=INK)
d.text((92,400), "Paste any skincare ingredient list — instantly see", font=font(36,bold=False), fill=(111,101,94))
d.text((92,446), "which ingredients are pore-clogging (comedogenic).", font=font(36,bold=False), fill=(111,101,94))
# pills (no emoji to avoid font issues)
def pill(x,y,txt,col,bgc):
    f=font(30); tb=d.textbbox((0,0),txt,font=f); w=tb[2]-tb[0]
    d.rounded_rectangle([x,y,x+w+44,y+56], radius=28, fill=bgc)
    d.text((x+22,y+11),txt,font=f,fill=col)
    return x+w+44+18
x=92
x=pill(x,532,"560+ ingredients",(196,77,56),(253,232,227))
x=pill(x,532,"100% free",(47,158,111),(231,246,238))
x=pill(x,532,"No signup",(217,154,0),(251,242,216))
og.save("og.png","PNG")
print("images written")
