import subprocess, shlex, json

def resolve_action(word, JSONFILE):
    for action, spec in JSONFILE["actions"].items():
        if word in spec["aliases"]:
            return action
    return None

def brain_chooses(text, JSONFILE):
    parts = text.lower().split()
    if len(parts) < 2:
        return

    action_word, target = parts[0], parts[1]
    action = resolve_action(action_word, JSONFILE)

    if not action:
        return

    cmd = JSONFILE["actions"][action]["command"].get(target)
    if not cmd:
        return
    try:
        subprocess.Popen(cmd)
    except FileNotFoundError:
        print("Command was unable to execute")
