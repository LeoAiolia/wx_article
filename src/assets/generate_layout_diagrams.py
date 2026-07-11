import os
from PIL import Image, ImageDraw, ImageFont

def create_diagram(case_num, filename):
    # 图像参数 - 简单白底黑字风格
    img_w, img_h = 800, 180
    bg_color = (255, 255, 255)  # 白色背景
    container_bg = (248, 250, 252)  # #F8FAFC - 容器浅灰蓝
    container_border = (148, 163, 184)  # #94A3B8 - 容器中灰边框
    
    # 创建画布
    image = Image.new("RGBA", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(image)
    
    # 容器参数
    pad_x = 100
    pad_y = 50
    con_w = img_w - 2 * pad_x  # 600
    con_h = 80
    con_x1, con_y1 = pad_x, pad_y
    con_x2, con_y2 = con_x1 + con_w, con_y1 + con_h
    
    # 绘制父容器圆角矩形
    draw.rounded_rectangle([con_x1, con_y1, con_x2, con_y2], radius=8, fill=container_bg, outline=container_border, width=2)
    
    # 字体加载
    font_path_cn = "/System/Library/Fonts/PingFang.ttc"
    
    if not os.path.exists(font_path_cn):
        font_path_cn = "/System/Library/Fonts/Supplemental/Arial.ttf" # Fallback
        
    try:
        font_title = ImageFont.truetype(font_path_cn, 15)
        font_text = ImageFont.truetype(font_path_cn, 13)
        font_tag = ImageFont.truetype(font_path_cn, 12)
        font_badge = ImageFont.truetype(font_path_cn, 11)
    except IOError:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    # 绘制标题栏（黑字）
    title_texts = {
        1: "情况一：纯 Row 布局 (未加约束导致的 Flex Overflow 越界报错)",
        2: "情况二：单侧 Flexible (右侧太长把左侧 iOS 观之挤压到极限)",
        3: "情况三：双侧 Flexible (左长右短，由于隔离测量导致左侧提前截断)",
        4: "情况四：CustomMultiChildLayout (智能顺序测量，左右各取所需且完美对齐)"
    }
    draw.text((pad_x, 18), title_texts[case_num], fill=(15, 23, 42), font=font_title)

    # 颜色系统 - 白底下的绿色与红色背景
    # 绿色背景组件（左侧 TextA）：浅绿填充，深绿边框，黑字
    left_fill = (232, 245, 233, 255)      # #E8F5E9
    left_outline = (76, 175, 80, 255)     # #4CAF50
    # 红色背景组件（右侧 TextB）：浅红填充，深红边框，黑字
    right_fill = (255, 235, 238, 255)     # #FFEBEE
    right_outline = (244, 67, 54, 255)    # #F44336
    
    text_color = (0, 0, 0) # 文字全用纯黑
    
    # 绘制子组件
    if case_num == 1:
        # 左侧文字：极长
        lw = 320
        lx1 = con_x1 + 10
        ly1 = con_y1 + 15
        lx2 = lx1 + lw
        ly2 = con_y2 - 15
        draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=4, fill=left_fill, outline=left_outline, width=1)
        draw.text((lx1 + 8, ly1 + 14), "这是一个超级漫长且有深度的 iOS 观之微信...", fill=text_color, font=font_text)
        
        # 右侧文字：极长，会越界
        rw = 320
        rx1 = lx2 + 10  # 440
        ry1 = con_y1 + 15
        rx2 = rx1 + rw  # 760
        ry2 = con_y2 - 15
        draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=4, fill=right_fill, outline=right_outline, width=1)
        draw.text((rx1 + 8, ry1 + 14), "移动端前沿开发技术与跨平台工程实践干货...", fill=text_color, font=font_text)
        
        # 溢出指示器（黄黑斜线）
        overflow_x = con_x2
        draw.rectangle([overflow_x, con_y1 + 2, overflow_x + 65, con_y2 - 2], fill=(234, 179, 8, 240))
        for offset in range(-10, 80, 12):
            draw.line([overflow_x + offset, con_y2, overflow_x + offset + 15, con_y1], fill=(0, 0, 0, 255), width=4)
        draw.rectangle([overflow_x - 110, con_y1 + 25, overflow_x - 5, con_y1 + 55], fill=(220, 38, 38))
        draw.text((overflow_x - 105, con_y1 + 32), "OVERFLOW 60px", fill=(255, 255, 255), font=font_badge)

    elif case_num == 2:
        # 左侧被挤压
        lw = 110
        lx1 = con_x1 + 10
        ly1 = con_y1 + 15
        lx2 = lx1 + lw
        ly2 = con_y2 - 15
        draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=4, fill=left_fill, outline=left_outline, width=1)
        draw.text((lx1 + 8, ly1 + 14), "iOS观之（超长...", fill=text_color, font=font_text)
        draw.rectangle([lx1 + 75, ly1 - 6, lx1 + 105, ly1 + 6], fill=(220, 38, 38))
        draw.text((lx1 + 78, ly1 - 5), "被压", fill=(255, 255, 255), font=font_badge)

        # 右侧超长标签，吃掉 450px 空间
        rw = 450
        rx1 = lx2 + 10  # 220
        ry1 = con_y1 + 15
        rx2 = rx1 + rw  # 670
        ry2 = con_y2 - 15
        draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=4, fill=right_fill, outline=right_outline, width=1)
        draw.text((rx1 + 8, ry1 + 14), "移动端前沿技术周刊与系统底层架构深度拆解干货内容及最新...", fill=text_color, font=font_text)

    elif case_num == 3:
        # 双侧 Flexible
        lw = 275
        lx1 = con_x1 + 10
        ly1 = con_y1 + 15
        lx2 = lx1 + lw  # 385
        ly2 = con_y2 - 15
        draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=4, fill=left_fill, outline=left_outline, width=1)
        draw.text((lx1 + 8, ly1 + 14), "iOS 观之公众号专注于 Flutter 与 iOS 跨...", fill=text_color, font=font_text)
        
        # 右侧很短
        rw = 70
        rx1 = lx2 + 10  # 395
        ry1 = con_y1 + 15
        rx2 = rx1 + rw  # 465
        ry2 = con_y2 - 15
        draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=4, fill=right_fill, outline=right_outline, width=1)
        draw.text((rx1 + 15, ry1 + 14), "置顶标签", fill=text_color, font=font_text)
        
        # 浪费的空白区域
        empty_x1 = rx2 + 5
        empty_x2 = con_x2 - 10
        draw.text((empty_x1 + 15, con_y1 + 32), "← 空白闲置区域（未被合理利用） →", fill=(148, 163, 184), font=font_tag)

    elif case_num == 4:
        # CustomMultiChildLayout
        lw = 400
        lx1 = con_x1 + 10
        ly1 = con_y1 + 15
        lx2 = lx1 + lw  # 510
        ly2 = con_y2 - 15
        draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=4, fill=left_fill, outline=left_outline, width=1)
        draw.text((lx1 + 8, ly1 + 14), "iOS 观之公众号专注于 Flutter 与 iOS 跨平台技术架构深度...", fill=text_color, font=font_text)
        
        # 右侧短，贴在最右端
        rw = 70
        rx2 = con_x2 - 10  # 690
        rx1 = rx2 - rw  # 620
        ry1 = con_y1 + 15
        ry2 = con_y2 - 15
        draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=4, fill=right_fill, outline=right_outline, width=1)
        draw.text((rx1 + 15, ry1 + 14), "置顶标签", fill=text_color, font=font_text)
        
        # 中间的自然留白
        draw.text((lx2 + 25, con_y1 + 32), "← 自然留白 →", fill=(71, 85, 105), font=font_tag)
        
    image.save(filename, "PNG")
    print(f"Generated: {filename}")

if __name__ == "__main__":
    assets_dir = "/Users/run/Documents/yxr/wx_article/src/assets"
    os.makedirs(assets_dir, exist_ok=True)
    
    create_diagram(1, os.path.join(assets_dir, "inline-layout-case1.png"))
    create_diagram(2, os.path.join(assets_dir, "inline-layout-case2.png"))
    create_diagram(3, os.path.join(assets_dir, "inline-layout-case3.png"))
    create_diagram(4, os.path.join(assets_dir, "inline-layout-case4.png"))
