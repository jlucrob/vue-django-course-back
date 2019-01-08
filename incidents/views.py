from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from incidents.models import Incident, Site, Update,Subscriber
from rest_framework.response import Response
from incidents.serializers import SubscriberSerializer, IncidentSerializer, UpdateSerializer, SiteTitleSerializer
from datetime import datetime
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from uuid import UUID


class SubscriberView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            uuid_val = UUID(request.data['id'], version=4)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        subscriber = get_object_or_404(
            Subscriber, unique_id=uuid_val)
        subscriber.delete()
        return Response()


class IncidentViewSet(mixins.ListModelMixin, 
                      mixins.CreateModelMixin, 
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def create(self, request):
        # sanity check that there is data for both serializers and the required site_id
        if 'incident' not in request.data or 'update' not in request.data and 'site_id' in request.data:
            return Response({'error': 'Make sure you fill in all fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        # pushing data through the serializers to validate the data 
        incident = IncidentSerializer(data=request.data['incident'])
        update = UpdateSerializer(data=request.data['update'])
        
        # validate that the site_id is only a number and valid
        try:
            site_id_int = int(request.data['site_id'])
            site = Site.objects.get(id=site_id_int)
            print('Found site!')
        except:
            return Response({'error': 'Please pick a site to file this incident under.'}, status=status.HTTP_400_BAD_REQUEST)
    
        # return errors if there are any
        if not incident.is_valid():
            return Response(incident.errors, status=status.HTTP_400_BAD_REQUEST)
        if not update.is_valid():
            return Response(update.errors, status=status.HTTP_400_BAD_REQUEST)

        # saving the incident and update. Passing extra info along through the save method
        incident = incident.save(site=site)
        update.save(incident=incident, user=request.user)
    
        # putting the incident through the serializer again to get the full data of this object (including auto added data)
        # to be send to the front end
        seralizer = IncidentSerializer(incident)
        return Response(seralizer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=True)
    def toggle_solved(self, request, pk=None):
        incident = self.get_object()
        incident.solved = not incident.solved
        incident.end = datetime.now()
        incident.save()
        return Response({'solved': incident.solved})


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteTitleSerializer


class UpdateViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    
    def perform_create(self, serializer):
        incident = get_object_or_404(Incident, pk=self.request.data["incident_id"])
        serializer.save(user=self.request.user, incident=incident)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if self.request.user == obj.user:
            return obj
        return Response(status=status.HTTP_401_UNAUTHORIZED)