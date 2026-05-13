from engine.display import print_header, print_line, slow_print, print_menu, get_choice, wait_enter, set_slow
from player.player import Player, PROFESSIONS
from train.train import show_train_hub
from dungeons.town import run_dungeon


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


if __name__ == "__main__":
    main()