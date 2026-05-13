from engine.display import print_header, print_menu, print_line, slow_print, wait_enter, get_choice
from data.items import ITEMS, get_item, describe_item


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