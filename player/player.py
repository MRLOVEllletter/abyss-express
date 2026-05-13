from engine.display import print_line, slow_print

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