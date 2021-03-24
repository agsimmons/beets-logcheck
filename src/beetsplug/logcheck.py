from collections import namedtuple
from pathlib import Path

from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from heybrochecklog.score import score_log


LogFile = namedtuple("LogFile", ["path", "data"])


def logcheck(lib, opts, args):
    for album in lib.albums(args):
        # TODO: Handle path decoding correctly
        album_path = Path(album.item_dir().decode("utf-8"))

        logs = []
        for log_file in album_path.glob("**/*.log"):
            try:
                log = score_log(log_file)
                if not log["unrecognized"]:
                    logs.append(LogFile(log_file, log))
            except FileNotFoundError:
                pass

        if logs:
            # TODO: Replace print statements with best practice
            # TODO: Support colored output
            print(album)
            for log in logs:
                relative_path = log.path.relative_to(album_path)
                print(f"  Log: {relative_path}")
                print(f"    Score: {log.data['score']}")

                if log.data["deductions"]:
                    print("    Deductions:")
                    for deduction in log.data["deductions"]:
                        print(f"      >>  {deduction[0]}")

            print()


logcheck_command = Subcommand("logcheck", help="Checks rip logs")
logcheck_command.func = logcheck


class LogCheckPlugin(BeetsPlugin):
    def commands(self):
        return [logcheck_command]
