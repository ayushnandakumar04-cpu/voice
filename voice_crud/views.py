from django.shortcuts import render
from django.contrib.auth.models import User
from voice_crud.models import Feedback
from rest_framework.views import APIView
from voice_crud.serializers import UserSerializers,FeedBackSerializers
from rest_framework.response import Response
from rest_framework import authentication,permissions,status
from django.shortcuts import get_object_or_404
from voice_crud.app_permissions import IsOwner
from django.db.models import Count
# Create your views here.

class SignupRegisterView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializers(data=form_data)
        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            user_object=User.objects.create_user(**cleaned_data)
            serializer_instance=UserSerializers(user_object)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class GetMeView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user=request.user
        qs=User.objects.get(username=auth_user)
        serializer_instance=UserSerializers(qs)
        return Response(data=serializer_instance.data)

class FeedBackListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        qs=Feedback.objects.filter(student=request.user)
        serializers=FeedBackSerializers(qs,many=True) 
        return Response(data=serializers.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=FeedBackSerializers(data=form_data)
        if serializer_instance.is_valid() :
            serializer_instance.save(student=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class FeedBackListRetrieveview(APIView):
     authentication_classes=[authentication.TokenAuthentication]
     permission_classes=[IsOwner]

     def get(self,request,pk=None):
        qs=get_object_or_404(Feedback,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance=FeedBackSerializers(qs)
        return Response(data=serializer_instance.data)
     
     def put(self,request,pk=None):
         instance=get_object_or_404(Feedback,id=pk)
         self.check_object_permissions(request,instance)
         form_data=request.data
         serializer_instance=FeedBackSerializers(data=form_data,instance=instance)
         if serializer_instance.is_valid(): 
             serializer_instance.save()
             return Response(serializer_instance.data)
         else:
            return Response(serializer_instance.errors)
          

     def delete(self,request,pk=None):
         instance=get_object_or_404(Feedback,id=pk)
         self.check_object_permissions(request,instance)
         instance.delete()
         return Response({"message": "Expense deleted successfully"})



class FeedbackSummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        feedbacks = Feedback.objects.filter(student=request.user)
        sentiment_counts = feedbacks.values('sentiment').annotate(total=Count('id'))
        category_counts = feedbacks.values('category').annotate(total=Count('id'))

        return Response({
            'total_feedback': feedbacks.count(),
            'sentiment_counts': {
                item.get('sentiment'): item.get('total')
                for item in sentiment_counts},
            'category_counts': {
                item.get('category'): item.get('total')
                for item in category_counts}
        })
