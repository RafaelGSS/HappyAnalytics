import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, plot, iplot
import cufflinks as cf
from scipy.stats import pearsonr

class Analytic(object):
    def __init__(self):
        cf.go_offline()

    def analyze_report_humor(self, data, image_name):
        content = pd.DataFrame(list(data), columns=['id', 'user_id', 'user_name', 'note_humor', 'description', 'date'])
        fig = content.iplot(kind='scatter', x='date', y='note_humor', categories='user_name', mode=['lines', 'markers'],
                            text='description', asFigure=True)
        path = plot(fig, filename=image_name)

        return image_name

    def analyze_correlation(self, data_, image_name):
        data = pd.DataFrame(list(data_), columns=['id', 'user_id', 'user_name', 'note_humor', 'description', 'date'])
        print(data)
        user_ids = np.unique(data["user_id"])
        user_names = np.unique(data["user_name"])
        print(user_ids)
        n = user_ids.size

        x = np.zeros((n,n))

        dict_tst = {}
        test = []
        for i in range(n-1):
            for k in range(i + 1, n):
                idk = k
                if k >= n:
                    idk = k - 1
                posusr1 = np.where(data["user_id"] == user_ids[i])
                posusr2 = np.where(data["user_id"] == user_ids[idk])
                print(user_ids[i], user_ids[idk])
                tmp = pearsonr(data.loc[posusr1]["note_humor"].values, data.loc[posusr2]["note_humor"].values)[0]
                x[i][idk] = tmp
            x[i] = np.array(np.nan_to_num(x[i]))
            maxcorr = x[i].max()
            mincorr = x[i].min()
            dict_tst[user_ids[i]] = {'maxcorr': {"user_name": user_names[np.where(np.array(x[i]) == maxcorr)[0]][0],
                                                 "corr": maxcorr},
                                     'mincorr': {"user_name": user_names[np.where(np.array(x[i]) == mincorr)[0]][0],
                                                 "corr": mincorr}
                                     }
            test.append({'maxcorr': dict_tst[user_ids[i]]['maxcorr']['corr'],
                         'usuariomax': dict_tst[user_ids[i]]['maxcorr']['user_name'],
                         'mincorr': dict_tst[user_ids[i]]['mincorr']['corr'],
                         'usuariomin': dict_tst[user_ids[i]]['mincorr']['user_name']})
        print(test)
        df = pd.DataFrame(test, index=user_ids)
        fig = df.iplot(kind='scatter', y=['maxcorr', 'mincorr'], x=['usuariomax', 'usuariomin'], mode=['list', 'markers'],
                           asFigure=True)

        path = plot(fig, filename=image_name)

        return image_name