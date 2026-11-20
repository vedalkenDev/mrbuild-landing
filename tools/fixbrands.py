import sys, os
from collections import deque
from PIL import Image, ImageFilter, ImageChops
SRC, DST = sys.argv[1], sys.argv[2]
CUT = {'bostik','cornice_maker','glue_devil','jojo','nutec','pbes'}   # text logos on white: remove bg
ALL = {'bostik','cornice_maker','jojo','nutec'}  # no intended white: clear enclosed counters too
# badges (makita, matus, xpanda, ...) keep their own block; only trim margins
def unblend(im, region):
    w,h=im.size; px=im.load(); m=region.load()
    for y in range(h):
        for x in range(w):
            if not m[x,y]: continue
            r,g,b,a=px[x,y]
            al=max(255-r,255-g,255-b)/255.0
            if al<=0.02: px[x,y]=(0,0,0,0); continue
            f=lambda c:max(0,min(255,round((c-255*(1-al))/al)))
            px[x,y]=(f(r),f(g),f(b),round(a*al))
def bg_region(im, thr=238):
    w,h=im.size; px=im.load()
    seen=Image.new('L',(w,h),0); s=seen.load(); q=deque()
    ok=lambda x,y: px[x,y][3]<20 or min(px[x,y][:3])>=thr
    for x in range(w):
        for y in (0,h-1):
            if ok(x,y) and not s[x,y]: s[x,y]=255; q.append((x,y))
    for y in range(h):
        for x in (0,w-1):
            if ok(x,y) and not s[x,y]: s[x,y]=255; q.append((x,y))
    while q:
        x,y=q.popleft()
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<w and 0<=ny<h and not s[nx,ny] and ok(nx,ny): s[nx,ny]=255; q.append((nx,ny))
    return seen.filter(ImageFilter.MaxFilter(5))  # grow 2px into antialiased edge
def content_box(im):
    rgb=im.convert('RGB'); a=im.getchannel('A')
    nonwhite=ImageChops.difference(rgb,Image.new('RGB',im.size,'white')).convert('L').point(lambda v:255 if v>12 else 0)
    vis=ImageChops.multiply(nonwhite,a.point(lambda v:255 if v>20 else 0))
    return vis.getbbox()
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.png'): continue
    n=f[:-4]; im=Image.open(os.path.join(SRC,f)).convert('RGBA')
    if n in ALL: unblend(im, Image.new('L',im.size,255))
    elif n in CUT: unblend(im, bg_region(im))
    bb=content_box(im)
    if bb:
        pad=max(2,int(0.03*max(bb[2]-bb[0],bb[3]-bb[1])))
        bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad))
        im=im.crop(bb)
    im.save(os.path.join(DST,f),optimize=True); print(n,im.size)
