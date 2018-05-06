from stemmingPT.stemmingPT import *

from app.repository.repository import Repository
from random import randint
from singleton import repo

class FunnyBot(object):
    def __init__(self):

        self.keys = ["vide", 'engraad', 'novidades',
                     'mem', "imagens", "divertidas",
                     "fot", "piad"]
        self.maxmemesent = 3

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

            # WITH LIMIT 10 orderby haha
            memes = repo.get_memes()

            best = float("-inf")
            thememe = None
            weights = [1.0, 2.0, 3.0, 4.0, -1.0, -2.0]

            for meme in memes:
                total = [meme.like, meme.love, meme.wow, meme.haha,
                         meme.sad, meme.angry]

                tmp = sum([a * b for a, b in zip(total, weights)]) / sum(total)

                if tmp > best and meme.nsent < self.maxmemesent:
                    best = tmp
                    thememe = meme

            repo.update_count_meme(table='posts', set='nsent={}'.format(thememe.nsent + 1), where='id={}'.format(thememe.id))
            return {"type": mtype, "link": thememe.permalink_url}

        return {"type": None, "link": None}

