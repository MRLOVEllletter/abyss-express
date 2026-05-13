# 深渊列车 · Abyss Express — Web Bundle
import sys, time, random

# === engine/display.py ===
import time
import sys

SLOW_TYPING = True
SLOW_SPEED = 0.015


def set_slow(enable):
    global SLOW_TYPING
    SLOW_TYPING = enable


def slow_print(text, end="\n"):
    if SLOW_TYPING:
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(SLOW_SPEED)
        sys.stdout.write(end)
        sys.stdout.flush()
    else:
        print(text, end=end)


def print_line(char="━", length=50):
    print(char * length)


def print_header(title, subtitle=""):
    print("╔" + "═" * 48 + "╗")
    title_line = f"║{title:^48}║"
    print(title_line)
    if subtitle:
        sub_line = f"║{subtitle:^48}║"
        print(sub_line)
    print("╚" + "═" * 48 + "╝")


def print_menu(title, options):
    print()
    print(f"  【{title}】")
    print()
    for key, desc in options:
        print(f"    {key}. {desc}")
    print()


def print_event_menu(options):
    for i, (text, _) in enumerate(options, 1):
        print(f"    {i}. {text}")
    print()


def get_event_choice(options):
    valid = [str(i) for i in range(1, len(options) + 1)]
    while True:
        choice = input("  请选择：").strip()
        if choice in valid:
            idx = int(choice) - 1
            return options[idx][1]
        print(f"  无效输入，请输入 1-{len(options)}")


def get_choice(prompt="请选择：", valid=None):
    while True:
        choice = input(prompt).strip()
        if valid is None or choice in valid:
            return choice
        print(f"无效输入，请输入 {', '.join(valid)}")


def wait_enter():
    input("\n 按 Enter 继续...")


def typewriter(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

# === player/player.py ===

PROFESSIONS = {
    "A": {
        "name": "赌徒",
        "title": "命运是一副牌，而我是那个出千的人。",
        "hp": 80,
        "trait": "胜率波动 —— 每次行动前可'下注'，下注越高，成功率波动越大",
        "desc": "你相信概率，但不相信公平。在别人眼中你是疯子，但你清楚——这个世界本来就是一场赌局。"
    },
    "B": {
        "name": "路人甲",
        "title": "站在人群中，你永远不会注意到我。这就是我的优势。",
        "hp": 100,
        "trait": "一件悲伤的事 —— 在不被关注时，容易被他人遗忘",
        "desc": "你习惯低调，习惯被忽视。但在阴影中待久了，你会发现很多别人看不到的东西。"
    },
    "C": {
        "name": "冒险家",
        "title": "未知是最好的邀请函。",
        "hp": 120,
        "trait": "危险嗅觉 —— 能感知到周围环境中隐藏的危险",
        "desc": "你天生属于荒野和废墟。别人避之不及的地方，对你来说就是游乐园。"
    },
    "D": {
        "name": "拾荒者",
        "title": "别人的垃圾，是我的宝藏。",
        "hp": 90,
        "trait": "废品眼光 —— 可以识别出物品的隐藏价值",
        "desc": "你的眼睛能在一堆破烂中找到真正的宝贝。这个世界丢掉的，你负责捡起来。"
    },
    "E": {
        "name": "守夜人",
        "title": "我在黑暗中守护，不是为了被记住，而是为了让更多人看到黎明。",
        "hp": 110,
        "trait": "不破之壁 —— 可以为队友创造临时安全区域",
        "desc": "你习惯了在黑暗中保持清醒。守护他人是你的本能，即使没人知道你的名字。"
    }
}


class Player:
    def __init__(self, name, prof_id):
        self.name = name
        self.prof_id = prof_id
        prof = PROFESSIONS[prof_id]
        self.prof_name = prof["name"]
        self.prof_title = prof["title"]
        self.prof_desc = prof["desc"]
        self.trait = prof["trait"]
        self.max_hp = prof["hp"]
        self.hp = self.max_hp
        self.evolution_rate = 0
        self.white_bills = 100
        self.inventory = []
        self.traits = [prof["trait"]]
        self.dungeon_count = 0
        self.total_score = 0

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return self.hp == 0

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item_id):
        for i, item in enumerate(self.inventory):
            if item["id"] == item_id:
                return self.inventory.pop(i)
        return None

    def has_item(self, item_id):
        return any(item["id"] == item_id for item in self.inventory)

    def show_stats(self):
        print_line()
        print(f"  【玩家档案】")
        print(f"  姓名：{self.name}")
        print(f"  职业：{self.prof_name}")
        print(f"  称号：{self.prof_title}")
        print()
        print(f"  HP：{self.hp}/{self.max_hp}")
        print(f"  进化率：{self.evolution_rate}%")
        print(f"  白钞：{self.white_bills}")
        print(f"  通关副本：{self.dungeon_count}")
        print()
        print(f"  【特性】")
        for t in self.traits:
            print(f"    · {t}")
        print()
        if self.inventory:
            print(f"  【道具栏】（{len(self.inventory)}件）")
            for item in self.inventory:
                print(f"    · {item['name']}（{item['level']}级）")
        else:
            print(f"  【道具栏】空")
        print_line()

# === data/items.py ===
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

# === train/train.py ===


TRAIN_RULES = """  深渊列车乘车规则：

  1. 必须消费。—— 列车不养闲人，每位乘客必须在每趟旅程中至少消费一次。
  2. 熄灯后请勿离开包厢。—— 熄灯后的走廊里有什么，没人说得清。
  3. 禁止在车厢内使用攻击性道具。—— 但"非攻击性"的定义比较灵活。
  4. 乘务员有权驱逐违规乘客。—— 别得罪他们。
  5. 列车鼓励偷袭、斗殴、猎食等多种休闲方式，但请注意不要影响列车正常运行。

  祝您旅途愉快。"""


def show_rules():
    print_header("深渊列车 · 乘车规则")
    slow_print(TRAIN_RULES)
    wait_enter()


def sleep_carriage(player):
    print_header("住宿车厢")
    slow_print("你走进住宿车厢，走廊两侧是一扇扇紧闭的包厢门。")
    slow_print("空气中弥漫着老旧的木头和灰尘的味道。")
    print_line()
    slow_print(f"当前HP：{player.hp}/{player.max_hp}")
    print_menu("选择", [
        ("1", "在床上休息（恢复50%HP）"),
        ("2", "睡个长觉（恢复全部HP，花费20白钞）"),
        ("0", "返回大厅")
    ])
    choice = get_choice()
    if choice == "1":
        heal = player.max_hp // 2
        player.heal(heal)
        slow_print(f"你躺下休息了一会儿。HP恢复 {heal} 点。")
        slow_print("床板有点硬，但在这个世界里，能躺着就已经很奢侈了。")
    elif choice == "2":
        if player.white_bills >= 20:
            player.white_bills -= 20
            player.heal(player.max_hp)
            slow_print("你付了20白钞，要了一间高级包厢。")
            slow_print("床很软，枕头上有薰衣草的味道。你睡得很好。")
            slow_print("HP已全部恢复。")
        else:
            slow_print("你翻了翻口袋，发现连20白钞都没有。")
            slow_print("乘务员用同情的眼神看着你。那眼神让你更难受了。")
    wait_enter()


def trade_carriage(player):
    print_header("交易车厢")
    slow_print("车厢里摆满了各种各样的商品，从破铜烂铁到闪闪发光的道具。")
    slow_print("柜台后的商贩用警惕的眼神打量着你。")
    print_line()
    print_menu("选择", [
        ("1", "浏览商品"),
        ("2", "出售道具"),
        ("0", "返回大厅")
    ])
    choice = get_choice()
    if choice == "1":
        _browse_shop(player)
    elif choice == "2":
        _sell_items(player)
    wait_enter()


def _browse_shop(player):
    print_header("商品列表")
    available = [item for item in ITEMS if item["price"] <= 200]
    for i, item in enumerate(available):
        print(f"  {i+1}. {item['name']}（{item['level']}级）— {item['price']}白钞")
        print(f"     效果：{item['effect']}")
        print()
    print(f"  你的白钞：{player.white_bills}")
    print()
    choice = input("  输入编号购买，输入 0 返回：").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(available):
            item = available[idx]
            if player.white_bills >= item["price"]:
                player.white_bills -= item["price"]
                player.add_item(item.copy())
                slow_print(f"你买下了【{item['name']}】。")
                slow_print(f"备注：{item['note']}")
            else:
                slow_print("白钞不够。商贩翻了翻白眼，继续擦他的玻璃柜。")
        elif int(choice) != 0:
            slow_print("无效编号。")


def _sell_items(player):
    if not player.inventory:
        slow_print("你翻遍了所有口袋，发现什么都没有。")
        slow_print("连商贩都懒得看你一眼。")
        return
    print_header("你的道具")
    for i, item in enumerate(player.inventory):
        print(f"  {i+1}. {item['name']}（{item['level']}级）")
    print()
    choice = input("  输入编号出售，输入 0 返回：").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(player.inventory):
            item = player.inventory.pop(idx)
            price = max(item["price"] // 2, 5)
            player.white_bills += price
            slow_print(f"你卖掉了【{item['name']}】，获得 {price} 白钞。")
            slow_print("商贩接过道具，面无表情地把它扔进身后的麻袋里。")
            slow_print("你感觉自己被坑了，但你没有证据。")


def info_carriage(player):
    print_header("情报车厢")
    slow_print("车厢里挂满了各种地图、照片和潦草的笔记。")
    slow_print("一个戴眼镜的老人坐在堆满文件的桌子后面，抬头看了你一眼。")
    print_line()
    slow_print("老人清了清嗓子：")
    slow_print("'新人？那你应该先了解一下你能去的地方。'")
    print_line()
    _show_dungeon_info()
    wait_enter()


def _show_dungeon_info():
    print("  【当前可用副本】")
    print()
    print("  ═══════════════════════════════════")
    print("  副本：分贝小镇")
    print("  等级要求：E级")
    print("  副本时间：7天")
    print("  建议人数：1人")
    print()
    print("  背景：分贝小镇曾经是一个宁静的旅游小镇，")
    print("  直到有一天，小镇上的所有声音都消失了。")
    print("  不是没有声音，而是所有超过呼吸声的音量都会消失。")
    print("  然后，小镇的钟塔开始倒着走。")
    print("  然后，居民开始失踪。")
    print("  然后，你来到了这里。")
    print("  ═══════════════════════════════════")
    print()
    slow_print("老人补充道：'这个副本的关键是——管好你的嘴。'")


def bar_carriage(player):
    print_header("酒吧车厢")
    slow_print("昏暗的灯光，嘈杂的人声，混杂着酒精和烟草的味道。")
    slow_print("角落里一个醉醺醺的乘客注意到了你。")
    print_line()
    _rumors = [
        "'听说014区出了件超级道具……那玩意儿能让人回到三秒前。'",
        "'别相信情报车厢那老头说的话，他上次跟我说一个E级副本简单，结果我差点死在里面。'",
        "'你知道为什么列车上禁止用攻击性道具吗？因为有人曾经炸掉了一整节车厢。'",
        "'我听说有个玩家在分贝小镇里待了七天，出来以后就再也没说过话。'",
        "'乘务员？他们以前也是玩家。至于为什么选择留下来——没人知道。'",
    ]
    import random
    rumor = random.choice(_rumors)
    slow_print(f"醉汉含糊地说：{rumor}")
    print_line()
    slow_print("他打了个酒嗝，又趴回桌上睡着了。")
    wait_enter()


def show_train_hub(player):
    while True:
        print_header(
            f"深渊列车 · 主神空间",
            f"乘客 {player.name} · {player.prof_name}"
        )
        print(f"  HP：{player.hp}/{player.max_hp}")
        print(f"  进化率：{player.evolution_rate}%  |  白钞：{player.white_bills}")
        print(f"  道具：{len(player.inventory)}件  |  通关：{player.dungeon_count}次")
        print_line()
        print_menu("车厢选择", [
            ("1", "住宿车厢 —— 休息恢复"),
            ("2", "交易车厢 —— 购买道具"),
            ("3", "情报车厢 —— 副本情报"),
            ("4", "酒吧车厢 —— 听听传闻"),
            ("5", "查看乘车规则"),
            ("6", "查看玩家档案"),
            ("7", "前往副本 —— 开始任务"),
            ("0", "退出游戏")
        ])
        choice = get_choice()
        if choice == "1":
            sleep_carriage(player)
        elif choice == "2":
            trade_carriage(player)
        elif choice == "3":
            info_carriage(player)
        elif choice == "4":
            bar_carriage(player)
        elif choice == "5":
            show_rules()
        elif choice == "6":
            player.show_stats()
            wait_enter()
        elif choice == "7":
            return "dungeon"
        elif choice == "0":
            return "quit"

# === dungeons/town.py ===
import random

EVENTS_POOL = [
    {
        "title": "街角的老人",
        "desc": "一个老人坐在街角的台阶上，似乎在等人。他看到你，微微点了点头。",
        "choices": [
            ("上前搭话", "talk"),
            ("默默走开", "leave")
        ],
        "result_talk": "老人说：'钟塔的指针是反的。记住，反的不只是时间。'你不太明白他的意思，但把这句话记在了心里。\n获得线索：钟塔的秘密",
        "result_leave": "你从老人身边走过。他的目光一直跟着你，直到你消失在街角。"
    },
    {
        "title": "废弃的报刊亭",
        "desc": "报刊亭的玻璃碎了，里面的报纸被风吹得到处都是。一张发黄的报纸上写着：'钟塔建成百年，镇长宣布将举办庆典。'日期是三十年前。",
        "choices": [
            ("翻找有用的东西", "search"),
            ("看看其他报纸", "read")
        ],
        "result_search": "你在柜台下面找到了一本破旧的日记。日记的主人似乎曾经是这里的报摊主。\n获得道具：陈旧的日记本",
        "result_read": "其他报纸上都是普通的小镇新闻——谁家的猫丢了，谁家的孩子考了第一名。看起来很平静的小镇。太平静了。"
    },
    {
        "title": "神秘的地下室入口",
        "desc": "你发现一扇半掩在地面的铁门。门上挂着一把锈迹斑斑的锁，锁上刻着奇怪的符号。",
        "choices": [
            ("想办法打开锁", "open"),
            ("先记下位置，以后再来", "note")
        ],
        "result_open": "你费了好大劲才撬开锁。铁门后面是一条通向地下的阶梯，黑暗而潮湿。你隐约听到深处有滴水声。\n你决定改天准备好再下来探索。",
        "result_note": "你记住了这个位置。也许以后会有用。"
    }
]

SOUND_POLICE_ENCOUNTERS = [
    "走廊尽头传来整齐的脚步声。是声音警察！你屏住呼吸，贴紧墙壁。脚步声越来越近，然后在距离你几米的地方停了下来……",
    "一束手电筒的光扫过你藏身的角落。你赶紧蹲下。光柱在你头顶晃了晃，然后移开了。你松了一口气。",
    "你听到前方传来一声尖叫，然后是急促的脚步声和某种沉闷的撞击声。声音警察就在附近巡逻。"
]


def _time_of_day(day, phase):
    names = ["白天", "傍晚", "夜晚"]
    decibel_limits = ["60分贝（正常说话）", "30分贝（耳语级别）", "完全静默"]
    warnings = [
        "可以正常说话，但不要太吵。",
        "请降低音量。耳语是安全的。",
        "绝对安静。任何声音都会触发清理机制。"
    ]
    return {
        "name": names[phase],
        "limit": decibel_limits[phase],
        "warning": warnings[phase],
        "phase": phase
    }


def _show_status(day, phase, player, clock_parts, found_residents, alerted):
    td = _time_of_day(day, phase)
    print_line("─")
    print(f"  第 {day}/7 天 · {td['name']}  |  限制音量：{td['limit']}")
    print(f"  HP：{player.hp}/{player.max_hp}  |  白钞：{player.white_bills}")
    print(f"  钟塔零件：{clock_parts}/3  |  已找到居民：{found_residents}")
    if alerted:
        print(f"  ⚠️ 声音警察已经注意到你了！")
    print_line("─")


def _sound_check(player, alerted):
    td = _time_of_day(0, 0)
    roll = random.random()
    if alerted:
        if roll < 0.4:
            slow_print("\n你听到了远处传来的脚步声。声音警察正在靠近！")
            print_menu("", [
                ("1", "快速躲进旁边的建筑"),
                ("2", "屏住呼吸，保持不动"),
                ("3", "转身就跑")
            ])
            choice = get_choice()
            if choice == "1":
                slow_print("你闪身躲进一栋废弃的建筑里。脚步声从门外经过，没有发现你。")
                return False
            elif choice == "2":
                slow_print("你贴着墙壁一动不动。脚步声越来越近……然后停在了你面前。")
                if random.random() < 0.5:
                    slow_print("手电筒的光在你脸上晃了晃，然后移开了。好险！")
                    return False
                else:
                    slow_print("'找到你了。'一个冰冷的声音说。")
                    player.take_damage(20)
                    slow_print("你被声音警察打了一棍，失去了20点HP。")
                    return player.hp <= 0
            else:
                slow_print("你拼命地跑。脚步声在身后紧追不舍。")
                if random.random() < 0.3:
                    slow_print("你摔倒了！声音警察追上了你……")
                    player.take_damage(30)
                    slow_print("你被狠狠地教训了一顿，失去了30点HP。")
                    return player.hp <= 0
                else:
                    slow_print("你钻进一条小巷，七拐八绕后终于甩掉了追兵。")
                    return False
    return False


def _random_event():
    return random.choice(EVENTS_POOL)


def _night_choice(player, safe_house_today):
    slow_print("\n天色已经完全暗了下来。")
    slow_print("你必须在完全静默的状态下找到一个安全的地方过夜。")
    print_line()
    if safe_house_today:
        print(f"  你知道今天的安全屋在：{safe_house_today}")
        print_menu("", [
            ("1", "前往安全屋"),
            ("2", "冒险探索（可能会遇到声音警察）")
        ])
        choice = get_choice()
        if choice == "1":
            slow_print(f"你小心翼翼地来到{safe_house_today}，关好门窗。")
            slow_print("这里很安全。你终于可以喘口气了。")
            heal = 15
            player.heal(heal)
            slow_print(f"休息一晚，HP恢复 {heal} 点。")
            return False
        else:
            slow_print("你决定在夜色中探索……")
            if random.random() < 0.5:
                return _sound_check(player, True)
            else:
                slow_print("运气不错，你没有遇到声音警察。")
                slow_print("但你也没找到什么有用的东西。")
                return False
    else:
        slow_print("你不知道安全屋在哪里。今晚只能碰运气了。")
        print_menu("", [
            ("1", "找一栋看起来安全的建筑过夜"),
            ("2", "继续探索，找线索（高风险）")
        ])
        choice = get_choice()
        if choice == "1":
            safe = random.random() < 0.4
            if safe:
                slow_print("你找到了一栋废弃的民居。虽然破旧，但至少能遮风挡雨。")
                slow_print("你蜷缩在角落里，度过了不安的一夜。")
                heal = 10
                player.heal(heal)
                slow_print(f"HP恢复 {heal} 点。")
                return False
            else:
                slow_print("你刚躺下，就听到了门外的脚步声……")
                return _sound_check(player, True)
        else:
            return _sound_check(player, True)


def run_dungeon(player):
    print_header("副本载入", "分贝小镇 · Decibel Town")
    slow_print("\n列车缓缓停靠在一个迷雾笼罩的小站台旁。")
    slow_print("你走下列车，空气中弥漫着潮湿的雾气。")
    slow_print("前方是一个安静得不太正常的小镇。")
    slow_print("你的手机收到一条消息：")
    print_line()
    slow_print("  【副本任务】")
    slow_print("  任务一：在小镇生存7天 —— 遵守'分贝规则'")
    slow_print("  任务二：找到失踪的居民 —— 他们去了哪里？")
    slow_print("  任务三：修复钟塔 —— 让时间恢复正常")
    print_line()
    slow_print("在你踏入小镇之前，请记住：")
    slow_print("白天可以说话，傍晚只能耳语，夜晚——完全安静。")
    slow_print("违反规则的话……你会遇到'声音警察'。")
    wait_enter()

    clock_parts = 0
    found_residents = 0
    alerted = False
    safe_house_locations = [
        "旧教堂的地下室",
        "图书馆的阁楼",
        "废弃邮局的仓库",
        "钟塔旁边的守夜人小屋"
    ]
    safe_house_index = 0
    has_diary = False
    tower_unlocked = False
    days_explored = set()
    last_action = None

    for day in range(1, 8):
        for phase in range(3):
            if not player.is_alive():
                break

            if phase == 2:
                dead = _night_choice(player, safe_house_locations[safe_house_index % len(safe_house_locations)])
                safe_house_index += 1
                if dead:
                    break
                continue

            _show_status(day, phase, player, clock_parts, found_residents, alerted)

            if phase == 0:
                if day not in days_explored:
                    days_explored.add(day)
                    slow_print(f"\n清晨的阳光勉强穿过雾气照进小镇。新的一天开始了。")

            time_names = ["白天", "傍晚"]
            print(f"\n现在是{time_names[phase]}。{_time_of_day(day, phase)['warning']}")

            if day == 1 and phase == 0:
                slow_print("\n你站在小镇的入口处。雾气在脚边流动，像某种活物。")
                slow_print("前方的街道空无一人，只有一盏路灯在白天还亮着。")
                print_menu("去向选择", [
                    ("1", "沿主街向前走"),
                    ("2", "进入街边的杂货店"),
                    ("3", "走向那座高高的钟塔"),
                    ("4", "观察周围环境")
                ])
                choice = get_choice()
                if choice == "1":
                    slow_print("你沿着主街向前走。街道两旁是紧闭的店铺和民居。")
                    slow_print("你注意到所有门牌号都是反着挂的。")
                    if random.random() < 0.6:
                        event = _random_event()
                        _handle_event(event, player)
                elif choice == "2":
                    _general_store(player)
                elif choice == "3":
                    clock_parts = _clock_tower(player, clock_parts)
                else:
                    slow_print("你仔细观察周围。雾气中有一些模糊的影子在移动。")
                    slow_print("你不确定那些是人还是别的什么东西。")
            else:
                event = _random_event()
                _handle_event(event, player)

            if clock_parts >= 3 and not tower_unlocked:
                slow_print("\n你已经收集了三个钟塔零件！")
                slow_print("也许现在是时候去修复钟塔了。")
                tower_unlocked = True

            if tower_unlocked and clock_parts >= 3:
                print_menu("", [
                    ("1", "前往钟塔修复它"),
                    ("2", "继续探索")
                ])
                choice = get_choice()
                if choice == "1":
                    result = _fix_tower(player, day, phase)
                    if result == "win":
                        return _dungeon_end(player, clock_parts, found_residents, day, True)
                    elif result == "alert":
                        alerted = True

            if phase == 1 and random.random() < 0.3:
                alerted = True
                slow_print("\n⚠️ 你听到远处传来了哨声。声音警察似乎注意到了什么动静。")

        if not player.is_alive():
            break

    if player.is_alive():
        return _dungeon_end(player, clock_parts, found_residents, 7, False)
    else:
        return _dungeon_end(player, clock_parts, found_residents, 0, False)


def _handle_event(event, player):
    print_header(event["title"])
    slow_print(event["desc"])
    print_event_menu(event["choices"])
    choice = get_event_choice(event["choices"])
    if choice == "talk":
        slow_print(event["result_talk"])
    elif choice == "leave":
        slow_print(event["result_leave"])
    elif choice == "search":
        slow_print(event["result_search"])
    elif choice == "read":
        slow_print(event["result_read"])
    elif choice == "open":
        slow_print(event["result_open"])
    elif choice == "note":
        slow_print(event["result_note"])
    wait_enter()


def _general_store(player):
    print_header("杂货店")
    slow_print("你推开杂货店的玻璃门。门上的铃铛发出清脆的响声。")
    slow_print("你立刻僵住了——声音太大了！")
    slow_print("但什么都没发生。店里空无一人。")
    print_line()
    slow_print("货架上还有一些东西。看起来是小镇居民匆忙撤离时留下的。")
    print_menu("", [
        ("1", "搜索货架"),
        ("2", "检查柜台后面的房间"),
        ("0", "离开")
    ])
    choice = get_choice()
    if choice == "1":
        slow_print("你在货架上找到了几样东西：")
        found_item = random.choice(["一包饼干", "一瓶水", "一把手电筒", "一盒火柴"])
        slow_print(f"一包看起来没过期的{found_item}。")
        slow_print("你在柜台下面还发现了一个旧式助听器。")
        player.add_item({
            "id": "hearing_aid",
            "name": "旧式助听器",
            "level": "E",
            "effect": "可以增强听力，在夜晚更容易察觉声音警察",
            "price": 0,
            "note": "上一个主人的听力可能不太好——这玩意儿音量调到最大也只能听到蚊子扇翅膀的声音。"
        })
        slow_print("获得道具：旧式助听器")
    elif choice == "2":
        slow_print("柜台后面是一个小房间。墙上贴满了照片和剪报。")
        slow_print("照片上的人都在笑。看起来很正常。")
        slow_print("但所有照片里，钟塔的指针都是反的。")
        slow_print("你在抽屉里找到了一张纸条：'镇长说一切都会好的。镇长说谎了。'")
    wait_enter()


def _clock_tower(player, parts):
    print_header("钟塔")
    slow_print("你走近钟塔。塔很高，顶端的大钟指针确实是反着走的。")
    slow_print("钟塔的大门虚掩着。")
    print_menu("", [
        ("1", "推门进去"),
        ("2", "绕着钟塔走一圈"),
        ("0", "离开")
    ])
    choice = get_choice()
    if choice == "1":
        slow_print("你推开门，走了进去。塔内很暗，空气中弥漫着灰尘和机油的味道。")
        slow_print("在楼梯下面，你发现了一个生锈的齿轮——看起来是从某个机器上掉下来的。")
        slow_print("\n获得：钟塔零件（1/3）")
        wait_enter()
        return parts + 1
    elif choice == "2":
        slow_print("你绕着钟塔走了一圈。在塔基的背面，你发现墙上刻着一些文字：")
        slow_print("'当指针归位，声音回归。'")
        slow_print("'当钟声响起，沉默终结。'")
        slow_print("下面还有一行小字：'但别让警察听见。——老K'")
        wait_enter()
        return parts
    return parts


def _fix_tower(player, day, phase):
    print_header("修复钟塔")
    slow_print("你带着收集到的零件来到钟塔内部。")
    slow_print("登上旋转楼梯，你来到了钟塔的机械室。")
    slow_print("巨大的齿轮组在你的面前展开，其中几个齿轮已经脱落。")
    print_line()
    slow_print("你需要决定如何修复……")
    print_menu("", [
        ("1", "按照机械原理小心安装（安全但耗时）"),
        ("2", "用力把零件塞进去（快速但可能发出噪音）")
    ])
    choice = get_choice()
    if choice == "1":
        slow_print("你小心翼翼地将齿轮一一复位。")
        slow_print("钟塔的指针开始缓慢地倒转……然后恢复正常。")
        slow_print("一声洪亮的钟声响起——")
        slow_print("那是这个小镇三十年来第一次听到真正的声音。")
        slow_print("\n小镇的雾气开始消散。失踪的居民从各个角落出现。")
        slow_print("他们看起来都很困惑，但都还活着。")
        return "win"
    else:
        slow_print("你用蛮力把齿轮塞了进去。巨大的金属撞击声回荡在整个小镇！")
        slow_print("指针确实开始恢复正常了……但你听到了急促的脚步声。")
        slow_print("很多脚步声。正在向钟塔靠近。")
        slow_print("⚠️ 声音警察来了！")
        return "alert"


def _dungeon_end(player, clock_parts, found_residents, day, fixed_tower):
    print_header("副本结算", "分贝小镇")

    if not player.is_alive():
        slow_print("\n你在分贝小镇倒下了。")
        slow_print("意识模糊中，你感觉自己被拖进了某个黑暗的地方……")
        slow_print("\n评级：E级 — 死亡")
        score = 10
        reward = 0
    elif fixed_tower:
        slow_print("\n钟声响起，小镇恢复了正常。")
        slow_print("失踪的居民们从藏身之处走出来，困惑但安全。")
        slow_print("一个老人——你之前见过的那个——走过来拍了拍你的肩膀。")
        slow_print("'谢谢你。你是第一个修好钟塔的人。'")
        print_line()
        if clock_parts >= 3:
            slow_print("评级：S级 — 完美通关！")
            slow_print("你修复了钟塔，拯救了小镇，还发现了背后的秘密。")
            score = 300
            reward = 200
        else:
            slow_print("评级：A级 — 任务完成")
            slow_print("钟塔修好了，但还有一些谜题你没有解开。")
            score = 200
            reward = 150
    elif day >= 7:
        slow_print("\n七天的期限到了。")
        slow_print("你虽然没有完全解开小镇的秘密，但你活了下来。")
        slow_print("深渊列车在站台等你。你回头看了一眼这个安静的小镇。")
        print_line()
        if clock_parts >= 2:
            slow_print("评级：B级 — 部分探索")
            score = 100
            reward = 80
        else:
            slow_print("评级：C级 — 勉强生存")
            score = 60
            reward = 40
    else:
        slow_print(f"你在第{day}天就被小镇打败了……")
        slow_print("评级：D级 — 失败")
        score = 20
        reward = 10

    print_line()
    slow_print(f"  基础奖励：{reward} 白钞")
    slow_print(f"  额外积分：{score}")
    print_line()

    player.white_bills += reward
    player.dungeon_count += 1
    player.total_score += score

    evo_gain = score // 50
    if evo_gain > 0:
        player.evolution_rate = min(100, player.evolution_rate + evo_gain)
        slow_print(f"  进化率提升：+{evo_gain}%")

    if score >= 200:
        special_item = "evol_p0"
        item = get_item(special_item)
        if item:
            player.add_item(item)
            slow_print(f"  获得特殊奖励：{item['name']}")

    wait_enter()
    return "alive" if player.is_alive() else "dead"

# === main.py ===


def welcome():
    print("╔" + "═" * 53 + "╗")
    print(f"║{'深渊列车 · Abyss Express':^53}║")
    print(f"║{'':^53}║")
    print(f"║{'\"规则就是武器，选择定义你是谁\"':^53}║")
    print("╚" + "═" * 53 + "╝")
    print()
    slow_print("尊敬的乘客，欢迎登上深渊列车。")
    slow_print("在你踏上第一段旅程之前，请告诉我——")


def get_player_name():
    print()
    while True:
        name = input("  你的名字是：").strip()
        if name:
            return name
        print("  列车长皱了皱眉：'你总得有个名字吧？'")


def choose_profession():
    print_header("身份匹配")
    slow_print("检测到新人乘客，正在为您匹配初始身份……")
    print()
    slow_print("深渊列车为您提供以下五种初始身份：")
    print_line()

    for key, prof in PROFESSIONS.items():
        print(f"  {key}. {prof['name']}")
        print(f"     \"{prof['title']}\"")
        print()

    print_line()
    choice = get_choice("  请选择你的身份 (A/B/C/D/E)：", valid=["A", "B", "C", "D", "E"])
    prof = PROFESSIONS[choice]
    print_line()
    slow_print(f"你选择了【{prof['name']}】。")
    slow_print(f"\"{prof['title']}\"")
    print()
    slow_print(prof['desc'])
    print()
    slow_print(f"初始特性：{prof['trait']}")
    wait_enter()
    return choice


def dungeon_result_handler(result, player):
    if result == "alive":
        slow_print("\n你带着一身疲惫回到了列车上。")
        slow_print("列车缓缓启动，窗外的小镇逐渐消失在雾气中。")
    elif result == "dead":
        slow_print("\n你在副本中死亡……")
        slow_print("但死亡不是终点。深渊列车上的医疗舱将你从死亡边缘拉了回来。")
        slow_print("代价是你所有的白钞——它们被用来支付医疗费了。")
        player.white_bills = max(0, player.white_bills - 50)
        player.hp = player.max_hp // 2
        slow_print(f"你醒来时发现自己躺在医疗车厢里。HP恢复了一半，但钱包空了。")
    wait_enter()


def farewell(player):
    print_header("再见", "期待你的归来")
    slow_print(f"乘客 {player.name}，你已完成了 {player.dungeon_count} 次副本。")
    slow_print(f"总积分：{player.total_score}")
    slow_print(f"当前进化率：{player.evolution_rate}%")
    print_line()
    slow_print("深渊列车永远为你停靠。")
    slow_print("保重。")


def main():
    set_slow(True)
    welcome()
    name = get_player_name()
    prof_id = choose_profession()
    player = Player(name, prof_id)

    print_header("登车", f"欢迎你，{name}")
    slow_print(f"你登上了深渊列车，找到了自己的包厢。")
    slow_print("列车发出一声悠长的汽笛，缓缓驶入黑暗之中。")
    slow_print("窗外，熟悉的世界的灯光逐渐远去……")
    slow_print("新的旅程开始了。")
    wait_enter()

    while True:
        action = show_train_hub(player)
        if action == "quit":
            break
        elif action == "dungeon":
            print_header("副本选择")
            slow_print("列车长递给你一张车票：")
            print_line()
            print("  【分贝小镇】E级副本 — 适合新人")
            print()
            print_menu("", [
                ("1", "出发！前往分贝小镇"),
                ("0", "还没准备好，回去准备")
            ])
            choice = get_choice()
            if choice == "1":
                result = run_dungeon(player)
                dungeon_result_handler(result, player)

    farewell(player)


# [web] auto-start: game entry
set_slow(True)
main()
