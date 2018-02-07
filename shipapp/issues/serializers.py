# Author : Debojit Kaushik ( 10th April 2017 )
from rest_framework import serializers
from .models import Issue, Solution, Image



#Serializer for Images.
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = (
            'deleted',
        )


#Serializer for Issues.
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        exclude = (
            'deleted',
        )


#Serializer for Solution.
class SolutionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many = True)
    class Meta:
        model = Solution
        exclude = (
            'deleted',
        )


#Serializer for Issues.
class IssueSerializerFields(serializers.ModelSerializer):
    images = ImageSerializer(many = True)
    signature = ImageSerializer()
    solutions = SolutionSerializer(many = True)
    class Meta:
        model = Issue
        # depth = 2
        exclude = (
            'deleted',
        )




#Serializer for Solution fields.
class SolutionSerializerFields(serializers.ModelSerializer):
    class Meta:
        model = Solution
        exclude = (
            'deleted',
        )
