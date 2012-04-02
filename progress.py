steps = [
    {
        "name": "start",
        "text": 'Welcome to Try Sed. This tutorial can be used as a first time introduction to sed or as a refresher course. To get started, enter "start" into the input box.',
        "entry": ["start"],
        "result": None,
    },
    {
        "name": "ls",
        "text": 'To get used to to the flow, we\'ll start off with a simple exercise. Use ls to examine your directory.',
        "entry": ["ls", "ls ."],
        "result": "bin\ndog\nnewfiles\npackers\ntrysed",
    },
    {
        "name": "cat",
        "text": 'See the file named dog? Cat that file.',
        "entry": ["cat dog", "cat ./dog"],
        "result": "cats and dogs until the end of time",
    },
]

class Progress(object):
    def __init__(self):
        self.step = 0

    def check_entry(self, entry):
        step = steps[self.step]
        return {
            "success": entry in step["entry"],
            "continue": step["result"] != None,
        }

    def check_result(self, result):
        step = steps[self.step]
        if step["result"]:
            return {
                "success": result in step["result"],
            }
        return {"success": False}

    def next_step(self):
        self.step += 1

    def get_dialog(self):
        return steps[self.step]["text"]

    def get_step(self):
        return (steps[self.step], self.step)
