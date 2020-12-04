
def handle_uploaded_file(file, folder, filename):
    print(file.chunks())
    with open('Damageapp/static/upload/predict/' + folder + '/a/' + filename, 'wb+') as destination:
        for chunk in file.chunks():            
            destination.write(chunk)
