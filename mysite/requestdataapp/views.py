from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse




def handle_file_upload(request: HttpRequest) -> HttpResponse:
    context = {
        'size': 0,
        'error_size_file': False,
    }
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        size = myfile.size
        context['size'] = size
        if size > 1048576:
            context['error_size_file'] = True
        else:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('Saved file', filename)

    return render(request, 'requestdataapp/file-upload.html', context=context)


