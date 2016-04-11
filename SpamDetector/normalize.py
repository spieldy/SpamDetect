import csv
import sys
from math import sqrt

class Normalizer(object):

    def load_csv(self):
        file = "../../../../../datasets/spambase.csv"
        data_file = open(file, 'r')
        data = csv.reader(data_file)
        return data

    @staticmethod
    def min_data_col(data):
        mins = [float(sys.maxsize)]*58
        for k in range(58):
            for d in data:
                if(mins[k] > float(d[k])):
                    mins[k] = float(d[k])
        return mins

    @staticmethod
    def max_data_col(data):
        maxs = [float(-sys.maxsize-1)]*58
        for k in range(58):
            for d in data:
                if(maxs[k] < float(d[k])):
                    maxs[k] = float(d[k])
        return maxs

    def normalization(self, data_save, min_range, max_range):
        mins = self.min_data_col(data_save)
        maxs = self.max_data_col(data_save)

        for i in range(58):
            for nb in range(len(data_save)):
                data_save[nb][i] = ((float(data_save[nb][i])-mins[i])/(maxs[i]-mins[i]))*(max_range-min_range)+min_range

        return data_save

    def statistics(self, data, nb_col):
        stats = []
        stats_spam = [[] for x in range(4)]
        stats_nospam = [[] for x in range(4)]
        data_spam = []
        data_nospam = []
        col_spam = 57
        nb_data = 0.0
        nb_data_spam = 0.0
        nb_data_nospam = 0.0
        min_spam = [99999]*nb_col
        min_nospam = [99999]*nb_col
        max_spam = [0]*nb_col
        max_nospam = [0]*nb_col
        avg_spam = [0]*nb_col
        avg_nospam = [0]*nb_col
        std_spam = [0]*nb_col
        std_nospam = [0]*nb_col

        for d in data:
            nb_data += 1
            if(float(d[col_spam]) == 1.0):
                data_spam.append(d)
            else:
                data_nospam.append(d)

        #calcul du min et max
        for d in data_spam:
            nb_data_spam += 1
            for i in range(nb_col):
                if(min_spam[i] > float(d[i])):
                    min_spam[i] = float(d[i])
                if(max_spam[i] < float(d[i])):
                    max_spam[i] = float(d[i])
                avg_spam[i] += float(d[i])

        for d in data_nospam:
            nb_data_nospam += 1
            for i in range(nb_col):
                if(min_nospam[i] > float(d[i])):
                    min_nospam[i] = float(d[i])
                if(max_nospam[i] < float(d[i])):
                    max_nospam[i] = float(d[i])
                avg_nospam[i] += float(d[i])

        #calcul de la moyenne
        for i in range(nb_col):
            avg_spam[i] = avg_spam[i]/nb_data
            avg_nospam[i] = avg_nospam[i]/nb_data

        #calcul de l'ecart-type
        for d in data_spam:
            for i in range(nb_col):
                std_spam[i] += (float(d[i])-avg_spam[i])**2

        for d in data_nospam:
            for i in range(nb_col):
                std_nospam[i] += (float(d[i])-avg_nospam[i])**2

        for i in range(nb_col):
            std_spam[i] = sqrt((1/nb_data)*std_spam[i])
            std_nospam[i] = sqrt((1/nb_data)*std_nospam[i])

        for i in range(nb_col):
            stats_spam[0].append(self.truncate(min_spam[i], 5))
            stats_spam[1].append(self.truncate(max_spam[i], 5))
            stats_spam[2].append(self.truncate(avg_spam[i], 5))
            stats_spam[3].append(self.truncate(std_spam[i], 5))

            stats_nospam[0].append(self.truncate(min_nospam[i], 5))
            stats_nospam[1].append(self.truncate(max_nospam[i], 5))
            stats_nospam[2].append(self.truncate(avg_nospam[i], 5))
            stats_nospam[3].append(self.truncate(std_nospam[i], 5))

        stats.append(stats_spam)
        stats.append(stats_nospam)

        return stats

    def truncate(self, f, n):
        #tronque un float f a n decimales sans arrondir
        s = '%.5f' % f
        i, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])

    def __init__(self):
        pass

if __name__ == '__main__':
    norm = Normalizer()
    data_save = []
    data = norm.load_csv()

    for line in data:
        try:
            data_save.append(line)
        except IndexError:
            pass

    data_normalized = norm.normalization(data_save, 0.0, 1.0)
    stats = norm.statistics(data_normalized, 58)

    '''
    print("SPAM")
    for s in stats[0]:
        print s
    print("NO SPAM")
    for s in stats[1]:
        print s
    '''