from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import RoomBooking, ZoneBooking
from .serializers import RoomBookingSerializer, ZoneBookingSerializer
from datetime import timedelta, datetime
from django.core.mail import send_mail
from django.conf import settings
from zones.models import Room, Zone
from itertools import combinations
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
import re

class ZoneBookingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ZoneBookingSerializer(data=request.data)
        if serializer.is_valid():
            zone = serializer.validated_data['zone']
            booking_date = serializer.validated_data['booking_date']

            # Проверка на пересечение дат
            overlapping_bookings = ZoneBooking.objects.filter(
                zone=zone,
                booking_date=booking_date
            )

            if overlapping_bookings.exists():
                return Response(
                    {"error": "Эта зона уже забронирована на выбранную дату."},
                    status=400
                )

            serializer.save()

            # Отправка email пользователю
            send_mail(
                subject="Подтверждение бронирования зоны",
                message=(
                    f"Здравствуйте, {serializer.validated_data['name']}!\n\n"
                    f"Вы успешно забронировали зону: {zone.name}\n"
                    f"Дата бронирования: {booking_date}.\n"
                    f"Мы скоро свяжемся с вами для подтверждения.\n\n"
                    f"Спасибо за бронирование!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[serializer.validated_data['email']],
                fail_silently=True,
            )

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RoomBookingListView(ListAPIView):
    queryset = RoomBooking.objects.all().order_by('-created_at')
    serializer_class = RoomBookingSerializer

class ZoneBookingListView(ListAPIView):
    queryset = ZoneBooking.objects.all().order_by('-created_at')
    serializer_class = ZoneBookingSerializer

class BookedDatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        bookings = RoomBooking.objects.all()
        room_dates = {}

        for booking in bookings:
            room_id = booking.room.id
            current_date = booking.check_in

            while current_date < booking.check_out:
                room_dates.setdefault(room_id, []).append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

        return Response(room_dates) 
       
class SmartBookingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            validate_booking_data(data)
        except ValidationError as e:
            raise DRFValidationError({"detail": str(e)})
        check_in = datetime.strptime(data['check_in'], "%Y-%m-%d").date()
        check_out = datetime.strptime(data['check_out'], "%Y-%m-%d").date()
        adults = int(data.get('adults') or 1)
        children = int(data.get('children') or 0)
        total_guests = adults + children
        room_id = data.get("room")

        booked_ids = RoomBooking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)

        # Шаг 1: Если пользователь выбрал конкретную комнату вручную
        if room_id:
            room = Room.objects.filter(id=room_id).first()
            if room and room.id not in booked_ids:
                RoomBooking.objects.create(
                    room=room,
                    name=data['name'],
                    phone=data['phone'],
                    email=data['email'],
                    check_in=check_in,
                    check_out=check_out,
                    adults=adults,
                    children=children,
                    note=data.get('note', '')
                )

                from django.utils.timezone import now

                # Вычисляем количество ночей
                nights = (check_out - check_in).days
                total_guests = adults + children
                total_price = total_guests * nights * room.price_per_night

                send_mail(
                    subject="Подтверждение бронирования",
                    message=(
                        f"Здравствуйте, {data['name']}!\n\n"
                        f"Ваш заказ подтвержден.\n\n"
                        f"📅 Заезд: {check_in.strftime('%Y-%m-%d')}\n"
                        f"📅 Выезд: {check_out.strftime('%Y-%m-%d')}\n"
                        f"⏰ Время заезда / выезда: 14:00 / 12:00\n\n"
                        f"👥 Гостей: {total_guests} (взрослых: {adults}, детей: {children})\n"
                        f"🛏 Кол-во ночей: {nights}\n"
                        f"🏠 Номер: {room.name}\n"
                        f"💰 Стоимость брони: {total_price:,.0f} KZT\n"
                        f"💳 Необходима предоплата: 10,000 KZT\n"
                        f"✅ Принято оплат: 0 KZT\n\n"
                        f"📌 Важная информация:\n"
                        f"Предоплата вносится в течение суток с момента брони через Kaspi по номеру:\n"
                        f"+7 777 777 77 77 (Имя Ф.)\n"
                        f"❗ Обязательно укажите имя клиента и дату заезда в комментарии.\n\n"
                        f"⚠️ В случае отсутствия оплаты бронь может быть аннулирована.\n"
                        f"Возврат предоплаты возможен при форс-мажоре согласно ГК РК.\n\n"
                        f"С уважением,\n"
                        f"Черноярская жемчужина\n"
                        f"📍 Павлодарская область\n"
                        f"📞 +7 777 777 77 77\n"
                        f"📧 info@chernoyarka.kz"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[data['email']],
                    fail_silently=False
                )


                return Response({"success": f"Комната '{room.name}' успешно забронирована!"})
            else:
                return Response({"error": "Выбранная комната уже занята"}, status=400)

        # Шаг 2: Автоматический подбор
        available_rooms = Room.objects.exclude(id__in=booked_ids).order_by('capacity')

        room = available_rooms.filter(capacity__gte=total_guests).first()
        if room:
            RoomBooking.objects.create(
                room=room,
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                check_in=check_in,
                check_out=check_out,
                adults=adults,
                children=children,
                note=data.get('note', '')
            )

            from django.utils.timezone import now

            # Вычисляем количество ночей
            nights = (check_out - check_in).days
            total_guests = adults + children
            total_price = total_guests * nights * room.price_per_night

            send_mail(
                subject="Подтверждение бронирования",
                message=(
                    f"Здравствуйте, {data['name']}!\n\n"
                    f"Ваш заказ подтвержден.\n\n"
                    f"📅 Заезд: {check_in.strftime('%Y-%m-%d')}\n"
                    f"📅 Выезд: {check_out.strftime('%Y-%m-%d')}\n"
                    f"⏰ Время заезда / выезда: 14:00 / 12:00\n\n"
                    f"👥 Гостей: {total_guests} (взрослых: {adults}, детей: {children})\n"
                    f"🛏 Кол-во ночей: {nights}\n"
                    f"🏠 Номер: {room.name}\n"
                    f"💰 Стоимость брони: {total_price:,.0f} KZT\n"
                    f"💳 Необходима предоплата: 10,000 KZT\n"
                    f"✅ Принято оплат: 0 KZT\n\n"
                    f"📌 Важная информация:\n"
                    f"Предоплата вносится в течение суток с момента брони через Kaspi по номеру:\n"
                    f"+7 777 777 77 77 (Имя С.)\n"
                    f"❗ Обязательно укажите имя клиента и дату заезда в комментарии.\n\n"
                    f"⚠️ В случае отсутствия оплаты бронь может быть аннулирована.\n"
                    f"Возврат предоплаты возможен при форс-мажоре согласно ГК РК.\n\n"
                    f"С уважением,\n"
                    f"Черноярская жемчужина\n"
                    f"📍 Павлодарская область\n"
                    f"📞 +7 777 777 77 77\n"
                    f"📧 info@chernoyarka.kz"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[data['email']],
                fail_silently=False
            )


            return Response({"success": f"Комната '{room.name}' успешно забронирована!"})

        # Шаг 3: Комбинированные комнаты
        for r in range(2, len(available_rooms) + 1):
            for combo in combinations(available_rooms, r):
                if sum(room.capacity for room in combo) >= total_guests:
                    room_names = []
                    for room in combo:
                        RoomBooking.objects.create(
                            room=room,
                            name=data['name'],
                            phone=data['phone'],
                            email=data['email'],
                            check_in=check_in,
                            check_out=check_out,
                            adults=0,
                            children=0,
                            note=f"{data.get('note', '')} (Автоназначено)"
                        )
                        room_names.append(room.name)

                    from django.utils.timezone import now

                    # Вычисляем количество ночей
                    nights = (check_out - check_in).days
                    total_guests = adults + children
                    total_price = total_guests * nights * room.price_per_night

                    send_mail(
                        subject="Подтверждение бронирования",
                        message=(
                            f"Здравствуйте, {data['name']}!\n\n"
                            f"Ваш заказ подтвержден.\n\n"
                            f"📅 Заезд: {check_in.strftime('%Y-%m-%d')}\n"
                            f"📅 Выезд: {check_out.strftime('%Y-%m-%d')}\n"
                            f"⏰ Время заезда / выезда: 14:00 / 12:00\n\n"
                            f"👥 Гостей: {total_guests} (взрослых: {adults}, детей: {children})\n"
                            f"🛏 Кол-во ночей: {nights}\n"
                            f"🏠 Номер: {room.name}\n"
                            f"💰 Стоимость брони: {total_price:,.0f} KZT\n"
                            f"💳 Необходима предоплата: 10,000 KZT\n"
                            f"✅ Принято оплат: 0 KZT\n\n"
                            f"📌 Важная информация:\n"
                            f"Предоплата вносится в течение суток с момента брони через Kaspi по номеру:\n"
                            f"+7 777 777 77 77 (Имя Ф.)\n"
                            f"❗ Обязательно укажите имя клиента и дату заезда в комментарии.\n\n"
                            f"⚠️ В случае отсутствия оплаты бронь может быть аннулирована.\n"
                            f"Возврат предоплаты возможен при форс-мажоре согласно ГК РК.\n\n"
                            f"С уважением,\n"
                            f"Черноярская жемчужина\n"
                            f"📍 Павлодарская область\n"
                            f"📞 +7 777 777 77 77\n"
                            f"📧 info@chernoyarka.kz"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[data['email']],
                        fail_silently=False
                    )


                    return Response({"success": f"Бронь оформлена в нескольких номерах: {room_names}"})

        return Response({"error": "Нет доступных номеров для такого количества гостей"}, status=400)
    
def validate_booking_data(data):
    required_fields = ['name', 'phone', 'email', 'check_in', 'check_out']
    for field in required_fields:
        if not data.get(field):
            raise ValidationError(f"Поле '{field}' обязательно.")

    try:
        validate_email(data['email'])
    except ValidationError:
        raise ValidationError("Некорректный email.")

    if len(data['phone']) < 6:
        raise ValidationError("Некорректный номер телефона.")
    try:
        check_in = datetime.strptime(data['check_in'], "%Y-%m-%d").date()
        check_out = datetime.strptime(data['check_out'], "%Y-%m-%d").date()
        today = datetime.now().date()

        if check_in < today:
            raise ValidationError("Нельзя бронировать на прошлую дату.")

        if check_out <= check_in:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")
    except ValueError:
        raise ValidationError("Формат даты должен быть YYYY-MM-DD.")
    
    sql_injection_pattern = re.compile(r"(?:')|(?:--)|(;)|(/\*)|(\*/)|(\b(select|insert|delete|drop|update|union|exec|alter)\b)", re.IGNORECASE)
    fields_to_check = ['name', 'email', 'phone', 'note']

    for field in fields_to_check:
        value = data.get(field, '')
        if sql_injection_pattern.search(value):
            raise ValidationError(f"Недопустимый ввод в поле '{field}'")