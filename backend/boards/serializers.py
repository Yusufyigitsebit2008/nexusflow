from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Workspace, Board, List, Card, Comment, Attachment, ChecklistItem

User = get_user_model()

# --- 1. EN TEMEL PARÇALAR (Bağımlılığı Olmayanlar) ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AttachmentSerializer(serializers.ModelSerializer):
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'uploaded_at', 'filename', 'card'] # 'card' alanı şart!

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'card', 'text', 'is_done'] # 👈 'card' EKLENDİ


class CardSerializer(serializers.ModelSerializer):
    assignees = UserSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    checklist_items = ChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = '__all__'

# --- 3. ÜST SEVİYE (Bunlar Card'ı kullanır) ---

class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    workspace_name = serializers.ReadOnlyField(source='workspace.name')
    members = UserSerializer(many=True, read_only=True)
    lists = ListSerializer(many=True, read_only=True) 

    class Meta:
        model = Board
        fields = '__all__'

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    boards = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owner', 'members', 'boards']

    def get_boards(self, obj):
        return [{"id": b.id, "name": b.name} for b in obj.boards.all()]
    
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    actor_name = serializers.ReadOnlyField(source='actor.username')
    
    class Meta:
        model = Activity
        fields = ['id', 'actor_name', 'action_type', 'description', 'created_at']