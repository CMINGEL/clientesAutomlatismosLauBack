from django.shortcuts import HttpResponse
from .models import cliente, ejecutivo, Archivo, Servicio
from .serializers import dbClientesSerializer, dbEjecutivosSerializer, UserSerializer, ServiciosSerializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
#Manejo de archivos
from django.core.files.storage import FileSystemStorage
import csv


class ejecutivos(APIView):
    def get(self, request):
        try:
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            if response:
                print('Autenticado')
                user, token = response
                print(user)
                print(token)
            datos = ejecutivo.objects.all()
            serializer = dbEjecutivosSerializer(datos, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 
            #else: 
                #return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ejecutivo.DoesNotExist:
            raise Http404
    def post(self, request):
        serializer = dbEjecutivosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, pk):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if(response):
            user, token = response
            if(user.is_superuser):
                try:
                    q = ejecutivo.objects.get(pk=pk)
                    serializer = dbEjecutivosSerializer(q, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    return Response({"message":"success", "Actualizado":q.nombre},status=status.HTTP_202_ACCEPTED)
                except:
                    return Response({"message":"wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
    def delete(self, request, pk):
        try:
            q = ejecutivo.objects.get(pk=pk)
            q.delete()
            return Response({"message":"success", "Eliminado":q.nombre},status=status.HTTP_202_ACCEPTED)
        except:
            raise Http404

class clientes(APIView):
    def get(self, request):
        try:
            datos = cliente.objects.all()
            serializer = dbClientesSerializer(datos, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 
        except cliente.DoesNotExist:
            raise Http404

    def post(self, request):
        try:
            serializer = dbClientesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            setServicios(serializer.data['id'], request.data.get('servicios'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            raise Http404

    def patch(self, request, pk):
        #TODO if pk si existe
        #JWT_authenticator = JWTAuthentication()
        #response = JWT_authenticator.authenticate(request)
        #print(response)
        #if(response):
        #     user, token = response
            # if(user.is_superuser):
        setServicios(pk, request.data.get('servicios'))
        try:
            q = cliente.objects.get(pk=pk)
            serializer = dbClientesSerializer(q, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print("Actualizado cliente: " + q.nombre)
            return Response({"message":"success", "Actualizado":q.nombre},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"message":"wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        try:
            q = cliente.objects.get(pk=pk)
            q.delete()
            return Response({"message":"success"},status=status.HTTP_202_ACCEPTED)
        except:
             raise Http404

class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class simple_upload(APIView):

    def get(self, request, pk):
        Archivos = Archivo.objects.all().filter(cliente_id = pk).values()
        return Response(Archivos)

    def post(self, request):
        if (request.FILES['myfile']):

            myfile = request.FILES['myfile']
            clienteID = request.POST.get("cliente_id")
        
 
            fs = FileSystemStorage()
            instance = Archivo(cliente_id=clienteID, image_content = myfile)
            instance.save()
            
            #filename = fs.save('./'+ clienteID +'/'+ myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)

            # context = {'uploaded_file_url': uploaded_file_url}

            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

class Servicios(APIView):
    def get(self, request):
        datos = Servicio.objects.all()
        serializer = ServiciosSerializers(datos, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 

    def post(self, request):
        serializer = ServiciosSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            q = Servicio.objects.get(pk=pk)
            q.delete()
            return Response({"message":"success", "Eliminado":q.tipoServicio},status=status.HTTP_202_ACCEPTED)
        except:
            raise Http404

    def patch(self, request, pk):
        try:
            q = Servicio.objects.get(pk=pk)
            serializer = ServiciosSerializers(q, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({"message":"success", "Actualizado":q.tipoServicio},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"message":"wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)
    
def setServicios(clietenID, serviciosName='0'):
    try:
        clientePatch = cliente.objects.get(pk=clietenID)
        clientePatch.servicios.clear()
        for servicioCliente in serviciosName:
            id = Servicio.objects.get(tipoServicio=servicioCliente)
            #print(id.pk)
            clientePatch.servicios.add(id.pk)
    except:
        print('Service DoesNotExist')



def descargaxls(request):
    registros= cliente.objects.all()
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="archivo.csv"'
    writer = csv.writer(response, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['id', 'Cliente','Numero Contacto', 'Email contraparte', 'Tipo contrato ','Fecha fin contrato', 'Fecha de Inicio contrato', 'Ejecutivo actual ',
                        'Ejecutivo Cierre','Desistido', 'Servicios'])

    for registro in registros:
        writer.writerow([registro.pk, registro.nombre, registro.numeroContacto, registro.email, registro.tipoContrato, registro.fechaFinContrato, registro.fechaInicioContrato,
                            registro.ejecutivoCierre, registro.ejecutivoActual, registro.desistido, registro.servicios.all()])
    return response

class ejecutivosT(APIView):
    def get(self, request):
        print("Autenticacion: {}".format(request.auth))
        print("Cuerpo: {}".format(request.data))
        try:
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            if response:
                user, token = response
                print(user)
                print(token)
                datos = ejecutivo.objects.all()
                serializer = dbEjecutivosSerializer(datos, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 
            else: 
                return Response(status=status.HTTP_401_UNAUTHORIZED)


        except ejecutivo.DoesNotExist:
            raise Http404