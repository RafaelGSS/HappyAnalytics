from stemmingPT.stemmingPT import *
from random import randint
from singleton_repo import repo

class FunnyBot(object):
    def __init__(self):

        self.keys = ["vide", 'engraad', 'novidades',
                     'mem', "imagens", "divertidas",
                     "fot", "piad"]
        self.maxmemesent = 5

    def analyze_response(self, message):
        msg = message.lower().split(" ")
        msg = [suffixRemoval(replaceTwoOrMore(cleanText(mi)))
               for mi in msg]

        msg = [mi.lower() for mi in msg if mi is not None and mi in self.keys]
        if msg:
            ptypes = ["video", "photo", "link"]

            mtype = ptypes[randint(0, 2)]

            if 'imagens' in msg or "fot" in msg:
                mtype = "photo"

            if 'vide' in msg:
                mtype = "video"

            memes = repo.get_memes(args_gen='WHERE type=\'{}\' ORDER BY haha DESC limit 10'.format(mtype))

            best = float("-inf")
            thememe = None
            weights = [1.0, 2.0, 3.0, 4.0, -1.0, -2.0]

            for meme in memes:
                total = [meme['like'], meme['love'], meme['wow'], meme['haha'],
                         meme['sad'], meme['angry']]

                tmp = sum([a * b for a, b in zip(total, weights)]) / sum(total)

                if tmp > best and meme['counter'] < self.maxmemesent:
                    best = tmp
                    thememe = meme

            repo.update_count_meme(set=int(thememe['counter']) + 1, id=thememe['id'])
            return {"type": mtype, "link": thememe['permalink_url'], "image":  thememe['full_picture']}

        return {"type": None, "link": None, "image": None}

