from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from AuthAccounts.models import User
from guide.models import Guide, Route, Like, DisLike, Share
from guide.serializers import CreateGuideSerializer, CreateRouteSerializer
from rest_framework.response import Response


# Create your views here.
class CreateGuideView(CreateAPIView):
    serializer_class = CreateGuideSerializer
    permission_classes = [IsAuthenticated]
    queryset = Guide.objects.all()


class GetUpdateDestroyGuideView(GenericAPIView):
    serializer_class = CreateGuideSerializer
    permission_classes = [IsAuthenticated]
    queryset = Guide.objects.all()

    def get(self, request, pk):
        guide = Guide.objects.get(pk=pk)
        serializer = self.serializer_class(guide)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            guide = Guide.objects.get(pk=pk)
        except Guide.DoesNotExist:
            return Response({'message': 'Guide not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(guide, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            guide = Guide.objects.get(pk=pk)
        except Guide.DoesNotExist:
            return Response({'message': 'Guide not found'}, status=status.HTTP_404_NOT_FOUND)

        guide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateRouteView(CreateAPIView):
    serializer_class = CreateRouteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()


class GetUpdateDestroyRouteView(GenericAPIView):
    serializer_class = CreateGuideSerializer
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()

    def get(self, request, pk):
        route = Route.objects.get(pk=pk)
        serializer = self.serializer_class(route)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

        route.delete()
        return Response({'message': 'Route deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class LikeRouteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()

    def post(self, request, route_id, user_id):
        try:
            route = self.queryset.get(pk=route_id)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            existing_likes = route.likes.filter(user=user)
            if existing_likes.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            like = Like.objects.create(user=user)
            route.likes.add(like)
        route.save()

        return Response(status=status.HTTP_200_OK)


class UnLikeRouteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()

    def post(self, request, route_id, user_id):
        try:
            route = Route.objects.get(pk=route_id)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        existing_likes = route.likes.filter(user=user)
        if not existing_likes.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            existing_likes.delete()
            route.likes.remove(existing_likes.first())

        route.save()

        return Response(status=status.HTTP_200_OK)


class DisLikeRouteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()

    def post(self, request, route_id, user_id):
        try:
            route = Route.objects.get(pk=route_id)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        existing_dislikes = route.dislikes.filter(user=user)
        if existing_dislikes.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        dislike = DisLike.objects.create(user=user)
        route.dislikes.add(dislike)
        return Response(status=status.HTTP_200_OK)


class UnDisLikeRouteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()

    def post(self, request, route_id, user_id):
        try:
            route = Route.objects.get(pk=route_id)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        existing_dislikes = route.dislikes.filter(user=user)
        if not existing_dislikes.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            existing_dislikes.delete()
            route.dislikes.remove(existing_dislikes.first())

        return Response(status=status.HTTP_200_OK)


class ShareRouteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()

    def get(self, request, route_id, user_id):
        try:
            route = Route.objects.get(pk=route_id)
        except Route.DoesNotExist:
            return Response({'message': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            share = Share.objects.create(user=user)
            route.shares.add(share)

        return Response({'shares': route.shares.count()}, status=status.HTTP_200_OK)
