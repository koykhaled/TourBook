from Tour_Organizer.models.tour import Reaction, ReactionState
from django.core import exceptions


class ReactionService:

    @staticmethod
    def check_existing_reaction(user):
        # check the reaction for authenticated client is already exist
        return Reaction.objects.filter(user=user)

    @staticmethod
    def create_reaction(tour, data, user):
        tour.reaction.create(
            reaction=data, user=user)
        return "Reaction Added Successfully!"

    @staticmethod
    def update_or_delete_reaction(reaction, data):
        message = ""
        if reaction.reaction != data:
            message = ReactionService.toggle_reaction(reaction, data)
        else:
            message = ReactionService.remove_reaction(reaction)
        return message

    @staticmethod
    def toggle_reaction(reaction_obj, data):
        # toggle the reaction => if the client already liked the tour and change it to dislike
        reaction_obj.reaction = data
        reaction_obj.save()
        return "Reaction Updated Successfully"

    @staticmethod
    def remove_reaction(reaction_obj):
        # remove the reaction if client click in the same reaction he made before
        reaction_obj.delete()
        return "Reaction Deleted Successfully"

    @staticmethod
    def validate_reaction(reaction):
        if reaction not in ReactionState.get_ReactionState():
            raise exceptions.ValidationError("Your Reaction Not Supported!!")
        return True
