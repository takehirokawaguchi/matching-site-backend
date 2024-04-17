from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from django.http import Http404
from django.db.models import Q, Max
from django.db.models.functions import Greatest, Least
from .models import User, Product
from .permisson import IsUserOrReadOnly
from .serializers import  *


class UserDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]


    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Userデータの更新
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()

        # Profileデータの再構築（レスポンスを確認するとネストからフラットな状態に変化していた）
        profile_data = {
            'affiliation': request.data.get('profile[affiliation]', ''),
            'company': request.data.get('profile[company]', ''),
            'industry': request.data.get('profile[industry]', ''),
            'bio': request.data.get('profile[bio]', ''),
            'profile_image': request.data.get('profile[profile_image]', None)
        }
        
        # Profileデータの更新
        profile_serializer = ProfileSerializer(user.profile, data=profile_data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            })
        else:
            return Response({
                'user_errors': user_serializer.errors,
                'profile_errors': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ProductList(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = ProductSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, pk):
        todo = self.get_object(pk)
        serializer = ProductSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyInbox(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        # 各ユーザー間の会話を一意に特定して、最後のメッセージを取得
        last_message_ids = ChatMessage.objects.filter(
            Q(sender_id=user_id) |
            Q(receiver_id=user_id)
        ).values('sender_id', 'receiver_id').annotate(
            smaller_id=Least('sender_id', 'receiver_id'),
            larger_id=Greatest('sender_id', 'receiver_id')
        ).values('smaller_id', 'larger_id').annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)

        # 上記のサブクエリを使って最新のメッセージだけを取得
        messages = ChatMessage.objects.filter(
            id__in=last_message_ids
        ).order_by('-created_at')

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

# テスト用（メッセージが格納されているか確認）
class GetAllMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):

        messages = ChatMessage.objects.all()

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

class GetMessages(APIView):

    def get(self, request, *args, **kwargs):
        sender_id = self.kwargs["sender_id"]
        receiver_id = self.kwargs["receiver_id"]

        messages = ChatMessage.objects.filter(
            sender__in=[sender_id, receiver_id],
            receiver__in=[sender_id, receiver_id]
        )

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

class SendMessage(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer

# 採用担当者のみ使用可能
class SearchUser(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_class = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = User.objects.filter(
            Q(username__icontains=username)|
            Q(email__icontains=username)
            # &~Q(user=logged_in_user)
        )

        if not users.exists():
            return Response(
                {"detail": "ユーザーが見つかりません。"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)