from django.http import response
from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Plate
from .serializers import PlateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

def search(request):
    query = request.GET.get('query')
    search_results = Plate.objects.filter(Q(plate__icontains=query))
    print(search_results)
    return render(request, 'search.html', {'plates': search_results, 'query': query})


def index_view(request):
    plates = Plate.objects.all()
    context = {
        'plates': plates
    }
    return render(request, 'index.html', context)


class PlateList(generics.ListCreateAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Plate.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("Can't delete other user's plates")

    def put(self, request, *args, **kwargs):
        post = Plate.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError("Can't edit other user's plates")

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

class PlateByUserCreateView(LoginRequiredMixin, CreateView):
    model = Plate
    fields = ['plate']
    success_url = ""
    template_name = 'user_plate_new.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

