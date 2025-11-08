from  django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .models import Allert
from .serializers import AllertSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework import status


@api_view(['POST'])
def AllertPingLossAPI(request):
    description = request.data.get('description')
    device_id = request.data.get('device_id')
    ping_status = request.data.get('ping_status')

    if not description or not device_id or not ping_status:
        return Response(
            {"errors": "description, device_id и ping_status обязательны"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if ping_status.lower() == 'loss':
        target_status = 'open'
    elif ping_status.lower() == 'up':
        target_status = 'resolved'
    else:
        return Response({"error": "ping_status не удовлетворяет условиям"}, status=status.HTTP_400_BAD_REQUEST)

    # Пытаемся найти открытый инцидент по device_id
    alert = Allert.objects.filter(device_id=device_id, status='open').first()

    if alert and target_status == 'resolved':
        # Закрываем существующий инцидент
        alert.status = 'resolved'
        alert.save()
        return Response({"message": f"Инцидент {alert.id} закрыт"}, status=status.HTTP_200_OK)

    if not alert and target_status == 'open':
        # Создаём новый инцидент
        alert = Allert.objects.create(
            description=description,
            device_id=device_id,
            status='open',
            source='monitoring'
        )
        return Response({
            "id": alert.id,
            "description": alert.description,
            "device_id": alert.device_id,
            "status": alert.status
        }, status=status.HTTP_201_CREATED)

    # Если нет действий для выполнения
    return Response({"message": "Нет действий для выполнения"}, status=status.HTTP_200_OK)


def allerts_view(request):

    status_filter = request.GET.get('status', '')
    if status_filter:
        alerts = Allert.objects.filter(status = status_filter).order_by('create_time')
    else:
        alerts = Allert.objects.all().order_by('create_time')

    if request.method == 'POST' and 'description' in request.POST:
        description = request.POST.get('description')
        source = request.POST.get('source', 'operator')
        device_id = request.POST.get('device_id', None)
        Allert.objects.create(description=description, source=source,device_id=device_id)
        return redirect('allerts_view')

    if request.method == 'POST' and 'search_id' in request.POST:
        alert_id = request.POST.get('search_id')
        new_status = request.POST.get('new_status')
        alert = get_object_or_404(Allert, id=alert_id)
        alert.status = new_status
        alert.save()
        return redirect('allerts_view')

    return render(request, 'lostsignal/allerts.html', {
        'alerts': alerts,
        'status_filter': status_filter
    })