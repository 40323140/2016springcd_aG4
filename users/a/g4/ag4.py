from flask import Blueprint, request
 
ag4_1 = Blueprint('ag4_1', __name__, url_prefix='/ag4_1', template_folder='templates')
 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
</head>
<body>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
'''
 
tail_str = '''
</script>
</body>
</html>
'''
 
chain_str = '''
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    #chamber = "M 0, 0 L 0, -20 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgoChamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole0 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
'''
 
@ag4_1.route('/gears', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/gears/<n1>/<n2>/<n3>/<n4>/<n5>')
def gears(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 15
n2 = 17
n3 = 20
n4 = 29
n5 = 40
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/n4+(180-180/n3)*n3/n4)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy,m,n5,pa,(180+180/n5+(180-180/n3)*n4/n5)-3)
</script>'''
    return outstring
@ag4_1.route('/gears09', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/gears09/<n1>/<n2>/<n3>/<n4>/<n5>')
def gears09(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 50
n2 = 17
n3 = 30
n4 = 29
n5 = 40
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/n4+(180-180/n3)*n3/n4)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy,m,n5,pa,(180+180/n5+(180-180/n3)*n4/n5)-4)
</script>'''
    return outstring
@ag4_1.route('/gears30', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/gears30/<n1>/<n2>/<n3>/<n4>/<n5>')
def gears30(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 60
n2 = 5
n3 = 20
n4 = 29
n5 = 40
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/n4+(180-180/n3)*n3/n4)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy,m,n5,pa,(180+180/n5+(180-180/n3)*n4/n5)-3)
</script>'''
    return outstring
@ag4_1.route('/gears35', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/gears35/<n1>/<n2>/<n3>/<n4>/<n5>')
def gears35(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 70
n2 = 17
n3 = 5
n4 = 29
n5 = 40
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/n4+(180-180/n3)*n3/n4)

</script>'''
    return outstring
@ag4_1.route('/gears36', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/gears36/<n1>/<n2>/<n3>/<n4>/<n5>')
def gears36(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 5
n2 = 10
n3 = 20
n4 = 40
n5 = 60
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/(n4+(180-180/n3)*n3/n4)-4)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy,m,n5,pa,(180+180/n5+((180-180/n3)*n4/n5)-3)-5)
</script>'''
    return outstring
@ag4_1.route('/gears44', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/gears44/<n1>/<n2>/<n3>/<n4>/<n5>')
def gears44(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 5
n2 = 10
n3 = 6
n4 = 10
n5 = 40
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/n4+((180-180/n3)*n3/n4)-17)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy,m,n5,pa,(180+180/n5+(180-180/n3)*n4/n5)-6)
</script>'''
    return outstring
@ag4_1.route('/cdw18gears', defaults={'n1':17,'n2':29,'n3':15,'n4':40,'n5':20})
@ag4_1.route('/cdw18gears/<n1>/<n2>/<n3>/<n4>/<n5>')
def cdw18gears(n1, n2, n3, n4, n5):
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">

<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = 40
n2 = 17
n3 = 20
n4 = 29
n5 = 40

# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3+n4+n5)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
pr4 = n4*m/2
pr5 = n5*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy,m,n4,pa,180-180/n4+(180-180/n3)*n3/n4)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy,m,n5,pa,(180+180/n5+(180-180/n3)*n4/n5)-3)

spur(cx, cy+pr5+pr5, m, n1, pa, (180-180/n1))
spur(cx+pr1+pr2, cy+pr5+pr5, m, n2, pa, (180-180/n2)+10)
spur(cx+pr1+pr2+pr2+pr3, cy+pr5+pr5, m, n3, pa, 180-180/n3+((180-180/n2)*n2/n3)+10)
spur(cx+pr1+pr2+pr2+2*pr3+pr4,cy+pr5+pr5,m,n4,pa,180-180/n4+((180-180/n3)*n3/n4)+5)
spur(cx+pr1+pr2+pr2+2*pr3+2*pr4+pr5,cy+pr5+pr5,m,n5,pa,(180+180/n5+(180-180/n3)*n4/n5)-3+5)


</script>'''
    return outstring
