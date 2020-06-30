from main.models import Libro,Puntuacion
import csv
import pandas as pd


def populateDB():
    num_libros = 0
    num_puntuaciones = 0


    Libro.objects.all().delete()
    Puntuacion.objects.all().delete()


    libros = []
    print('Empezando a cargar libros...')
    with open('./BX-Book-dataset/books.csv') as File:
        reader = csv.reader(File)
        for row in reader:
            a = ""
            for i in range(len(row)):
                a = a + str(row[i])
            row = a
            if(row != 'ï»¿ISBN;title;author;year;publisher'):
                row = row.replace("amp;","amp:").split(";")
                if(row[3] == "Unknown"):
                    row[3] = None
                if('"' in row[2] and "amp" not in row[2] and '""' not in row[2]):
                    row[2] = str(row[2]) + str(row[3])
                    row[3] = row[4]
                    row[4] = row[5]
                    row = row[:5]

                if(len(row) == 6):
                    row[2] = str(row[2]) + str(row[3])
                    row[3] = row[4]
                    row[4] = row[5]
                    row = row[:5]
                if(len(row) == 7):
                    row[2] = str(row[2]) + str(row[3]) + str(row[4])
                    row[3] = row[5]
                    row[4] = row[6]
                    row = row[:5]
                libros.append(row)
                libro_obj, creado = Libro.objects.get_or_create(ISBN=row[0], titulo=row[1],autor=row[2], editor=row[4], anyoPublicacion=row[3])
                if(creado):
                    num_libros += 1


        print('Numero de libros cargados: {}'.format(num_libros))

    puntuaciones= []
    print('Empezando a cargar puntuaciones...')
    with open('./BX-Book-dataset/ratings.csv') as File:
        reader = csv.reader(File)
        for row in reader:
            if (row[0] != 'ï»¿User-ID;ISBN;Book-Rating'):
                row = row[0].split(";")
                puntuacion_obj, creado = Puntuacion.objects.get_or_create(usuario=int(row[0]), ISBN=int(row[1]),puntuacion=int(row[2]))
                if(creado):
                    num_puntuaciones += 1

        print('Numero de puntuaciones cargadas: {}'.format(num_puntuaciones))
    print('Base de datos cargada completamente')


if __name__ == '__main__':
    populateDB()