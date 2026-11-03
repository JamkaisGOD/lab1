import os
import sys

PDDL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pddl")


# ---------- Blocksworld үйлдлүүд (Алхам 2-ын хүснэгт) ----------

def pick_up(x):
    pre = {('clear', x), ('ontable', x), ('handempty',)}
    add = {('holding', x)}
    delete = {('ontable', x), ('clear', x), ('handempty',)}
    return ('pick-up', x), pre, add, delete


def put_down(x):
    pre = {('holding', x)}
    add = {('ontable', x), ('clear', x), ('handempty',)}
    delete = {('holding', x)}
    return ('put-down', x), pre, add, delete


def stack(x, y):
    pre = {('holding', x), ('clear', y)}
    add = {('on', x, y), ('clear', x), ('handempty',)}
    delete = {('holding', x), ('clear', y)}
    return ('stack', x, y), pre, add, delete


def unstack(x, y):
    pre = {('on', x, y), ('clear', x), ('handempty',)}
    add = {('holding', x), ('clear', y)}
    delete = {('on', x, y), ('clear', x), ('handempty',)}
    return ('unstack', x, y), pre, add, delete


# ---------- Logistics үйлдлүүд (Алхам 8-ын хүснэгт) ----------

def load(pkg, veh, loc):
    pre = {('at', veh, loc), ('at', pkg, loc)}
    add = {('in', pkg, veh)}
    delete = {('at', pkg, loc)}
    return pre, add, delete


def unload(pkg, veh, loc):
    pre = {('at', veh, loc), ('in', pkg, veh)}
    add = {('at', pkg, loc)}
    delete = {('in', pkg, veh)}
    return pre, add, delete


def drive_truck(truck, frm, to, c):
    pre = {('at', truck, frm), ('in-city', frm, c), ('in-city', to, c)}
    add = {('at', truck, to)}
    delete = {('at', truck, frm)}
    return ('drive-truck', truck, frm, to, c), pre, add, delete


def fly_airplane(plane, frm, to):
    pre = {('at', plane, frm)}
    add = {('at', plane, to)}
    delete = {('at', plane, frm)}
    return ('fly-airplane', plane, frm, to), pre, add, delete


# ---------- Hanoi (нэмэлт) ----------

def move(d, frm, to):
    pre = {('on', d, frm), ('clear', d), ('clear', to), ('smaller', to, d)}
    add = {('on', d, to), ('clear', frm)}
    delete = {('on', d, frm), ('clear', to)}
    return ('move', d, frm, to), pre, add, delete


ACTIONS = {
    'pick-up': pick_up,
    'put-down': put_down,
    'stack': stack,
    'unstack': unstack,
    'drive-truck': drive_truck,
    'fly-airplane': fly_airplane,
    'move': move,
}


def make_action(name, args):
    if name in ('load-truck', 'load-airplane'):
        return (name, *args), *load(*args)
    if name in ('unload-truck', 'unload-airplane'):
        return (name, *args), *unload(*args)
    if name not in ACTIONS:
        raise ValueError(f"Тодорхойгүй үйлдэл: {name}")
    return ACTIONS[name](*args)


def applicable(state, pre):
    return pre <= state


def apply(state, add, delete):
    # эхлээд хас, дараа нь нэм
    return frozenset((state - delete) | add)


def parse_plan(path):
    plan = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            parts = line.strip('()').lower().split()
            plan.append((parts[0], parts[1:]))
    return plan


# ---------- problem файлаас init, goal унших ----------

def tokenize(text):
    lines = [l.split(';')[0] for l in text.splitlines()]
    text = ' '.join(lines).replace('(', ' ( ').replace(')', ' ) ')
    return text.lower().split()


def read_tree(tokens):
    tok = tokens.pop(0)
    if tok == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(read_tree(tokens))
        tokens.pop(0)
        return lst
    return tok


def parse_problem(path):
    with open(path, encoding='utf-8') as f:
        tree = read_tree(tokenize(f.read()))
    init, goal = set(), set()
    for part in tree:
        if isinstance(part, list) and part[0] == ':init':
            init = {tuple(fact) for fact in part[1:]}
        if isinstance(part, list) and part[0] == ':goal':
            g = part[1]
            facts = g[1:] if g[0] == 'and' else [g]
            goal = {tuple(fact) for fact in facts}
    return frozenset(init), frozenset(goal)


def check(init, goal, plan, verbose=False):
    state = frozenset(init)
    for i, (name, args) in enumerate(plan):
        act, pre, add, delete = make_action(name, args)
        if not applicable(state, pre):
            missing = sorted(pre - state)
            print(f"  БУРУУ: {i}-р алхамд ({' '.join(act)}) precondition биелээгүй. Дутуу: {missing}")
            return False
        state = apply(state, add, delete)
        if verbose:
            print(f"  {i}: ({' '.join(act)})")
    if not goal <= state:
        print(f"  БУРУУ: зорилго биелээгүй. Дутуу: {sorted(goal - state)}")
        return False
    print(f"  ЗӨВ: {len(plan)} алхамтай төлөвлөгөө зорилгод хүрлээ")
    return True


def check_files(problem, soln, verbose=False):
    init, goal = parse_problem(os.path.join(PDDL_DIR, problem))
    plan = parse_plan(os.path.join(PDDL_DIR, soln))
    print(f"{problem} + {soln}")
    return check(init, goal, plan, verbose)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')  # Windows консолд кирилл хэвлэх

    if len(sys.argv) == 3:
        check_files(sys.argv[1], sys.argv[2], verbose=True)
        raise SystemExit

    print("===== pyperplan-ын төлөвлөгөөнүүд =====")
    for p in ['p01', 'p02', 'p03', 'p04', 'lp01', 'lp02', 'lp03', 'hanoi3', 'hanoi4']:
        if os.path.exists(os.path.join(PDDL_DIR, p + '.pddl.soln')):
            check_files(p + '.pddl', p + '.pddl.soln')

    print("\n===== Гараар өгсөн буруу төлөвлөгөө (p01) =====")
    init, goal = parse_problem(os.path.join(PDDL_DIR, 'p01.pddl'))
    print("(stack a b) ганцаараа:")
    check(init, goal, [('stack', ['a', 'b'])])
    print("(pick-up a), (pick-up b):")
    check(init, goal, [('pick-up', ['a']), ('pick-up', ['b'])])

    print("\n===== Алхам 7: эвдэрсэн domain-ы төлөвлөгөөг жинхэнэ дүрмээр шалгах =====")
    for d, p in [('broken1', 'p01'), ('broken2', 'p02'), ('broken4', 'p03')]:
        soln = f"{d}_{p}.soln"
        if os.path.exists(os.path.join(PDDL_DIR, soln)):
            check_files(p + '.pddl', soln)
