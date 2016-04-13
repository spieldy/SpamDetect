from Carbon.Windows import false
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import DocumentForm
from normalize import Normalizer
from kmeans import KMeanClusterer
import os


# Create your views here.
def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['docfile'], request.FILES['docfile'].name)
            # Redirect to the document list after POST
            norm = Normalizer()
            data_save = []
            workpath = os.path.dirname(os.path.abspath(__file__)) #Returns the Path your .py file is in
            data = norm.load_csv(os.path.join(workpath, 'dataset/'+request.FILES['docfile'].name))

            for line in data:
                try:
                    data_save.append(line)
                except IndexError:
                    pass

            data_normalized = norm.normalization(data_save, 0.0, 1.0)
            stats = norm.statistics(data_normalized, 58)

            spam = []
            for i in range(0, 58):
                line = []
                line.append(i)
                for j in range(0, 4):
                    line.append(stats[0][j][i])
                spam.append(line)

            no_spam = []
            for i in range(0, 58):
                line = []
                line.append(i)
                for j in range(0, 4):
                    line.append(stats[1][j][i])
                no_spam.append(line)

            new_stats = []
            for i in range(0, 58):
                line = []
                line.append(i)
                for j in range(0, 4):
                    line.append(stats[0][j][i])
                for j in range(0, 4):
                    line.append(stats[1][j][i])
                new_stats.append(line)

            return render(request, 'stats.html', {'stats': new_stats,'spam': stats[0], 'no_spam': no_spam })
    else:
        form = DocumentForm() # A empty, unbound form
        return render(request, 'index.html', {'form': form})

def kmeans(request):
    k = 2
    workpath = os.path.dirname(os.path.abspath(__file__)) #Returns the Path your .py file is in
    datafile = os.path.join(workpath, 'dataset/spambase.data.txt')
    champs = [25, 15]
    kMeanClusterer = KMeanClusterer(k, datafile, champs)
    kMeanClusterer.assignement()

    centroids = []
    clusters = []
    for i in range(k):
        centroids.append(kMeanClusterer.getCluster(i).getCentroid())
    for i in range(k):
        clusters.append(kMeanClusterer.getCluster(i).getPoints())

    return render(request, 'kmeans.html', {'k': len(champs), 'centroids': centroids, 'clusters': clusters})


def handle_uploaded_file(f, file_name):
    workpath = os.path.dirname(os.path.abspath(__file__)) #Returns the Path your .py file is in
    destination = open(os.path.join(workpath, 'dataset/'+file_name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()