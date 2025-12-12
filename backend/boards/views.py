from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model 
import random
from rest_framework.views import APIView 
from django.db.models import Q 
from .models import Attachment
from .serializers import AttachmentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ChecklistItem 
from .serializers import ChecklistItemSerializer 
from .models import Workspace, Board, List, Card, Comment
from .serializers import (
    WorkspaceSerializer, BoardSerializer, ListSerializer, 
    CardSerializer, CommentSerializer, RegisterSerializer
)
from .ai_service import generate_card_description

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Aktif User modelini çek
User = get_user_model()

# --- KAYIT OLMA (REGISTER) VIEW ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# --- WORKSPACE ---
class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(owner=user) | Workspace.objects.filter(members=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# --- BOARD ---
class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(workspace__owner=self.request.user) | Board.objects.filter(workspace__members=self.request.user)

# --- LIST ---
class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = List.objects.all()

# --- CARD ---
class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Card.objects.all()

    @action(detail=False, methods=['post'])
    def ai_generate(self, request):
        title = request.data.get('title')
        if not title:
             return Response({'error': 'Başlık gerekli!'}, status=400)
        ai_response = generate_card_description(title)
        return Response({'description': ai_response})

    def perform_update(self, serializer):
        instance = serializer.save()
        self.notify_websockets(instance, 'card_updated', CardSerializer(instance).data)

    def perform_create(self, serializer):
        instance = serializer.save()
        self.notify_websockets(instance, 'card_created', {
            'list_id': instance.list.id,
            'card': CardSerializer(instance).data
        })
    
    def perform_destroy(self, instance):
        card_id = instance.id
        list_id = instance.list.id
        board_id = instance.list.board.id
        instance.delete()
        
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'board_{board_id}',
                {
                    'type': 'board_update',
                    'data': {
                        'action': 'card_deleted',
                        'card_id': card_id,
                        'list_id': list_id
                    }
                }
            )
        except Exception as e:
            print(f"WebSocket Hatası (Delete): {e}")

    def notify_websockets(self, instance, action, data):
        try:
            channel_layer = get_channel_layer()
            board_id = str(instance.list.board.id)
            async_to_sync(channel_layer.group_send)(
                f'board_{board_id}',
                {'type': 'board_update', 'data': {'action': action, **data}}
            )
        except Exception as e:
            print(f"WebSocket Hatası (Card): {e}")

# --- COMMENT ---
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        try:
            channel_layer = get_channel_layer()
            board_id = str(instance.card.list.board.id)
            async_to_sync(channel_layer.group_send)(
                f'board_{board_id}',
                {
                    'type': 'board_update',
                    'data': {
                        'action': 'new_comment',
                        'card_id': str(instance.card.id),
                        'comment': CommentSerializer(instance).data
                    }
                }
            )
        except Exception as e:
            print(f"WebSocket Hatası (Comment): {e}")

class GenerateDemoDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # 1. Demo Workspace Oluştur
        ws_names = ["Start-Up Projesi", "Yazılım Ekibi", "Pazarlama Kampanyası"]
        ws = Workspace.objects.create(name=random.choice(ws_names), owner=user)
        ws.members.add(user)

        # 2. İçine 2 Tane Board Ekle
        board_names = ["Mobil Uygulama", "Web Sitesi Revize", "Q3 Hedefleri", "Sosyal Medya"]
        chosen_boards = random.sample(board_names, 2)
        
        for b_name in chosen_boards:
            board = Board.objects.create(name=b_name, workspace=ws)
            
            # 3. Listeleri Ekle
            lists = ["Yapılacaklar", "Sürüyor", "Test", "Tamamlandı"]
            
            for i, list_title in enumerate(lists):
                l = List.objects.create(title=list_title, board=board, position=i)
                
                # 4. Rastgele Kartlar Ekle (Her listeye 0-3 arası)
                card_titles = [
                    "Login sayfası tasarımı", "API entegrasyonu", "Bug fix: Header kayması",
                    "Müşteri toplantısı", "Veritabanı yedeği", "Logo revizesi",
                    "Dark mode desteği", "Unit testleri yaz"
                ]
                
                for _ in range(random.randint(0, 3)):
                    Card.objects.create(
                        title=random.choice(card_titles),
                        list=l,
                        description="Bu bir otomatik oluşturulmuş demo kartıdır.",
                        priority=random.choice(['low', 'medium', 'high', 'urgent'])
                    )

        return Response({"message": "Demo verileri başarıyla oluşturuldu! 🚀"})
class GlobalSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])

        results = []

        # 1. Panolarda Ara
        boards = Board.objects.filter(
            Q(name__icontains=query) & 
            (Q(workspace__owner=request.user) | Q(workspace__members=request.user))
        ).distinct()[:5] # İlk 5 sonuç
        
        for b in boards:
            results.append({
                'type': 'board',
                'title': b.name,
                'subtitle': f"Pano - {b.workspace.name}",
                'url': f"/board/{b.id}",
                'icon': '📋'
            })

        # 2. Kartlarda Ara
        cards = Card.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            list__board__workspace__owner=request.user # Basit yetki kontrolü
        ).distinct()[:10] # İlk 10 sonuç

        for c in cards:
            results.append({
                'type': 'card',
                'title': c.title,
                'subtitle': f"Kart - {c.list.board.name}",
                'url': f"/board/{c.list.board.id}", 
                'icon': '📝'
            })

        return Response(results)
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) 

    def perform_create(self, serializer):
        serializer.save()

class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
from .models import Activity
from .serializers import ActivitySerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.request.query_params.get('board')
        if board_id:
            return Activity.objects.filter(board_id=board_id)
        return Activity.objects.none()