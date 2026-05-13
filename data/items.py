ITEMS = [
    {
        "id": "lighter",
        "name": "纵火犯的工具",
        "level": "E",
        "price": 30,
        "effect": "可以点燃大多数可燃物",
        "note": "发明者是一位热爱艺术的纵火犯。他说：'每一场火灾都是一幅转瞬即逝的画作。'后来他被自己的画作烧死了。"
    },
    {
        "id": "compass",
        "name": "不靠谱的指南针",
        "level": "E",
        "price": 20,
        "effect": "永远指向你来时的方向，而不是你要去的方向",
        "note": "发明者是个路痴，他把自己不需要的东西做成了道具。后来他失踪了，据说是因为跟着指南针走回了家。"
    },
    {
        "id": "fork",
        "name": "鉴定叉",
        "level": "D",
        "price": 50,
        "effect": "刺入物体后，可以鉴定出成分并推荐食用方法",
        "note": "一位永星餐厅的资深美食家发明了这种餐具。他对活人使用的最后一次鉴定结果是：'肌肉偏少，肥肉偏多，含微量毒素，食用基本无害。但食人违背人伦道德与美食操守，不建议食用。'"
    },
    {
        "id": "glasses",
        "name": "诚实眼镜",
        "level": "D",
        "price": 60,
        "effect": "戴上后能看到目标当前最强烈的情绪关键词",
        "note": "大部分人戴上后的第一发现是——别人看你时的真实想法是'这傻X戴了个什么玩意儿'。"
    },
    {
        "id": "bow_arrow",
        "name": "相互讨厌的弓与箭",
        "level": "E",
        "price": 25,
        "effect": "弓不喜欢被紧绷，箭不喜欢被射出去。十次中可能只有一次命中目标。但分开使用时，弓可作指南针，箭可在密闭空间内追踪目标。",
        "note": "弓和箭正在冷战，请不要在它们面前提起对方。"
    },
    {
        "id": "mask",
        "name": "扭曲面具",
        "level": "B",
        "price": 200,
        "effect": "戴上后，任何人看到它都会产生眩晕效果。三分钟内，谁也别想看清面具下的这张脸。",
        "note": "别看它像一张纸，但它确实很有用。唯一的缺点是——你自己也看不清路。"
    },
    {
        "id": "torch",
        "name": "无畏风雪的火把",
        "level": "E",
        "price": 35,
        "effect": "在恶劣天气下也不会熄灭的火把",
        "note": "生产商保证在任何天气下都能使用。测试人员在撒哈拉沙漠测试后反馈：'确实不灭，但我在沙漠里要火把干什么？'"
    },
    {
        "id": "shoes",
        "name": "超级跑鞋",
        "level": "E",
        "price": 40,
        "effect": "短时间内大幅提升移动速度",
        "note": "原名叫'跑得快'，但因为太直白了被市场部否决。改名后销量提升了300%——事实证明玩家就是这么好骗。"
    },
    {
        "id": "med_kit",
        "name": "基础自愈剂",
        "level": "E",
        "price": 25,
        "effect": "恢复30点HP",
        "note": "味道像过期的草莓味止咳糖浆。但效果还不错——只要你忍住不吐出来。"
    },
    {
        "id": "evol_p0",
        "name": "基础进化剂（P0）",
        "level": "E",
        "price": 80,
        "effect": "提升进化率5%",
        "note": "每一口都在提醒你——你的身体正在被改造成某种东西。至于变成什么，说明书上没写。"
    },
    {
        "id": "antidote",
        "name": "通用解毒剂",
        "level": "D",
        "price": 45,
        "effect": "解除大部分中毒状态",
        "note": "'通用'的意思是'大部分情况下有用'，'大部分情况下有用'的意思是'你最好祈祷自己在那个大部分里'。"
    },
    {
        "id": "earplug",
        "name": "隔音耳塞",
        "level": "E",
        "price": 15,
        "effect": "在安静环境下隔绝外部声音",
        "note": "便宜的塑料制品。隔音效果取决于你把它往耳朵里塞得有多深——塞太深你可能就取不出来了。"
    }
]


def get_item(item_id):
    for item in ITEMS:
        if item["id"] == item_id:
            return item.copy()
    return None


def get_shop_items(max_level="D"):
    return [item for item in ITEMS if item["price"] <= 200 and ord(item["level"]) >= ord(max_level)]


def describe_item(item):
    lines = []
    lines.append(f"  【{item['name']}】({item['level']}级)")
    lines.append(f"  效果：{item['effect']}")
    lines.append(f"  备注：{item['note']}")
    return "\n".join(lines)