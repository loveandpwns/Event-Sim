# _                                _                         
#| |event_loader.py               | |                        
#| | _____   _____  __ _ _ __   __| |_ ____      ___ __  ___ 
#| |/ _ \ \ / / _ \/ _` | '_ \ / _` | '_ \ \ /\ / / '_ \/ __|
#| | (_) \ V /  __/ (_| | | | | (_| | |_) \ V  V /| | | \__ \
#|_|\___/ \_/ \___|\__,_|_| |_|\__,_| .__/ \_/\_/ |_| |_|___/
#                                   | |                      
#                                   |_|     
import os
import re


class EventFileError(Exception):
    def __init__(self, filepath, line_no, message, bad_line):
        self.filepath = filepath
        self.line_no = line_no
        self.message = message
        self.bad_line = bad_line
        super().__init__(f"{filepath}:{line_no} {message}: {bad_line}")


class EventLoader:
    def __init__(self):
        self.pools = {
            "bloodbath_normal": [],
            "bloodbath_fatal": [],
            "day_normal": [],
            "day_fatal": [],
            "night_normal": [],
            "night_fatal": [],
        }

    def clear(self):
        for k in self.pools:
            self.pools[k] = []

    def load_files(self, filepaths):
        self.clear()
        for path in filepaths:
            self.load_file(path)

    def load_file(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n\r") for line in f]

        if not lines:
            raise EventFileError(filepath, 1, "Empty file", "")

        raw_header = lines[0].strip()
        normalized = re.sub(r"\s+", " ", raw_header).lower()

        fatal = False
        if normalized.startswith("fatal "):
            fatal = True
            base = normalized.replace("fatal ", "", 1)
        elif " fatal " in normalized:
            fatal = True
            base = normalized.replace(" fatal ", " ", 1)
        else:
            base = normalized

        if base not in ("bloodbath events", "day events", "night events"):
            raise EventFileError(filepath, 1, "Invalid header", raw_header)

        phase = base.split()[0]
        pool_key = f"{phase}_{'fatal' if fatal else 'normal'}"

        idx = 1
        while idx < len(lines):
            if not lines[idx].strip():
                idx += 1
                continue
            block, consumed = self.parse_block(filepath, lines, idx, phase, fatal)
            self.pools[pool_key].append(block)
            idx += consumed

    def parse_block(self, filepath, lines, start, phase, fatal):
        def safe_line(n):
            if start + n >= len(lines):
                raise EventFileError(filepath, start + n + 1, "Unexpected EOF", "")
            return lines[start + n]

        line_requires = safe_line(0)
        if not line_requires.lower().startswith("# requires:"):
            raise EventFileError(filepath, start + 1, "Expected '# requires:'", line_requires)
        requires_flags = self.parse_flags(line_requires)

        line_sets = safe_line(1)
        if not line_sets.lower().startswith("# sets:"):
            raise EventFileError(filepath, start + 2, "Expected '# sets:'", line_sets)
        sets_flags = self.parse_flags(line_sets, allow_empty=True)

        text_line = safe_line(2).strip()
        if not text_line:
            raise EventFileError(filepath, start + 3, "Empty event text", text_line)

        players_line = safe_line(3).strip()
        if not players_line.isdigit():
            raise EventFileError(filepath, start + 4, "Invalid players_required", players_line)
        players_req = int(players_line)

        killers, victims, dead_req = [], [], None
        consumed = 4

        if fatal:
            killers_line = safe_line(4).strip()
            victims_line = safe_line(5).strip()

            killers = self.parse_idx_line(killers_line, players_req, filepath, start + 5)
            victims = self.parse_idx_line(victims_line, players_req, filepath, start + 6)

            if not victims:
                raise EventFileError(filepath, start + 6, "Fatal event must have at least 1 victim", victims_line)

            consumed = 6
        else:
            d_line = safe_line(4).strip()
            if not d_line.startswith("D"):
                raise EventFileError(filepath, start + 5, "Expected D line", d_line)
            dead_req = self.parse_dead(d_line, filepath, start + 5)
            consumed = 5

        event = {
            "id": f"{phase}_{start+1}",
            "phase": phase,
            "fatal": fatal,
            "text": text_line,
            "players_required": players_req,
            "flags": {
                "requires": requires_flags,
                "sets": sets_flags,
            },
            "origin": {
                "file": os.path.basename(filepath),
                "line": start + 1,
            },
        }

        if fatal:
            event["killers"] = killers
            event["victims"] = victims
        else:
            event["dead_required"] = dead_req

        return event, consumed

    def parse_flags(self, line, allow_empty=False):
        parts = line.split(":", 1)
        if len(parts) != 2:
            return {"all": [], "targeted": {}, "dead_targeted": {}}
        content = parts[1].strip()
        if not content:
            return {"all": [], "targeted": {}, "dead_targeted": {}}
        
        tokens = content.lower().split()
        all_flags = []
        targeted = {}
        dead_targeted = {}
        
        for token in tokens:
            if ':' in token:
                flag_name, indices_str = token.split(':', 1)
                
                if indices_str.startswith('d'):
                    dead_idx = int(indices_str[1:])
                    if dead_idx not in dead_targeted:
                        dead_targeted[dead_idx] = []
                    dead_targeted[dead_idx].append(flag_name)
                else:
                    indices = [int(x.strip()) for x in indices_str.split(',')]
                    for idx in indices:
                        if idx not in targeted:
                            targeted[idx] = []
                        targeted[idx].append(flag_name)
            else:
                all_flags.append(token)
        
        return {"all": all_flags, "targeted": targeted, "dead_targeted": dead_targeted}

    def parse_idx_line(self, raw, max_index, filepath, line_no):
        if raw == "0":
            return []
        tokens = raw.split()
        result = []
        for tok in tokens:
            if not tok.isdigit():
                raise EventFileError(filepath, line_no, "Invalid index token", tok)
            val = int(tok)
            if val < 1 or val > max_index:
                raise EventFileError(filepath, line_no, "Index out of range", tok)
            result.append(val)
        return result

    def parse_dead(self, raw, filepath, line_no):
        tokens = raw.split()
        if tokens[0] != "D":
            raise EventFileError(filepath, line_no, "D line must start with 'D'", raw)
        if len(tokens) == 1:
            return 0
        if len(tokens) == 2 and tokens[1].isdigit():
            return int(tokens[1])
        raise EventFileError(filepath, line_no, "Invalid D line format", raw)


if __name__ == "__main__":
    loader = EventLoader()
    try:
        loader.load_files(["day_events.txt", "night_events.txt", "bloodbath_events.txt"])
        print("Loaded pools:")
        for key, events in loader.pools.items():
            print(f"{key}: {len(events)} events")
    except EventFileError as e:
        print("Error loading events:", e)
