import csv
from collections import Counter
from operator import itemgetter

import matplotlib.pyplot as plt

N_VOTERS_RO = 8954959
N_VOTERS_SR = 369775
N_VOTERS_ALL = N_VOTERS_RO + N_VOTERS_SR
PARTIES = ['PSD', 'USR-PLUS', 'PRO Romania', 'UDMR', 'PNL', 'ALDE', 'PRODEMO', 'PMP', 'PSR', 'PSDI', 'PRU', 'UNPRR',
           'BUN',
           'Gregoriana Tudoran', 'George Simion', 'Peter Costea']

GRAPH_COLORS = ['#27427d', '#60468c', '#934690', '#c24587', '#e74b74', '#fe6159', '#ff8138', '#ffa600']


def get_votes(csv_path):
    votes = Counter()
    with open(csv_path, encoding='UTF-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        header = reader.__next__()
        start_col = header.index('g1')
        for row in reader:
            votes += Counter({p: int(row[start_col + i]) for i, p in enumerate(PARTIES)})
    return votes


def save_chart(votes, path):
    sorted_votes = votes.most_common()
    sorted_votes[7:] = [('Irelevant', sum(map(itemgetter(1), sorted_votes[7:])))]

    x, y = list(map(itemgetter(1), sorted_votes)), list(map(itemgetter(0), sorted_votes))
    fig1, ax1 = plt.subplots()
    patches, texts, auto_texts = ax1.pie(x, labels=y, counterclock=False, colors=GRAPH_COLORS, autopct='%1.2f%%',
                                         startangle=90)

    for text in auto_texts:
        text.set_color('#e2e2e2')
        text.set_fontsize(8)

    ax1.axis('equal')
    plt.tight_layout()
    plt.savefig(path, dpi=500)


# Read and process data
votes_ro = get_votes('pv_RO_EUP_PROV.csv')
votes_sr = get_votes('pv_SR_EUP_PROV.csv')
votes_all = votes_ro + votes_sr

threshold_parties = {p: c for p, c in votes_all.items() if c / N_VOTERS_ALL > 0.05}
threshold_sum = sum(threshold_parties.values())
party_meps = {p: round(c / threshold_sum * 33) for p, c in threshold_parties.items()}

# Print stats
total_votes = sum(votes_all.values())
for party, count in votes_all.most_common(10):
    print(f'{count / total_votes * 100:5.2f}% | {party_meps.get(party, 0):2} | {party.ljust(18)} | {count:,}')

print(f'\n'
      f'{total_votes:,} / {N_VOTERS_ALL:,} ({total_votes / N_VOTERS_ALL * 100:.2f}%)\n'
      f'{N_VOTERS_ALL - total_votes:,} votes left\n')

# Save charts
save_chart(votes_ro, 'chart_ro.png')
save_chart(votes_sr, 'chart_sr.png')
save_chart(votes_all, 'chart_total.png')
