from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Card, List, Comment, Activity, Attachment

@receiver(post_save, sender=Card)
def log_card_activity(sender, instance, created, **kwargs):
    board = instance.list.board
    user = instance.assignees.first()

    actor = board.workspace.owner 

    if created:
        action = "Kart Oluşturdu"
        desc = f"'{instance.title}' kartı '{instance.list.title}' listesine eklendi."
    else:
        action = "Kart Güncelledi"
        desc = f"'{instance.title}' kartında değişiklik yapıldı."

    Activity.objects.create(
        actor=actor,
        action_type=action,
        content_type=instance.get_content_type_obj(), # Bunu modelde tanımlayacağız
        object_id=instance.id,
        board=board,
        description=desc
    )

@receiver(post_save, sender=Comment)
def log_comment_activity(sender, instance, created, **kwargs):
    if created:
        board = instance.card.list.board
        Activity.objects.create(
            actor=instance.author,
            action_type="Yorum Yaptı",
            content_type=instance.get_content_type_obj(), # Modelde tanımlayacağız
            object_id=instance.id,
            board=board,
            description=f"'{instance.card.title}' kartına yorum yaptı: {instance.text[:20]}..."
        )

@receiver(post_save, sender=Attachment)
def log_attachment_activity(sender, instance, created, **kwargs):
    if created:
        board = instance.card.list.board
        Activity.objects.create(
            actor=board.workspace.owner, # Şimdilik owner
            action_type="Dosya Yükledi",
            content_type=instance.get_content_type_obj(), # Modelde tanımlayacağız
            object_id=instance.id,
            board=board,
            description=f"'{instance.card.title}' kartına dosya eklendi."
        )