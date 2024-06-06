from django.shortcuts import render

from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from rest_framework import status

from api.models import Task

from api.serializers import TaskSerializer,UserSerializer

from rest_framework.views import APIView
     
from rest_framework import authentication,permissions

from rest_framework import serializers





class TaskViewSetView(ViewSet):
    
    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get_object(self,id):
         
        return Task.objects.get(id=id)
    
    def list(self,request,*args,**kwargs):

        qs=Task.objects.filter(user_object=request.user)

        serializer_instance=TaskSerializer(qs,many=True)

        return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
    

    def create(self,request,*args,**kwargs):

        data=request.data

        serializer_instance=TaskSerializer(data=data)

        if serializer_instance.is_valid():

            serializer_instance.save(user_object=request.user)    # for model serializer

            # task.object.create(serializer_instance.validated_date)     #for normal serializer

            return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)

        return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,*args,**kwargs):
    
           id=kwargs.get("pk")

           qs=self.get_object(id)   # task objecct

           if qs.user_object!=request.user:
                
                raise serializers.ValidationError("permission denied")

           serializer_instance=TaskSerializer(qs)

           return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
   
    def get_object(self,id):
         
         return Task.objects.get(id=id)
    

    def update(self,request,*args,**kwargs):

         id=kwargs.get("pk")

         task_object=self.get_object(id)

         if request.user!=task_object.user_object:

              raise serializers.ValidationError("permission denied")

         serializer_instance=TaskSerializer(data=request.data,instance=task_object)

         if serializer_instance.is_valid():
              
              serializer_instance.save()

              return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
         
         return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
         
         id=kwargs.get("pk")

         task_object=Task.objects.get(id=id)

         if request.user!=task_object.user_object:
              
              raise serializers.ValidationError("permission denied")
              
         Task.objects.get(id=id).delete()

         return Response(data={"message":"deleted"},status=status.HTTP_200_OK)
    
    
class UserView(APIView):

     def post(self,request,*args,**kwargs):

          serializer_instance=UserSerializer(data=request.data)

          if serializer_instance.is_valid():

               serializer_instance.save()

               return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)
          
          return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
         
